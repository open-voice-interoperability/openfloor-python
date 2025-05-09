from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Iterator, Tuple
from .envelope import Event, To, Parameters
from .dialog_event import DialogEvent, DialogHistory
from .json_serializable import JsonSerializableDict

@dataclass
class UtteranceEvent(Event):
    """Represents an utterance event in the conversation"""
    eventType: str = "utterance"
    dialogEvent: Optional[DialogEvent] = field(default=None, repr=False)
    parameters: Parameters = field(default_factory=Parameters)

    def __post_init__(self):
        """Initialize after dataclass initialization"""
        if self.dialogEvent is not None:
            self.parameters["dialogEvent"] = self.dialogEvent
        if "dialogEvent" not in self.parameters or not isinstance(self.parameters["dialogEvent"], DialogEvent):
            raise ValueError("UtteranceEvent must contain a dialogEvent parameter")

    def __iter__(self) -> Iterator[Tuple[str, Any]]:
        """Convert UtteranceEvent instance to JSON-compatible dictionary"""
        yield 'eventType', self.eventType
        if self.to is not None:
            yield 'to', dict(self.to)
        if self.reason is not None:
            yield 'reason', self.reason
        if self.parameters:
            yield 'parameters', dict(self.parameters)

@dataclass
class ContextEvent(Event):
    """Represents a context event providing additional information to recipient agents"""
    eventType: str = "context"
    dialogHistory: Optional[DialogHistory] = field(default=None, repr=False)
    parameters: Parameters = field(default_factory=lambda: Parameters(dialogHistory=None))

    def __post_init__(self):
        if self.dialogHistory is not None:
            self.parameters["dialogHistory"] = self.dialogHistory
        if "dialogHistory" not in self.parameters or not isinstance(self.parameters["dialogHistory"], DialogHistory):
            self.parameters["dialogHistory"] = DialogHistory()

    def __iter__(self) -> Iterator[Tuple[str, Any]]:
        """Convert ContextEvent instance to JSON-compatible dictionary"""
        yield 'eventType', self.eventType
        if self.to is not None:
            yield 'to', dict(self.to)
        if self.reason is not None:
            yield 'reason', self.reason
        if self.parameters:
            yield 'parameters', dict(self.parameters)

@dataclass
class InviteEvent(Event):
    """Represents an invitation for an agent to join the conversation"""
    eventType: str = "invite"

@dataclass
class UninviteEvent(Event):
    """Represents removing an agent from the conversation"""
    eventType: str = "uninvite"

@dataclass
class DeclineInviteEvent(Event):
    """Represents declining an invitation to join the conversation"""
    eventType: str = "declineInvite"

@dataclass
class ByeEvent(Event):
    """Represents an agent leaving the conversation"""
    eventType: str = "bye"
    parameters: Parameters = field(default_factory=Parameters)

@dataclass
class GetManifestsEvent(Event):
    """Represents a request for agent manifests"""
    eventType: str = "getManifests"
    parameters: Parameters = field(default_factory=lambda: Parameters({
        "recommendScope": "internal"  # Can be "external", "internal", or "all"
    }))

@dataclass
class PublishManifestsEvent(Event):
    """Represents publishing agent manifests"""
    eventType: str = "publishManifests"
    parameters: Parameters = field(default_factory=lambda: Parameters({
        "servicingManifests": [],
        "discoveryManifests": []
    }))

@dataclass
class RequestFloorEvent(Event):
    """Represents a request for the conversational floor"""
    eventType: str = "requestFloor"

@dataclass
class GrantFloorEvent(Event):
    """Represents granting the conversational floor to an agent"""
    eventType: str = "grantFloor"

@dataclass
class RevokeFloorEvent(Event):
    """Represents revoking the conversational floor from an agent"""
    eventType: str = "revokeFloor" 