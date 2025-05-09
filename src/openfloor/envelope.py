from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Iterator, Tuple
from datetime import datetime
from .json_serializable import JsonSerializableDict, JsonSerializableList
from .manifest import Identification
from .dialog_event import DialogHistory
import uuid

@dataclass
class Schema(JsonSerializableDict):
    """Represents the schema section of an Open Floor message envelope"""
    version: str = "1.0.0"
    url: Optional[str] = None

    def __iter__(self) -> Iterator[Tuple[str, Any]]:
        """Convert Schema instance to JSON-compatible dictionary"""
        yield 'version', self.version
        if self.url is not None:
            yield 'url', self.url

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Schema':
        """Create a Schema instance from a dictionary"""
        return cls(**data)
    
    def __post_init__(self):
        if self.version is None:
            self.version="1.0.0"

@dataclass
class Conversant(JsonSerializableDict):
    """Represents a conversant in the conversation"""
    identification: Identification
    persistentState: Dict[str, Any] = field(default_factory=dict)

    def __iter__(self) -> Iterator[Tuple[str, Any]]:
        """Convert Conversant instance to JSON-compatible dictionary"""
        yield 'identification', dict(self.identification)
        if self.persistentState:
            yield 'persistentState', self.persistentState

    def __post_init__(self):
        if self.identification is None:
            raise ValueError("identification is required for the Conversant")

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Conversant':
        """Create a Conversant instance from a dictionary"""
        if 'identification' in data:
            data['identification'] = Identification.from_dict(data['identification'])
        return cls(**data)

@dataclass
class Conversation(JsonSerializableDict):
    """Represents the conversation section of an Open Floor message envelope"""
    id: Optional[str] = None
    conversants: List[Conversant] = field(default_factory=list)

    def __post_init__(self):
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
class Sender(JsonSerializableDict):
    """Represents the sender section of an Open Floor message envelope"""
    speakerUri: str
    serviceUrl: Optional[str] = None

    def __iter__(self) -> Iterator[Tuple[str, Any]]:
        """Convert Sender instance to JSON-compatible dictionary"""
        yield 'speakerUri', self.speakerUri
        if self.serviceUrl is not None:
            yield 'serviceUrl', self.serviceUrl

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Sender':
        """Create a Sender instance from a dictionary"""
        return cls(**data)

@dataclass
class To(JsonSerializableDict):
    """Represents the 'to' section of an event"""
    speakerUri: Optional[str] = None
    serviceUrl: Optional[str] = None
    private: bool = False

    def __post_init__(self):
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

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'To':
        """Create a To instance from a dictionary"""
        return cls(**data)

@dataclass
class Parameters(JsonSerializableDict):
    """Represents a dictionary of parameters that can be serialized to JSON"""
    def __init__(self, *args, **kwargs):
        self._data = {}
        if args and isinstance(args[0], dict):
            self._data.update(args[0])
        self._data.update(kwargs)

@dataclass
class Event(JsonSerializableDict):
    """Represents an event in the events section of an Open Floor message envelope"""
    eventType: str
    to: Optional[To] = None
    reason: Optional[str] = None
    parameters: Parameters = field(default_factory=Parameters)

    def __post_init__(self):
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
class Envelope(JsonSerializableDict):
    """Represents the root Open Floor message envelope"""
    conversation: Conversation
    sender: Sender
    schema: Schema = field(default_factory=Schema)
    events: List[Event] = field(default_factory=list)

    def __iter__(self) -> Iterator[Tuple[str, Any]]:
        """Convert OpenFloor instance to JSON-compatible dictionary"""
        yield 'schema', dict(self.schema)
        yield 'conversation', dict(self.conversation)
        yield 'sender', dict(self.sender)
        if self.events:
            yield 'events', [dict(event) for event in self.events]

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
class SupportedLayers(JsonSerializableDict):
    """Represents the supported input and output layers for a capability"""
    input: List[str] = field(default_factory=lambda: ["text"])
    output: List[str] = field(default_factory=lambda: ["text"])

    def __iter__(self) -> Iterator[Tuple[str, Any]]:
        """Convert SupportedLayers instance to JSON-compatible dictionary"""
        yield 'input', self.input
        yield 'output', self.output

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SupportedLayers':
        """Create a SupportedLayers instance from a dictionary"""
        return cls(**data)

@dataclass
class Capability(JsonSerializableDict):
    """Represents a single capability in the capabilities array"""
    keyphrases: List[str]
    descriptions: List[str]
    languages: Optional[List[str]] = None
    supportedLayers: Optional[SupportedLayers] = None

    def __post_init__(self):
        if self.supportedLayers is None:
            self.supportedLayers = SupportedLayers()

    def __iter__(self) -> Iterator[Tuple[str, Any]]:
        """Convert Capability instance to JSON-compatible dictionary"""
        yield 'keyphrases', self.keyphrases
        yield 'descriptions', self.descriptions
        if self.languages is not None:
            yield 'languages', self.languages
        if self.supportedLayers is not None:
            yield 'supportedLayers', dict(self.supportedLayers)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Capability':
        """Create a Capability instance from a dictionary"""
        if 'supportedLayers' in data:
            data['supportedLayers'] = SupportedLayers.from_dict(data['supportedLayers'])
        return cls(**data)

@dataclass
class Manifest(JsonSerializableDict):
    """Represents an Assistant Manifest according to the specification"""
    identification: Identification
    capabilities: List[Capability]

    def __iter__(self) -> Iterator[Tuple[str, Any]]:
        """Convert Manifest instance to JSON-compatible dictionary"""
        yield 'identification', dict(self.identification)
        yield 'capabilities', [dict(capability) for capability in self.capabilities]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Manifest':
        """Create a Manifest instance from a dictionary"""
        if 'identification' in data:
            data['identification'] = Identification.from_dict(data['identification'])
        if 'capabilities' in data:
            data['capabilities'] = [Capability.from_dict(cap) for cap in data['capabilities']]
        return cls(**data) 
    
