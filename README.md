# openfloor

## Overview

The **Open-floor** specification enables human and autonomous agents to work together by gathering around a shared conversational 'floor' and engaging in conversation to solve shared problems or goals. It is entirely language, platform and framework independent.

The **Open-floor** specifications define a family of JSON structures that can be used to create the payload to send standard messages between agents and users. 

The Open-floor messaging standard has the following features:

- Open standard for inter-agent communication
- Multi-party (agent) conversation support
- Allows the mixing of simple and sophisticated conversational agents
- Symmetry between Users and Agents
- Extensible media type support
- Support for delegation, channeling, and mediation patterns
- Agent discovery capabilities

This `openfloor` python module provies rich set of classes from which dialog events and the message envelopes that contain them can be created, changed and saved. 

It can be used to aid the construction of any componens with produces or consumes standard Open Floor inter-agent messages.  This includes Open Floor user-proxy agents, floor managers, and autonomous agents.

## Installation

```bash
pip install openfloor
```

## Quick Tutorial

The `openfloor` library allows you to construct, interrogate and alter payloads that meet the Open-floor messaging standard.   It saves you from having to worry too much about the underlying JSON and provides a level of type-safety and checking.   If you use the library properly you should always be constructing payloads that meet the standard.

### Dialog Events

Media events such as utterances are represented in the openfloor standard as Dialog Events.  Dialog events can contain media with any mime type and can be broken into optional tokens and carry start and end-timing information.

Here's a simple example of creating a dialog event that represents an utterance. 

```python
from openfloor import TextFeature, DialogEvent

utterance=DialogEvent(
    speakerUri="tag:userproxy.com,2025:abc123",
    features={"text":TextFeature(values=["Hello, world!"])}
)
print(utterance.to_json(indent=4))
```
Which will generate the JSON for a dialog event as below.
```json
{
    "id": "de:7200e0e8-b3c0-459e-846d-c33ab9b0b8a6",
    "speakerUri": "tag:userproxy.com,2025:abc123",
    "span": {
        "startTime": "2025-05-08T18:20:45.550842"
    },
    "features": {
        "text": {
            "mimeType": "text/plain",
            "tokens": [
                {
                    "value": "Hello, world!"
                }
            ]
        }
    }
}
```
### Message Envelopes

#### Define the manifests

The openfloor standard uses a predefined format to carry information about conversants in a conversation.   These are called Manifests.

The Manifest is split into two parts, an `identification` section and a `capabilities` section.  The `identification` section is the part that is actually used in the envelope to carry information about conversants in the conversation but we will define a full manifest for our agent to show all the parts.

There is no difference between users and agents in the openfloor standard so we will define our user and our agent.  Remember that the standard can support multiple simulataneous users and agents conversing around the floor.

```
from openfloor.manifest import *

chat_agent_details = Manifest(
  identification = Identification(
    speakerUri="tag:dev.travelbot,2025:0001", 
    serviceUrl="https://dev.travelbot.ee/openfloor/conversation",
    organization="Travelbot Inc.",
    conversationalName="travelbot",
    department="Reservations and Customer Service",
    role="Reservation Specialist",
    synopsis="Reservation specialist as part of the Travelbot system."),
  capabilities = [
    Capability(
        keyphrases=["book","reserve","flight","hotel","car","cruise"], 
        descriptions=["book flights, hotels, cars, and cruises"], 
        languages=["en-us"],
        supportedLayers=SupportedLayers(input=["text"], output=["text"])
    ),
    Capability(
        keyphrases=["billing","payment","invoice","receipt"], 
        descriptions=["Respond to enquiries about billing, payments, and invoices"], 
        languages=["en-us"],
        supportedLayers=SupportedLayers(input=["text"], output=["text"])
    )
  ]
)

user_details = Manifest(
  Identification(
            conversationalName="John Doe",
            speakerUri="tag:userproxy.com,2025:abc123", 
            serviceUrl="https://userproxy.com",
            role="User"
        )
)
```

All objects in openfloor can be printed in JSON format. For example:

```
print(chat_agent_details.to_json(indent=2))
print(user_id_details.to_json(indent=2))
```

All objects in openfloor can also be created from JSON strings or from file.  For example:

```
chat_agent_details = Manifest.from_file("travelbot.json")
user_details = Manifest.from_file("john_doe.json")
```

We will use parts of the manifest to build the envelope.

#### Create an empty envelope

Messages that pass between agents are represented by Message Envelopes. `openfloor` provides a rich programmatic way to interact with these envelopes.

First we create an empty envelope. All envelopes must be assigned to a conversation and have a sender.  We will create an envelope from the user to be sent to the agent.  

The speakerUri is the primary identifier of a conversant and it is therefore needed to address who the envelope has come from.  It can be any string but we recommend choosing a URI as this is unique across the whole internet namespace.

