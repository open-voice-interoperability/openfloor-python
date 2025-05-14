from typing import Optional, List, Tuple, Dict
import events as events_module
from abc import ABC, abstractmethod
from openfloor import Parameters, DialogEvent, TextFeature, To, Sender, Manifest, Conversation, Envelope, Event, InviteEvent, UtteranceEvent, ContextEvent, UninviteEvent, DeclineInviteEvent, ByeEvent, GetManifestsEvent, PublishManifestsEvent, RequestFloorEvent, GrantFloorEvent, RevokeFloorEvent

class OpenFloorEvents(events_module.Events):
    """Base class for Open Floor agents that defines event handlers"""
    __events__ = (
        'on_envelope',
        'on_utterance', 
        'on_context', 
        'on_invite', 
        'on_uninvite', 
        'on_decline_invite', 
        'on_bye', 
        'on_get_manifests', 
        'on_publish_manifests', 
        'on_request_floor', 
        'on_grant_floor', 
        'on_revoke_floor',
        "on_yield_floor"
    )

class OpenFloorAgent(OpenFloorEvents):

    _manifest : Optional[Manifest] = None

    def __init__(self, manifest: Manifest):
        super().__init__()
        self._manifest = manifest

    @property
    def speakerUri(self) -> str:
        """A convenient shorthand to get the speakerUri from the manifest"""
        return self._manifest.identification.speakerUri
    
    @property
    def serviceUrl(self) -> str:
        """A convenient shorthand to get the serviceUrl from the manifest"""
        return self._manifest.identification.serviceUrl

    def add_metadata(self, events: List[Event]) -> List[Tuple[Event, Dict[str, bool]]]:
        """Split events into those intended for this agent and those for other agents
        
        Args:
            events: List of events to split
            
        Returns:
            List of tuples (event, metadata) where:
            - event: The original event
            - metadata: Dictionary containing:
                - addressed_to_me: Boolean indicating if event is intended for this agent
        """
        result = []
        #Add from speakerUri to each event
        for event in events:
            result.append((
                event, 
                {
                    "addressed_to_me": (
                        event.to is None or 
                        event.to.speakerUri == self._manifest.identification.speakerUri or
                        event.to.serviceUrl == self._manifest.identification.serviceUrl
                    )
                }
            ))
                
        return result

