from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Iterator, Tuple
from datetime import datetime
from .json_serializable import JsonSerializableDict, JsonSerializableList, JsonSerializableDataclass
from .manifest import Identification
from .dialog_event import DialogHistory
import uuid
import json

@dataclass
class Schema(JsonSerializableDataclass):
    """Represents the schema section of an Open Floor message envelope"""
    version: str = "1.0.0"
    url: Optional[str] = None

    def __post_init__(self):
        """Initialize after dataclass initialization"""
        if self.version is None:
            self.version="1.0.0"

    def __iter__(self) -> Iterator[Tuple[str, Any]]:
        """Convert Schema instance to JSON-compatible dictionary"""
        yield 'version', self.version
        if self.url is not None:
            yield 'url', self.url

class Parameters(JsonSerializableDict):
    """Represents a dictionary of parameters that can be serialized to JSON"""
    pass

class PersistentState(JsonSerializableDict):
    """Represents the persistent state of a conversant that can be serialized to JSON"""
    pass

@dataclass
class Conversant(JsonSerializableDataclass):
    """Represents a conversant in the conversation"""
    identification: Identification
    persistentState: PersistentState = field(default_factory=PersistentState)

    def __post_init__(self):
        """Initialize after dataclass initialization"""
        if self.identification is None:
            raise ValueError("identification is required for the Conversant")

    def __iter__(self) -> Iterator[Tuple[str, Any]]:
        """Convert Conversant instance to JSON-compatible dictionary"""
        yield 'identification', dict(self.identification)
        if self.persistentState:
            yield 'persistentState', dict(self.persistentState)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Conversant':
        """Create a Conversant instance from a dictionary"""
        if 'identification' in data:
            data['identification'] = Identification.from_dict(data['identification'])
        if 'persistentState' in data:
            data['persistentState'] = PersistentState(data['persistentState'])
        return cls(**data)

@dataclass
class Conversation(JsonSerializableDataclass):
    """Represents the conversation section of an Open Floor message envelope"""
    id: Optional[str] = None
    conversants: List[Conversant] = field(default_factory=list)

    def __post_init__(self):
        """Initialize after dataclass initialization"""
        if self.id is None:
            self.id = f"conv:{uuid.uuid4()}"

    def __iter__(self) -> Iterator[Tuple[str, Any]]:
        """Convert Conversation instance to JSON-compatible dictionary"""
        yield 'id', self.id
        if self.conversants:
            yield 'conversants', [dict(conversant) for conversant in self.conversants]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Conversation':
        """Create a Conversation instance from a dictionary"""
        if 'conversants' in data:
            data['conversants'] = [Conversant.from_dict(conv) for conv in data['conversants']]
        return cls(**data)

@dataclass
class Sender(JsonSerializableDataclass):
    """Represents the sender section of an Open Floor message envelope"""
    speakerUri: str
    serviceUrl: Optional[str] = None

    def __iter__(self) -> Iterator[Tuple[str, Any]]:
        """Convert Sender instance to JSON-compatible dictionary"""
        yield 'speakerUri', self.speakerUri
        if self.serviceUrl is not None:
            yield 'serviceUrl', self.serviceUrl

@dataclass
class To(JsonSerializableDataclass):
    """Represents the 'to' section of an event"""
    speakerUri: Optional[str] = None
    serviceUrl: Optional[str] = None
    private: bool = False

    def __post_init__(self):
        """Initialize after dataclass initialization"""
        if self.speakerUri is None and self.serviceUrl is None:
            raise ValueError("Must specify either speakerUri or serviceUrl")

    def __iter__(self) -> Iterator[Tuple[str, Any]]:
        """Convert To instance to JSON-compatible dictionary"""
        if self.speakerUri is not None:
            yield 'speakerUri', self.speakerUri
        if self.serviceUrl is not None:
            yield 'serviceUrl', self.serviceUrl
        if self.private:
            yield 'private', self.private