We'll use the manifest from above to get the speakerUri.

```python
from openfloor import UtteranceEvent

conversation=Conversation()
sender=Sender(speakerUri=user_details.identification.speakerUri)
envelope=Envelope(conversation=conversation,sender=sender)

print(envelope.to_json(indent=2))
```

Which creates the following envelope:

```json
{
{
  "schema": {
    "version": "1.0.0"
  },
  "conversation": {
    "id": "conv:5d389c98-7eea-432a-833c-1e71e2b21fb8"
  },
  "sender": {
    "speakerUri": "tag:userproxy.com,2025:abc123"
  },
  "events": []
}
```
This is an empty envelope which are used to respond to a message if there is no need to send any events in return.

#### Add conversants to the envelope

Now lets use the manifests that we defined above to add a `conversant` section into the `conversation` to provide basic information about who is currently a participant in the conversation.

We use the Identification section of the manifest to define a conversant in the conversation record.

The conversant records can also optionally have a PersistentState defined which is a custom set of key value pairs that are supplied specially for stateless agents to perist their state between calls.  We add a simple example of a persistent state to the chate agent.

```python

chat_agent_persistent_state=PersistentState(
  conversationEnded=None,
  conversationActive=True,
  conversationPaused=False,
  conversationResumed=None
)
conversation.conversants.append(Conversant(user_details.identification))
conversation.conversants.append(Conversant(chat_agent_details.identification,persistentState=chat_agent_persistent_state))

print(conversation.to_json(indent=2))
```
This will give us the more substantial envelope containing the conversant information.

```json
{
  "schema": {
    "version": "1.0.0"
  },
  "conversation": {
    "id": "conv:6a62cbc9-5082-4935-837a-fdbbef562e1c",
    "conversants": [
      {
        "identification": {
          "speakerUri": "tag:userproxy.com,2025:abc123",
          "serviceUrl": "https://userproxy.com",
          "conversationalName": "John Doe",
          "role": "User"
        }
      },
      {
        "identification": {
          "speakerUri": "tag:dev.travelbot,2025:0001",
          "serviceUrl": "https://dev.travelbot.ee/openfloor/conversation",
          "organization": "Travelbot Inc.",
          "conversationalName": "travelbot",
          "department": "Reservations and Customer Service",
          "role": "Reservation Specialist",
          "synopsis": "Reservation specialist as part of the Travelbot system."
        },
        "persistentState": {
          "conversationEnded": null,
          "conversationActive": true,
          "conversationPaused": false,
          "conversationResumed": null
        }
      }
    ]
  },
  "sender": {
    "speakerUri": "tag:userproxy.com,2025:abc123"
  },
  "events": []
}
```

#### Add an Utterance to the Envelope

Now we can add the utterance that the user wants to send to the agent.  The UtteranceEvent contains a DialogEvent which carries the media for the utterance.

It may seems redundant to specify the speakerUri again in the DialogEvent but the openfloor messaging allows for conversants to pass on utterances abd media events generated by other conversants and maintain the original generator of the utterance.

So, in the following example we create an utterance to be spoken by the user that is sending the envelope with the same speakerUri.

```
from openfloor.envelope import *

utterance=DialogEvent(
  speakerUri=user_details.identification.speakerUri,
  features={"text":TextFeature(values=["Give me the times to Vancouver!"])}
  )
envelope.events.append(UtteranceEvent(dialogEvent=utterance))

print(envelope.to_json(indent=2))
```

The envelope now looks like this:

```json
{
  "schema": {
    "version": "1.0.0"
  },
  "conversation": {
    "id": "conv:296b03ef-569b-4c52-b436-6875ea63e4f6",
    "conversants": [
      {
        "identification": {
          "speakerUri": "tag:userproxy.com,2025:abc123",
          "serviceUrl": "https://userproxy.com",
          "conversationalName": "John Doe",
          "role": "User"
        }
      },
      {
        "identification": {
          "speakerUri": "tag:dev.travelbot,2025:0001",
          "serviceUrl": "https://dev.travelbot.ee/openfloor/conversation",
          "organization": "Travelbot Inc.",
          "conversationalName": "travelbot",
          "department": "Reservations and Customer Service",
          "role": "Reservation Specialist",
          "synopsis": "Reservation specialist as part of the Travelbot system."
        }
      }
    ]
  },
  "sender": {
    "speakerUri": "tag:userproxy.com,2025:abc123"
  },
  "events": [
    {
      "eventType": "utterance",
      "parameters": {
        "dialogEvent": {
          "id": "de:186e63aa-af22-4ece-82f1-d9794893b5f2",
          "speakerUri": "tag:userproxy.com,2025:abc123",
          "span": {
            "startTime": "2025-05-09T16:16:00.436444"
          },
          "features": {
            "text": {
              "mimeType": "text/plain",
              "tokens": [
                {
                  "value": "Give me the times to Vancouver!"
                }
              ]
            }
          }
        }
      }
    }
  ]
}
```

