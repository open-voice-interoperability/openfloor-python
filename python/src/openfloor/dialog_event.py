from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union, Any, Iterator, Tuple, ClassVar, Type
from enum import Enum
from abc import ABC
import json
from jsonpath_ng import jsonpath, parse
from .json_serializable import JsonSerializableList, JsonSerializableDict, JsonSerializableDataclass
import uuid

def get_isosplit(s: str, split: str) -> Tuple[int, str]:
    """Split string at delimiter and return number and remainder
    Returns 0 and the string if the delimiter is not found or the text preceding the delimiter is not a number"""
    if split in s:
        n, s = s.split(split)
        try:
            n = int(n)
        except:
            n=0
    else:
        n = 0
    return int(n), s

def parse_isoduration(s: str) -> timedelta:
    """Parse ISO 8601 duration format to timedelta
    
    Args:
        s: ISO 8601 duration string (e.g., "PT3H30M15S")
        
    Returns:
        datetime.timedelta object
    """
    # Remove prefix
    s = s.split('P')[-1]
    
    # Step through letter dividers
    days, s = get_isosplit(s, 'D')
    _, s = get_isosplit(s, 'T')
    hours, s = get_isosplit(s, 'H')
    minutes, s = get_isosplit(s, 'M')
    seconds, s = get_isosplit(s, 'S')

    return timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)

def timedelta_to_iso_duration(td: timedelta) -> str:
    """Convert timedelta to ISO 8601 duration format
    
    Args:
        td: datetime.timedelta object
        
    Returns:
        ISO 8601 duration string (e.g., "PT3H30M15S")
    """
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    
    parts = []
    if hours > 0:
        parts.append(f"{hours}H")
    if minutes > 0:
        parts.append(f"{minutes}M")
    if seconds > 0 or not parts:
        parts.append(f"{seconds}S")
    
    return f"PT{''.join(parts)}"

@dataclass
class Span(JsonSerializableDataclass):
    """Represents a time span for a dialog event or token"""
    startTime: Optional[datetime] = None
    startOffset: Optional[timedelta] = None  # Duration as timedelta
    endTime: Optional[datetime] = None
    endOffset: Optional[timedelta] = None  # Duration as timedelta

    def __post_init__(self):
        """Initialize after dataclass initialization"""
        super().__init__()
        if self.endTime is None and self.startOffset is None: # Default to now if there is no startOffset
            self.startTime = datetime.now()
        if self.startTime is not None and self.startOffset is not None:
            raise ValueError(f"Cannot specify both startTime and startOffset: {self.startTime} and {self.startOffset}")
        if self.endTime is not None and self.endOffset is not None:
            raise ValueError(f"Cannot specify both endTime and endOffset: {self.endTime} and {self.endOffset}")
        if self.startTime is None and self.startOffset is None:
            raise ValueError(f"Must specify either startTime or startOffset: {self.startTime} and {self.startOffset}")

    def __iter__(self) -> Iterator[Tuple[str, Any]]:
        """Convert Span instance to JSON-compatible dictionary"""
        if self.startTime is not None:
            yield 'startTime', self.startTime.isoformat()
        if self.startOffset is not None:
            yield 'startOffset', timedelta_to_iso_duration(self.startOffset)
        if self.endTime is not None:
            yield 'endTime', self.endTime.isoformat()
        if self.endOffset is not None:
            yield 'endOffset', timedelta_to_iso_duration(self.endOffset)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Span':
        """Create a Span instance from a dictionary"""
        if 'endTime' in data and isinstance(data['endTime'], str):
            data['endTime'] = datetime.fromisoformat(data['endTime'])
        if 'startTime' in data and isinstance(data['startTime'], str):
            data['startTime'] = datetime.fromisoformat(data['startTime'])
        if 'startOffset' in data and isinstance(data['startOffset'], str):
            data['startOffset'] = parse_isoduration(data['startOffset'])
        if 'endOffset' in data and isinstance(data['endOffset'], str):
            data['endOffset'] = parse_isoduration(data['endOffset'])
        return cls(**data)

@dataclass
class Token(JsonSerializableDataclass):
    """Represents a single token in a feature"""
    value: Optional[Any] = None
    valueUrl: Optional[str] = None
    span: Optional[Span] = None
    confidence: Optional[float] = None
    links: List[str] = field(default_factory=list)  # JSON Path references

    def __post_init__(self):
        """Initialize after dataclass initialization"""
        super().__init__()
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
    
    def linked_values(self,dialog_event) -> List[Tuple[str, Any]]:
        values=[]
        for l in self.links:
            jsonpath_expr = parse(l)
            features_dict=dict(dialog_event.features)
            for match in jsonpath_expr.find(features_dict):
                if match:
                    values.append([match.full_path,match.value])
        return values

@dataclass
class Feature(JsonSerializableDataclass):
    """Represents a feature in a dialog event"""
    mimeType: str
    tokens: List[Token] = field(default_factory=list)
    alternates: List[List[Token]] = field(default_factory=list)
    lang: Optional[str] = None  # BCP 47 language tag
    encoding: Optional[str] = None  # "ISO-8859-1" or "UTF-8"
    tokenSchema: Optional[str] = None  # e.g., "BertTokenizer.from_pretrained(bert-base-uncased)"

    def __post_init__(self):
        """Initialize after dataclass initialization"""
        super().__init__()
        if self.encoding is not None and self.encoding not in ["ISO-8859-1", "UTF-8", "iso-8859-1", "utf-8"]:
            raise ValueError("Encoding must be either 'ISO-8859-1', 'iso-8859-1', 'UTF-8', or 'utf-8'")

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
class TextFeature(Feature):
    """Represents a text feature in a dialog event with mime type set to text/plain by default"""
    mimeType: str = "text/plain"
    values: Optional[List[str]] = field(default=None, repr=False)

    def __post_init__(self):
        """Initialize tokens from values if provided"""
        if self.values is not None:
            self.tokens = [Token(value=value) for value in self.values]

    def __iter__(self) -> Iterator[Tuple[str, Any]]:
        """Exclude the values field from the iteration"""
        yield from super().__iter__()

@dataclass
class DialogEvent(JsonSerializableDataclass):
    """Represents a dialog event according to the specification"""
    speakerUri: str
    id: Optional[str] = None
    span: Optional[Span] = field(default_factory=Span)
    features: Dict[str, Feature] = field(default_factory=dict)
    previousId: Optional[str] = None
    context: Optional[str] = None

    def __post_init__(self):
        """Initialize after dataclass initialization"""
        super().__init__()
        if self.id is None:
            self.id = f"de:{uuid.uuid4()}"
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

class DialogHistory(JsonSerializableList):
    pass

