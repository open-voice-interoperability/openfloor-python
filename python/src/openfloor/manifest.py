from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Iterator, Tuple
from .json_serializable import JsonSerializableDict, JsonSerializableDataclass

@dataclass
class Identification(JsonSerializableDataclass):
    """Represents the identification section of a conversant"""
    speakerUri: str
    serviceUrl: str
    organization: str
    conversationalName: str
    synopsis: str
    department: Optional[str] = None
    role: Optional[str] = None
    openFloorRoles: Optional[Dict[str, bool]] = None

    def __post_init__(self):
        """Initialize after dataclass initialization"""
        if self.speakerUri is None:
            raise ValueError("speakerUri is required to create an instance of the Identification class")
        if self.serviceUrl is None:
            raise ValueError("serviceUrl is required to create an instance of the Identification class")
        if self.organization is None:
            raise ValueError("organization is required to create an instance of the Identification class")
        if self.conversationalName is None:
            raise ValueError("conversationalName is required to create an instance of the Identification class")
        if self.synopsis is None:
            raise ValueError("synopsis is required to create an instance of the Identification class")

    def __iter__(self) -> Iterator[Tuple[str, Any]]:
        """Convert Identification instance to JSON-compatible dictionary"""
        yield 'speakerUri', self.speakerUri
        yield 'serviceUrl', self.serviceUrl
        yield 'organization', self.organization
        yield 'conversationalName', self.conversationalName
        yield 'synopsis', self.synopsis
        if self.department is not None:
            yield 'department', self.department
        if self.role is not None:
            yield 'role', self.role
        if self.openFloorRoles is not None:
            yield 'openFloorRoles', self.openFloorRoles

@dataclass
class SupportedLayers(JsonSerializableDataclass):
    """Represents the supported input and output layers for a capability"""
    input: List[str] = field(default_factory=lambda: ["text"])
    output: List[str] = field(default_factory=lambda: ["text"])

    def __iter__(self) -> Iterator[Tuple[str, Any]]:
        """Convert SupportedLayers instance to JSON-compatible dictionary"""
        yield 'input', self.input
        yield 'output', self.output

@dataclass
class Capability(JsonSerializableDataclass):
    """Represents a single capability in the capabilities array"""
    keyphrases: List[str]
    descriptions: List[str]
    languages: Optional[List[str]] = None
    supportedLayers: Optional[SupportedLayers] = None

    def __post_init__(self):
        """Initialize after dataclass initialization"""
        if self.supportedLayers is None:
            self.supportedLayers = SupportedLayers()

    def __iter__(self) -> Iterator[Tuple[str, Any]]:
        """Convert Capability instance to JSON-compatible dictionary"""
        yield 'keyphrases', self.keyphrases
        yield 'descriptions', self.descriptions
        if self.languages is not None:
            yield 'languages', self.languages
        if self.supportedLayers is not None:
            yield 'supportedLayers', self.supportedLayers.__json__()

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Capability':
        """Create a Capability instance from a dictionary"""
        if 'supportedLayers' in data:
            data['supportedLayers'] = SupportedLayers.from_dict(data['supportedLayers'])
        return super().from_dict(data)

@dataclass
class Manifest(JsonSerializableDataclass):
    """Represents an Assistant Manifest according to the specification"""
    identification: Identification
    capabilities: List[Capability] = field(default_factory=list)

    def __iter__(self) -> Iterator[Tuple[str, Any]]:
        """Convert Manifest instance to JSON-compatible dictionary"""
        yield 'identification', self.identification.__json__()
        yield 'capabilities', [capability.__json__() for capability in self.capabilities]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Manifest':
        """Create a Manifest instance from a dictionary"""
        if 'identification' in data:
            data['identification'] = Identification.from_dict(data['identification'])
        if 'capabilities' in data:
            data['capabilities'] = [Capability.from_dict(cap) for cap in data['capabilities']]
        return super().from_dict(data)