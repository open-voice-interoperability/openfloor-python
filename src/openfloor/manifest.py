from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Iterator, Tuple
from .json_serializable import JsonSerializableDict

@dataclass
class Identification(JsonSerializableDict):
    """Represents the identification section of a conversant"""
    speakerUri: str
    serviceUrl: str
    organization: Optional[str] = None
    conversationalName: Optional[str] = None
    department: Optional[str] = None
    role: Optional[str] = None
    synopsis: Optional[str] = None

    def __iter__(self) -> Iterator[Tuple[str, Any]]:
        """Convert Identification instance to JSON-compatible dictionary"""
        yield 'speakerUri', self.speakerUri
        yield 'serviceUrl', self.serviceUrl
        if self.organization is not None:
            yield 'organization', self.organization
        if self.conversationalName is not None:
            yield 'conversationalName', self.conversationalName
        if self.department is not None:
            yield 'department', self.department
        if self.role is not None:
            yield 'role', self.role
        if self.synopsis is not None:
            yield 'synopsis', self.synopsis
    
    def __post_init__(self):
        if self.speakerUri is None:
            raise ValueError("speakerUri is required to create an instance of the Identification class")
        if self.serviceUrl is None:
            raise ValueError("serviceUrl is required to create an instance of the Identification class")

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Identification':
        """Create an Identification instance from a dictionary"""
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