class BotAgent(OpenFloorAgent):    
    """
    BotAgent is a simple bot agent.  It can be used as a class in its own right or subclassed to create more complex agents.
    
    The class provides default event handlers that meet the Open Floor specification
    requirements for a bot agent. 
    
    The default on_envelope handler processes events in a specific order, checking for invite events first if the bot is not already in
    a conversation.
    
    Event handlers can be customized by subclassing and overriding the default handlers.
    
    For a minimal implementation, all that is required is the following
    - Implement a handler for invite events to send a greeting
    - Implement a handler for bye events to send a farewell
    - Implement a handler for utterance events to handle conversation
    """

    _current_context : List[ContextEvent] = []
    _active_conversation : Optional[Conversation] = None    
    _has_floor : bool = False

    def __init__(self, manifest: Manifest):
        super().__init__(manifest)
        self._active_conversation = None
        self._has_floor = False
        self._current_context = []
        self.__attach_handlers__()

    def __attach_handlers__(self):
        # Register all handlers with the event system
        self.on_envelope += self.bot_on_envelope
        self.on_invite += self.bot_on_invite
        self.on_utterance += self.bot_on_utterance
        self.on_context += self.bot_on_context
        self.on_uninvite += self.bot_on_uninvite
        self.on_grant_floor += self.bot_on_grant_floor
        self.on_revoke_floor += self.bot_on_revoke_floor
        self.on_get_manifests += self.bot_on_get_manifests
        
        print(f"registered handlers: {len(self)}")
        
        """
        The following events are not handled because according the spec they can be ignored by a simple bot agent.
        self.on_bye
        self.on_decline_invite  
        self.on_yield_floor  
        self.on_publish_manifests  
        self.on_request_floor  
        """
        
        # Map event types to their handler functions
        self._event_type_to_handler = {
            "invite": self.on_invite,
            "utterance": self.on_utterance,
            "context": self.on_context,
            "uninvite": self.on_uninvite,
            "declineInvite": self.on_decline_invite,
            "bye": self.on_bye,
            "getManifests": self.on_get_manifests,
            "publishManifests": self.on_publish_manifests,
            "requestFloor": self.on_request_floor,
            "grantFloor": self.on_grant_floor,
            "revokeFloor": self.on_revoke_floor,
            "yieldFloor": self.on_yield_floor
        }

    def process_envelope(self, in_envelope: Envelope) -> Envelope:
        #Create an empty response envelope. use the conversation from the input envelope and set the sender from the manifest.  
        out_envelope=Envelope(
            conversation=in_envelope.conversation,
            sender=Sender(
                speakerUri=self.speakerUri,
                serviceUrl=self.serviceUrl
            )
        )

        self.on_envelope(in_envelope, out_envelope)
        return out_envelope

    def bot_on_envelope(self, in_envelope: Envelope, out_envelope: Envelope) -> Envelope:
        print("Entering bot_on_envelope")
        #clear the current context
        self._current_context = []
        
        #If we are already in a different conversation then raise an exception. This is a situation that simple agents should not allow.
        print(f"self._active_conversation: {self._active_conversation}")
        print(f"in_envelope.conversation.id: {in_envelope.conversation.id}")    
        
        if (self._active_conversation is not None and self._active_conversation.id != in_envelope.conversation.id):
            raise Exception("Bot is already in a different conversation.  Cannot accept invite to a different conversation.")

        """Remove any events that are not intended for this agent"""
        events_with_metadata = self.add_metadata(in_envelope.events)
        my_events_with_metadata = [[event,metadata] for event, metadata in events_with_metadata if metadata["addressed_to_me"]]

        #Process the remaining events in order
        for event,metadata in my_events_with_metadata:
            print(f"Processing event: {event.to_json()}")
            print(f"Processing event with type: {event.eventType}")
            
            handler = self._event_type_to_handler.get(event.eventType)
            if handler is None:
                raise ValueError(f"Unknown event type: {event.eventType}")
            handler(event, in_envelope, out_envelope)
        
        print(f"out_envelope: {out_envelope.to_json()}")
        
        return out_envelope

    def bot_on_invite(self, event: InviteEvent, in_envelope: Envelope, out_envelope: Envelope) -> None:
        print("Entering bot_on_invite")
       
        #Accept the invitation
        self._active_conversation = Conversation(id=in_envelope.conversation.id)
        
        #automatically treat this as if the inviting agent had also granted the floor. (This is default behavior according to the spec)
        self.bot_on_grant_floor(
            GrantFloorEvent(
                to=To(speakerUri=self._manifest.identification.speakerUri),
                reason="Automatic floor grant as a result of the invitation"
            ),
            in_envelope,
            out_envelope
        )

    def bot_on_grant_floor(self, event: GrantFloorEvent, in_envelope: Envelope, out_envelope: Envelope) -> None:
        print("Entering bot_on_grant_floor")
        self._has_floor = True

    def bot_on_revoke_floor(self, event: RevokeFloorEvent, in_envelope: Envelope, out_envelope: Envelope) -> None:
        print("Entering bot_on_revoke_floor")
        self._has_floor = False

    def bot_on_utterance(self, event: UtteranceEvent, in_envelope: Envelope, out_envelope: Envelope) -> None:
        print("Entering bot_on_utterance")
        utterance=DialogEvent(
            speakerUri=self._manifest.identification.speakerUri,
            features={"text":TextFeature(values=["Sorry! I'm a simple bot that has not been programmed to do anything yet."])},
        )
        out_envelope.events.append(UtteranceEvent(dialogEvent=utterance))

    def bot_on_context(self, event: ContextEvent, in_envelope: Envelope, out_envelope: Envelope) -> None:
        print("Entering bot_on_context")
        self._current_context.append(event)

    def bot_on_uninvite(self, event: UninviteEvent, in_envelope: Envelope, out_envelope: Envelope) -> None:
        print("Entering bot_on_uninvite")
        self._active_conversation = None  

    def bot_on_get_manifests(self, event: GetManifestsEvent, in_envelope: Envelope, out_envelope: Envelope) -> None:
        print("Entering bot_on_get_manifests")
        out_envelope.events.append(
            PublishManifestsEvent(
                Parameters=Parameters(
                    manifests={"servicingManifests" : [self._manifest], "discoveryManifests" : []}
                )
            )
        )