In a multi-party conversation, utterances can be directed to specific participants on the floor. Events can also me designated as 'private' indicating to the floor that they are intended for the designated particpant only.

For example the utterance above could have been defined as a private utterance meant specifically for the travelbot agent as below:

```
utterance=DialogEvent(
  speakerUri=user_details.identification.speakerUri,
  features={"text":TextFeature(values=["Give me the times to Vancouver!"])}
  )
envelope.events.append(
  UtteranceEvent(
    dialogEvent=utterance,
    to=To(
      speakerUri=chat_agent_details.identification.speakerUri,
      private=Ture
    )
  )
)
     
print(envelope.to_json(indent=2))
```

Which would lead to the utterance being re-defined to the following in the envelope.

```json
    ..
    {
      "eventType": "utterance",
      "to": {
        "speakerUri": "tag:dev.travelbot,2025:0001",
        "private": true
      },
      "parameters": {
        "dialogEvent": {
          "id": "de:29a268a4-5955-44b5-af53-f3d476c2f005",
          "speakerUri": "tag:userproxy.com,2025:abc123",
          "span": {
            "startTime": "2025-05-09T16:23:56.948646"
          },
          "features": {
            "text": {
              "mimeType": "text/plain",
              "tokens": [
                {
                  "value": "Give me the times to Vancouver!"
                }
              ]
            }
          }
        }
      }
    }
    ...
```

#### Adding Context and DialogHistory

We can also add a Context event to an envelope to provide context for the other events in the envelope.  ContextEvents have one standardized optional parameter `dialogHistory`. They can also have any number of additional arbitrary keys and contents.    

There is no limit to the number of Context Events that can be added to an envelope.

We show below how dialog history of the last for utterances could be added to the envelope.  Individual agents can choose exactly what they put into the dialog history or the floor manager could be used to maintain this a generic context event in all envelopes that cross the floor.

In this example we create the four utterances that make up the dialog history from JSON for brevity.

```python
from openfloor import *

dialog_history=DialogHistory()
dialog_history.append(DialogEvent.from_json('{"id": "event-1", "speakerUri": "tag:userproxy.com,2025:abc123", "span": {"startTime": "2024-03-14T12:00:00.000000"}, "features": {"text": {"mimeType": "text/plain", "tokens": [{"value": "hello"}]}}}'))
dialog_history.append(DialogEvent.from_json('{"id": "event-2", "speakerUri": "tag:dev.travelbot,2025:0001", "span": {"startTime": "2024-03-14T12:04:00.000000"}, "features": {"text": {"mimeType": "text/plain", "tokens": [{"value": "hello, how can i help you?"}]}}}'))
dialog_history.append(DialogEvent.from_json('{"id": "event-3", "speakerUri": "tag:userproxy.com,2025:abc123", "span": {"startTime": "2024-03-14T12:00:05.000000"}, "features": {"text": {"mimeType": "text/plain", "tokens": [{"value": "i need to book a flight"}]}}}'))
dialog_history.append(DialogEvent.from_json('{"id": "event-4", "speakerUri": "tag:dev.travelbot,2025:0001", "span": {"startTime": "2024-03-14T12:12:00.000000"}, "features": {"text": {"mimeType": "text/plain", "tokens": [{"value": "i can help you with that"}]}}}'))


context_event=ContextEvent(dialogHistory=dialog_history)
context_event.parameters["arbitrary_key"]="arbitrary_value"

envelope.events.append(context_event)

#print the envelope
print(envelope.to_json(indent=2))
```
This leaves us with our final envelope:

