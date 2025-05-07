from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Dict, List, Optional, Union, Any, Iterator, Tuple, ClassVar, Type
from enum import Enum
from abc import ABC
import json

class JsonSerializable(ABC):
    """Base class for JSON serializable objects"""
    def __iter__(self) -> Iterator[Tuple[str, Any]]:
        """Convert instance to JSON-compatible dictionary"""
        raise NotImplementedError

    def to_json(self, **kwargs) -> str:
        """Convert instance to JSON string"""
        return json.dumps(dict(self), **kwargs)

    @classmethod
    def from_json(cls, json_str: str, **kwargs) -> 'JsonSerializable':
        """Create an instance from a JSON string"""
        data = json.loads(json_str, **kwargs)
        return cls.from_dict(data)

class TokenSchema(str, Enum):
    """Example token schema enum - this would be expanded based on specific needs"""
    BERT_BASE_UNCASED = "BertTokenizer.from_pretrained(bert-base-uncased)"

@dataclass
class Span(JsonSerializable):
    """Represents a time span for a dialog event or token"""
    startTime: Optional[str] = field(default_factory=lambda: datetime.now().isoformat())
    startOffset: Optional[str] = None  # ISO 8601 duration format
    endTime: Optional[datetime] = None
    endOffset: Optional[str] = None  # ISO 8601 duration format

    def __post_init__(self):
        if self.startTime is not None and self.startOffset is not None:
            raise ValueError("Cannot specify both startTime and startOffset")
        if self.endTime is not None and self.endOffset is not None:
            raise ValueError("Cannot specify both endTime and endOffset")
        if self.startTime is None and self.startOffset is None:
            raise ValueError("Must specify either startTime or startOffset")

    def __iter__(self) -> Iterator[Tuple[str, Any]]:
        """Convert Span instance to JSON-compatible dictionary"""
        if self.startTime is not None:
            yield 'startTime', self.startTime
        if self.startOffset is not None:
            yield 'startOffset', self.startOffset
        if self.endTime is not None:
            yield 'endTime', self.endTime.isoformat()
        if self.endOffset is not None:
            yield 'endOffset', self.endOffset

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Span':
        """Create a Span instance from a dictionary"""
        if 'endTime' in data and isinstance(data['endTime'], str):
            data['endTime'] = datetime.fromisoformat(data['endTime'])
        return cls(**data)

@dataclass
class Token(JsonSerializable):
    """Represents a single token in a feature"""
    value: Optional[Any] = None
    valueUrl: Optional[str] = None
    span: Optional[Span] = None
    confidence: Optional[float] = None
    links: List[str] = field(default_factory=list)  # JSON Path references

    def __post_init__(self):
        if self.value is None and self.valueUrl is None:
            raise ValueError("Must specify either value or valueUrl")
        if self.value is not None and self.valueUrl is not None:
            raise ValueError("Cannot specify both value and valueUrl")
        if self.confidence is not None and not 0 <= self.confidence <= 1:
            raise ValueError("Confidence must be between 0 and 1")

    def __iter__(self) -> Iterator[Tuple[str, Any]]:
        """Convert Token instance to JSON-compatible dictionary"""
        if self.value is not None:
            yield 'value', self.value
        if self.valueUrl is not None:
            yield 'valueUrl', self.valueUrl
        if self.span is not None:
            yield 'span', dict(self.span)
        if self.confidence is not None:
            yield 'confidence', self.confidence
        if self.links:
            yield 'links', self.links

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Token':
        """Create a Token instance from a dictionary"""
        if 'span' in data:
            data['span'] = Span.from_dict(data['span'])
        return cls(**data)

@dataclass
class Feature(JsonSerializable):
    """Represents a feature in a dialog event"""
    mimeType: str = "text/plain"
    tokens: List[Token] = field(default_factory=list)
    alternates: List[List[Token]] = field(default_factory=list)
    lang: Optional[str] = None  # BCP 47 language tag
    encoding: Optional[str] = None  # "ISO-8859-1" or "UTF-8"
    tokenSchema: Optional[str] = None

    def __post_init__(self):
        if self.encoding is not None and self.encoding not in ["ISO-8859-1", "UTF-8"]:
            raise ValueError("Encoding must be either 'ISO-8859-1' or 'UTF-8'")

    def __iter__(self) -> Iterator[Tuple[str, Any]]:
        """Convert Feature instance to JSON-compatible dictionary"""
        yield 'mimeType', self.mimeType
        yield 'tokens', [dict(token) for token in self.tokens]
        if self.alternates:
            yield 'alternates', [[dict(token) for token in alt] for alt in self.alternates]
        if self.lang is not None:
            yield 'lang', self.lang
        if self.encoding is not None:
            yield 'encoding', self.encoding
        if self.tokenSchema is not None:
            yield 'tokenSchema', self.tokenSchema

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Feature':
        """Create a Feature instance from a dictionary"""
        if 'tokens' in data:
            data['tokens'] = [Token.from_dict(token) for token in data['tokens']]
        if 'alternates' in data:
            data['alternates'] = [[Token.from_dict(token) for token in alt] for alt in data['alternates']]
        return cls(**data)

@dataclass
class DialogEvent(JsonSerializable):
    """Represents a dialog event according to the specification"""
    id: str
    speakerUri: str
    span: Span
    features: Dict[str, Feature] = field(default_factory=dict)
    previousId: Optional[str] = None
    context: Optional[str] = None

    def __post_init__(self):
        if not self.features:
            raise ValueError("Dialog event must contain at least one feature")

    def __iter__(self) -> Iterator[Tuple[str, Any]]:
        """Convert DialogEvent instance to JSON-compatible dictionary"""
        yield 'id', self.id
        yield 'speakerUri', self.speakerUri
        yield 'span', dict(self.span)
        yield 'features', {name: dict(feature) for name, feature in self.features.items()}
        if self.previousId is not None:
            yield 'previousId', self.previousId
        if self.context is not None:
            yield 'context', self.context

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DialogEvent':
        """Create a DialogEvent instance from a dictionary"""
        if 'span' in data:
            data['span'] = Span.from_dict(data['span'])
        if 'features' in data:
            data['features'] = {name: Feature.from_dict(feature) for name, feature in data['features'].items()}
        return cls(**data) 