@dataclass
class Event(JsonSerializableDataclass):
    """Represents an event in the events section of an Open Floor message envelope"""
    eventType: str
    to: Optional[To] = None
    reason: Optional[str] = None
    parameters: Parameters = field(default_factory=Parameters)

    def __post_init__(self):
        """Initialize after dataclass initialization"""
        if isinstance(self.parameters, dict):
            self.parameters = Parameters(self.parameters)

    def __iter__(self) -> Iterator[Tuple[str, Any]]:
        """Convert Event instance to JSON-compatible dictionary"""
        yield 'eventType', self.eventType
        if self.to is not None:
            yield 'to', dict(self.to)
        if self.reason is not None:
            yield 'reason', self.reason
        if self.parameters:
            yield 'parameters', dict(self.parameters)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Event':
        """Create an Event instance from a dictionary"""
        if 'to' in data:
            data['to'] = To.from_dict(data['to'])
        if 'parameters' in data and isinstance(data['parameters'], dict):
            data['parameters'] = Parameters(data['parameters'])
        return cls(**data)
    
@dataclass
class Envelope(JsonSerializableDataclass):
    """Represents the root Open Floor message envelope"""
    conversation: Conversation = field(default_factory=Conversation)
    sender: Sender = field(default_factory=Sender)
    schema: Schema = field(default_factory=Schema)
    events: List[Event] = field(default_factory=list)

    def __iter__(self) -> Iterator[Tuple[str, Any]]:
        """Convert OpenFloor instance to JSON-compatible dictionary"""
        yield 'schema', dict(self.schema)
        yield 'conversation', dict(self.conversation)
        yield 'sender', dict(self.sender)
        yield 'events', [dict(event) for event in self.events]

    def to_json(self, as_payload: bool = False, **kwargs) -> str:
        """Convert to JSON string, optionally wrapped in a payload"""
        if as_payload:
            return Payload(openFloor=self).to_json(**kwargs)
        return super().to_json(**kwargs)

    def to_file(self, filename: str, as_payload: bool = False, **kwargs) -> None:
        """Save to JSON file, optionally wrapped in a payload"""
        if as_payload:
            Payload(openFloor=self).to_file(filename, **kwargs)
        else:
            super().to_file(filename, **kwargs)

    @classmethod
    def from_json(cls, json_str: str, as_payload: bool = False, **kwargs) -> 'Envelope':
        """Create from JSON string, optionally unwrapped from a payload"""
        if as_payload:
            payload = Payload.from_json(json_str, **kwargs)
            return payload.openFloor
        return cls.from_dict(json.loads(json_str, **kwargs))

    @classmethod
    def from_file(cls, filename: str, as_payload: bool = False, **kwargs) -> 'Envelope':
        """Create from JSON file, optionally unwrapped from a payload"""
        if as_payload:
            payload = Payload.from_file(filename, **kwargs)
            return payload.openFloor
        with open(filename, 'r') as f:
            return cls.from_dict(json.load(f, **kwargs))

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Envelope':
        """Create an OpenFloor instance from a dictionary"""
        if 'schema' in data:
            data['schema'] = Schema.from_dict(data['schema'])
        if 'conversation' in data:
            data['conversation'] = Conversation.from_dict(data['conversation'])
        if 'sender' in data:
            data['sender'] = Sender.from_dict(data['sender'])
        if 'events' in data:
            data['events'] = [Event.from_dict(event) for event in data['events']]
        return cls(**data)

@dataclass
class Payload(JsonSerializableDataclass):
    """Represents a payload containing an Open Floor message envelope"""
    openFloor: Envelope

    def __iter__(self) -> Iterator[Tuple[str, Any]]:
        """Convert Payload instance to JSON-compatible dictionary"""
        yield 'openFloor', dict(self.openFloor)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Payload':
        """Create a Payload instance from a dictionary"""
        if 'openFloor' in data:
            data['openFloor'] = Envelope.from_dict(data['openFloor'])
        return cls(**data)
    
    

    
    
