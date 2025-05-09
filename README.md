# openfloor



## Overview

The **Open-floor** specification enables human and autonomous agents to work together by gathering around a shared conversational 'floor' and engaging in conversation to solve shared problems or goals. It is entirely language, platform and framework independent.

The **Open-floor** specifications define a family of JSON structures that can be used to send standard messages between agents and users. 

The Open Floor messaging standard has the following features:

- Open standard for inter-agent communication
- Multi-party (agent) conversation support
- Allows the mixing of simple and sophisticated conversational agents
- Symmetry between Users and Agents
- Extensible media type support
- Support for delegation, channeling, and mediation patterns
- Agent discovery capabilities

This `openfloor` python module provies rich set of classes from which dialog events and the message envelopes that contain them can be created, changed and saved. 

It can be used to aid the construction of any componens with produces or consumes standard Open Floor inter-agent messages.  This includes Open Floor user-proxy agents, floor managers, and autonomous agents.

## Specifications

This implementation is based on three key specifications:

1. **Open Floor Inter-Agent Message Specification**
   - Defines the message envelope format for inter-agent communication
   - Specifies conversation management and event types
   - Supports multi-party conversations and agent discovery
   - Enables delegation, channeling, and mediation patterns

2. **Interoperable Dialog Event Specification**
   - Defines the format for dialog events within conversations
   - Supports multiple features (text, audio, etc.)
   - Includes time spans and token-based content
   - Enables cross-references between features
   - Supports multiple languages and custom feature types

3. **Assistant Manifest Specification**
   - Defines how agents describe their capabilities
   - Includes identification and supported layers
   - Enables agent discovery and capability matching
   - Supports multiple languages and keyphrases

These specifications work together to create a complete framework for interoperable conversational agents. The message specification provides the overall structure, the dialog event specification handles the content, and the manifest specification enables agent discovery and capability matching.

## Installation

```bash
pip install openfloor
```

## Quick Start

### Dialog Events
Media events such as utterances are represented in the openfloor standard as Dialog Events.  Dialog events can contain media with any mime type and can be broken into optional tokens and carry start and end-timing information.

Here's a simple example of creating a dialog event that represents an utterance. 

```python
from openfloor import TextFeature, DialogEvent

utterance=DialogEvent(
    id="1",
    speakerUri="tag:userproxy.com,2025:abc123",
    features={"text":TextFeature(values=["Hello, world!"])}
)
print(utterance.to_json(indent=4))
```
Which will generate the JSON for a dialog event as below.
```json
{
    "id": "1",
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

Messages that pass between agents are represented by Message Envelopes. `openfloor` provides a rich programmatic way to interact with these envelopes.

Here's an example of the creation of a minimal message envelope containing a single utterance event which contains the same dialog-event as the above example.

```python
from openfloor.envelope import *

envelope=Envelope(
    conversation=Conversation(id="1234567890"),
    sender=Sender(
        speakerUri="tag:userproxy.com,2025:abc123", 
        serviceUrl="https://userproxy.com"
    )
    events=[
        UtteranceEvent(
            
        )
    ]
utterance=DialogEvent(

    id="123456",
    speakerUri="tag:userproxy.com,2025:abc123",
    features={"text":TextFeature(values=["Hello, world!"])},

(conversation=conversation, sender=sender, events=[utterance])

print(envelope.to_json(indent=2))
```

Which creates the following envelope:

```json
{
  "schema": {
    "version": "1.0.0"
  },
  "conversation": {
    "id": "1234567890"
  },
  "sender": {
    "speakerUri": "tag:userproxy.com,2025:abc123",
    "serviceUrl": "https://userproxy.com"
  },
  "events": [
    {
      "id": "1",
      "speakerUri": "tag:userproxy.com,2025:abc123",
      "span": {
        "startTime": "2025-05-08T18:38:43.256158"
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
  ]
}
```

Files and dictionaries can be converted to dictionaries, json strings or saved to file.  They can also be used to instantiate any class representing any part of an envelope.  All of the envelopes created by the following code will have the same contents.

```python
#Convert to dict (i.e. python object containing simple JSON equivalent types)
dict1=dict(envelope)

#Convert to JSON string
json1=envelope.to_json(indent=2)

#Save as JSON
envelope.to_file("envelope1.json",indent=2)

#Create from dictionary
envelope_from_dict=Envelope.from_dict(dict1)

#Create from JSON string
envelope_from_dict=Envelope.from_json(json1)

#Create from JSON file
envelope_from_dict=Envelope.from_file("envelope1.json")
```

## Key Features

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
git clone https://github.com/yourusername/openfloor.git
cd openfloor

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

This implementation is based on the Open Floor specification developed by the Open Voice Interoperability Initiative operating within the Linux Foundation AI & Data Foundation.