```json
{
  "schema": {
    "version": "1.0.0"
  },
  "conversation": {
    "id": "conv:8870e238-e42e-4332-9ba8-edb4d47faf54",
    "conversants": [
      {
        "identification": {
          "speakerUri": "tag:userproxy.com,2025:abc123",
          "serviceUrl": "https://userproxy.com",
          "conversationalName": "John Doe",
          "role": "User"
        }
      },
      {
        "identification": {
          "speakerUri": "tag:dev.travelbot,2025:0001",
          "serviceUrl": "https://dev.travelbot.ee/openfloor/conversation",
          "organization": "Travelbot Inc.",
          "conversationalName": "travelbot",
          "department": "Reservations and Customer Service",
          "role": "Reservation Specialist",
          "synopsis": "Reservation specialist as part of the Travelbot system."
        }
      }
    ]
  },
  "sender": {
    "speakerUri": "tag:userproxy.com,2025:abc123"
  },
  "events": [
    {
      "eventType": "utterance",
      "to": {
        "speakerUri": "tag:dev.travelbot,2025:0001",
        "private": true
      },
      "parameters": {
        "dialogEvent": {
          "id": "de:70b102e9-a3e9-4338-bb16-801d928eb8fd",
          "speakerUri": "tag:userproxy.com,2025:abc123",
          "span": {
            "startTime": "2025-05-09T16:38:30.562920"
          },
          "features": {
            "text": {
              "mimeType": "text/plain",
              "tokens": [
                {
                  "value": "Give me the times to Vancouver!"
                }
              ]
            }
          }
        }
      }
    },
    {
      "eventType": "context",
      "parameters": {
        "dialogHistory": [
          {
            "id": "event-1",
            "speakerUri": "tag:userproxy.com,2025:abc123",
            "span": {
              "startTime": "2025-05-09T16:38:30.576182"
            },
            "features": {
              "text": {
                "mimeType": "text/plain",
                "tokens": [
                  {
                    "value": "hello"
                  }
                ]
              }
            }
          },
          {
            "id": "event-2",
            "speakerUri": "tag:dev.travelbot,2025:0001",
            "span": {
              "startTime": "2025-05-09T16:38:30.576242"
            },
            "features": {
              "text": {
                "mimeType": "text/plain",
                "tokens": [
                  {
                    "value": "hello, how can i help you?"
                  }
                ]
              }
            }
          },
          {
            "id": "event-3",
            "speakerUri": "tag:userproxy.com,2025:abc123",
            "span": {
              "startTime": "2025-05-09T16:38:30.576280"
            },
            "features": {
              "text": {
                "mimeType": "text/plain",
                "tokens": [
                  {
                    "value": "i need to book a flight"
                  }
                ]
              }
            }
          },
          {
            "id": "event-4",
            "speakerUri": "tag:dev.travelbot,2025:0001",
            "span": {
              "startTime": "2025-05-09T16:38:30.576314"
            },
            "features": {
              "text": {
                "mimeType": "text/plain",
                "tokens": [
                  {
                    "value": "i can help you with that"
                  }
                ]
              }
            }
          }
        ],
        "arbitrary_key": "arbitrary_value"
      }
    }
  ]
}
```
## The Open Floor Standard

### Specifications

The openfloor standard is defined over an interconnected family of three specifications.  These are:

1. **[Open Floor Inter-Agent Message Specification Version 0.9.4](docs/AssistantManifestSpec.md)**

   - Defines the message envelope format for inter-agent communication
   - Specifies conversation management and event types
   - Supports multi-party conversations and agent discovery
   - Enables delegation, channeling, and mediation patterns

2. **[Interoperable Dialog Event Object Specification Version 1.0.2](docs/InteropDialogEventSpecs.md)**
   - Defines the format for dialog events within conversations
   - Supports multiple features (text, audio, etc.)
   - Includes time spans and token-based content
   - Enables cross-references between features
   - Supports multiple languages and custom feature types

3. **[Assistant Manifest Specification Version 0.9.2](docs/AssistantManifestSpec.md)**
   - Defines how agents describe their capabilities
   - Includes identification and supported layers
   - Enables agent discovery and capability matching
   - Supports multiple languages and keyphrases

These specifications work together to create a complete framework for interoperable conversational agents. The message specification provides the overall structure, the dialog event specification handles the content, and the manifest specification enables agent discovery and capability matching.

### Message Envelope Structure

The Open Floor message format uses a JSON structure that includes:

- Schema information
- Conversation details
- Sender information
- Events array

### Event Types

The library supports various event types:

- `UtteranceEvent`: For sending and receiving messages
- `ContextEvent`: For providing additional context
- `InviteEvent`: For inviting agents to join conversations
- `UninviteEvent`: For removing agents from conversations
- `DeclineInviteEvent`: For declining invitations
- `ByeEvent`: For leaving conversations
- `GetManifestsEvent`: For requesting agent manifests
- `PublishManifestsEvent`: For publishing agent manifests
- `RequestFloorEvent`: For requesting the conversational floor
- `GrantFloorEvent`: For granting the floor to an agent
- `RevokeFloorEvent`: For revoking the floor from an agent

### Dialog Events

Dialog events support:

- Multiple features (text, audio, etc.)
- Time spans
- Token-based content
- Confidence scores
- Cross-references between features
- Multiple languages
- Custom feature types

## Development

To set up the development environment:

```bash
# Clone the repository
git clone https://github.com/davidattwater/openfloor
cd openfloor

# Install development dependencies
pip install -e ".[dev]"
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the Apache License Version 2.0, - see the [LICENSE.txt](LICENSE.txt) file for details.

## Acknowledgments

This implementation is based on the Open Floor specification developed by the Open Voice Interoperability Initiative operating within the Linux Foundation AI & Data Foundation.