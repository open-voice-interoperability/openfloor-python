from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Union, Any
from enum import Enum

class TokenSchema(str, Enum):
    """Example token schema enum - this would be expanded based on specific needs"""
    BERT_BASE_UNCASED = "BertTokenizer.from_pretrained(bert-base-uncased)"

@dataclass
class Span:
    """Represents a time span for a dialog event or token"""
    start_time: Optional[datetime] = None
    start_offset: Optional[str] = None  # ISO 8601 duration format
    end_time: Optional[datetime] = None
    end_offset: Optional[str] = None  # ISO 8601 duration format

    def __post_init__(self):
        if self.start_time is not None and self.start_offset is not None:
            raise ValueError("Cannot specify both start_time and start_offset")
        if self.end_time is not None and self.end_offset is not None:
            raise ValueError("Cannot specify both end_time and end_offset")
        if self.start_time is None and self.start_offset is None:
            raise ValueError("Must specify either start_time or start_offset")

@dataclass
class Token:
    """Represents a single token in a feature"""
    value: Optional[Any] = None
    value_url: Optional[str] = None
    span: Optional[Span] = None
    confidence: Optional[float] = None
    links: List[str] = field(default_factory=list)  # JSON Path references

    def __post_init__(self):
        if self.value is None and self.value_url is None:
            raise ValueError("Must specify either value or value_url")
        if self.value is not None and self.value_url is not None:
            raise ValueError("Cannot specify both value and value_url")
        if self.confidence is not None and not 0 <= self.confidence <= 1:
            raise ValueError("Confidence must be between 0 and 1")

@dataclass
class Feature:
    """Represents a feature in a dialog event"""
    mime_type: str = "text/plain"
    tokens: List[Token] = field(default_factory=list)
    alternates: List[List[Token]] = field(default_factory=list)
    lang: Optional[str] = None  # BCP 47 language tag
    encoding: Optional[str] = None  # "ISO-8859-1" or "UTF-8"
    token_schema: Optional[str] = None

    def __post_init__(self):
        if self.encoding is not None and self.encoding not in ["ISO-8859-1", "UTF-8"]:
            raise ValueError("Encoding must be either 'ISO-8859-1' or 'UTF-8'")

@dataclass
class DialogEvent:
    """Represents a dialog event according to the specification"""
    id: str
    speaker_uri: str
    span: Span
    features: Dict[str, Feature] = field(default_factory=dict)
    previous_id: Optional[str] = None
    context: Optional[str] = None

    def __post_init__(self):
        if not self.features:
            raise ValueError("Dialog event must contain at least one feature") 