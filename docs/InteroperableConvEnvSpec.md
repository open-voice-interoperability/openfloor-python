<img src="https://github.com/open-voice-interoperability/artwork/blob/main/horizontal/color/Interoperability_Logo_color.png" width="200">

# Open Floor Inter-Agent Message Specification Version 1.1.0

**The Open Floor Project**\
**Open Voice Interoperability Initiative - LF AI & Data Foundation**

**RELEASED** \
**Version 1.1.0**

*_Editor-in-Chief: David Attwater_*\
*_Contributors: Leah Barnes, Csaba Bolyós, Emmett Coin,  Deborah Dahl, Diego Gosmar, Jim Larson, Rainer Türner, Dirk Schnelle-Walka, Allan Wylie, Andreas Zettl_*

## TABLE OF CONTENTS
- [0 SCOPE AND INTRODUCTION](#0-SCOPE-AND-INTRODUCTION)
  - [0.1 Document Scope](#01-Document-Scope)
  - [0.2 Open-Floor Message Envelopes](#02-Open-Floor-Message-Envelopes)
  - [0.3 Delegation, Channeling and Mediation](#03-Delegation-Channeling-and-Mediation)
  - [0.4 Multi-Party Conversations](#04-Multi-Party-Conversations)
  - [0.5 Discovery](#05-Discovery)
  - [0.6 Agent Identity](#06-Agent-Identity)
- [1 SPECIFICATION](#1-SPECIFICATION)
  - [1.1 Syntax and Protocol](#11-Syntax-and-Protocol)
  - [1.2 AAA & Security](#12-AAA--Security)
  - [1.3 Nomenclature](#13-Nomenclature)
  - [1.4 Message Envelope Structure](#14-Message-Envelope-Structure)
  - [1.5 Schema Object](#15-Schema-Object)
  - [1.6 Conversation Object](#16-Conversation-Object)
  - [1.7 Sender Object](#17-Sender-Object)
  - [1.8 Events Object](#18-Events-Object)
  - [1.9 Event-Types](#19-Event-Types)
  - [1.10 Utterance Events](#110-Utterance-Events)
  - [1.10.1 dialogEvent Text Feature](#1101-dialogEvent-Text-Feature)
  - [1.11 Extensible Dialog Event Features](#111-Extensible-Dialog-Event-Features)
  - [1.12 invite Event](#112-invite-Event)
  - [1.13 uninvite Event](#113-uninvite-Event)
  - [1.14 acceptInvite Event](#114-acceptInvite-Event)
  - [1.15 declineInvite Event](#115-declineInvite-Event)
  - [1.16 bye Event](#116-bye-Event)
  - [1.17 getManifests Event](#117-getManifests-Event)
  - [1.18 publishManifests Event](#118-publishManifests-Event)
  - [1.19 requestFloor Event](#119-requestFloor-Event)
  - [1.20 grantFloor Event](#120-grantFloor-Event)
  - [1.21 revokeFloor Event](#121-revokeFloor-Event)
  - [1.22 yieldFloor Event](#122-yieldFloor-Event)
- [2 Minimal Behaviors](#2-Minimal-Behaviors)
  - [2.1 Minimal Servicing Assistant Behaviors (on Receipt of Events)](#21-Minimal-Servicing-Assistant-Behaviors-on-Receipt-of-Events)
  - [2.2 Minimal Conversation Floor Manager Behaviors (on Receipt of Events)](#22-Minimal-Conversation-Floor-Manager-Behaviors-on-Receipt-of-Events)
  - [2.3 Ignoring events with protocols that require a response](#23-Ignoring-events-with-protocols-that-require-a-response)
- [3 JSON Envelope Schema](#3-JSON-Envelope-Schema)
- [4 References](#4-References)
- [5 Glossary of Terms](#5-Glossary-of-Terms)
- [6 Decision Log](#6-Decision-Log)
- [7 Document Change Log](#7-Document-Change-Log)

*****
### 0 SCOPE AND INTRODUCTION
#### 0.1 Document Scope
This document specifies the "Open-Floor" Inter-Agent Message Specification, developed by the Open Voice Interoperability Initiative operating within the Linux Foundation AI & Data Foundation.  The purpose of this open messaging standard is to enable human and autonomous agents to work together by gathering around a shared conversational 'floor' and engage in conversation to solve a shared problem or goal.

The standard differs from other inter-agent frameworks in the following ways:

- Uses multi-party conversation as the model for inter-agent co-operation
- Open standard that can allow inter-working between agents in different technology stacks
- Symmetry between Users and Agents allowing humans and AIs to collaborate to solve problems
- Extensible to new media types 

The user stories upon which this specification is based can be found in the white paper - Interoperability of Conversational Assistants [1].  

#### 0.2 Open-Floor Message Envelopes
The Open-Floor Message format is a universal JSON structure whose purpose is to allow human or automatic agents (assistants) to interoperably participate in a conversation.  When coupled with a specific protocol, such as HTTPS (See section 1.2), a conversational agent that can generate and send Message Envelopes is capable of inter-operating with any other Open-Floor compliant agent, regardless of the technology or architecture on which that other agent is based.


<img width="510" alt="Simple Open-Floor Agent Example" src="simple-configuration.png">

Collaboration between agents and human users is modelled upon a conversation between peers gathering around a shared 'floor'.  As with normal human-human conversation, agents (users or conversational assistants) communicate with each other by exchanging 'utterances'.  In many ways the 'floor' is analogous to a  conference bridge that joins participants in a conversation.  Also, as with normal conversation, the participants in the conversation collaborate to achieve a goal together. In some cases a convener agent may also be present to mediate the conversation on the floor in a manner analogous to a chair moderating a meeting.

A conversation can consist of multiple conversants, who may be any arbitrary mixture of human or autonomous agents.  The simplicity of the interface means that the messages can also be used as a platform independent interface between a chat client and AI chat agents.

Figure 1 shows a simple schematic showing a user interacting at various points with three Open-floor compliant dialog assistants, via a user proxy agent, and a conversation floor manager.  Let's assume for now that there is a single user who remains constant for the duration of the conversation.  This user engages with a number of dialog agents, one at a time,  during the course of the conversation in a sequential manner.

The proxy agent acts as a media gateway with the user - converting whatever media interface the user is interacting with into standard interoperable messaging. The conversational floor manager acts as a hub to coordinate the conversation.

In the example shown in Figure 1, the user proxy agent and the conversation manager can be combined.   This combined function is termed an 'Open-Floor Compliant Host Browser'.

In its simplest form, the user proxy agent might present a text-based chat interface to the user.  For spoken interaction, the proxy agent will likely also contain speech-to-text and text-to-speech facilities but other configurations are also anticipated including support for images, video and document attachments.  The proxy agent may have conversational ability in its own right but in many cases, it may only provide rudimentary capabilities such as wake-word detection.

Messages that pass between Open-floor agents are termed 'conversation envelopes'.  Each arrow in the diagram denotes a message passing from one agent to another.  Each of these messages will comprise a single message envelope.   Each conversant can 'hear' things said to it or 'say' things by making an 'utterance'.   They can also 'whisper' to each other behind the scenes by sending private utterances to each other.   Conversants may also invite other agents to join the conversation or they might ask other agents if they are capable of a certain activity or would like recommend another agent for a certain task.

#### 0.3 Delegation, Channeling and Mediation

The floor manager is in control of which conversants are engaged in a conversation at any given moment.

To start a conversation, the proxy agent invites a specific dialog agent (e.g. Dialog Assistant A) to take part in a conversation with the user.   Once engaged, the assistant receives an open-floor message containing a user utterance and sends an utterance back to the user in response.  Once the assistant is done with the interaction they can simply end the interaction or, via the floor, invite another agent to enter the conversation (e.g. Dialogue Assistant B in the diagram).   The change of control of a dialog between two agents is called 'delegation'.

Dialog Assistants may also engage the services of another dialog assistant behind the scenes to assist with the conversation (e.g. Assistant A engages the services of assistant C to support it in its interaction with the user.)    The controlling agent might choose to pass utterances unaltered to the target agent and may in return pass the target agent's responses unaltered to the user.  This pattern is termed 'channeling'. It is in many ways functionally equivalent to delegating the conversation but the channeling agent passes the messages on or can intervene or override the contribution of the agent to which the conversation is being channeled.  For example, a channelling agent may decide to keep the intent of the utterance but change how the content is rendered.  In a voice interface this might involve things like increasing the volume for the hard of hearing, decreasing the speed of presentation for the cognitively challenged or for non-native speakers, change the voice characteristics of the presentation, or change the language, or change visual characteristics if these are present.

Alternatively, the intermediate agent may reformulate the user's utterances and/or the target agent's utterances, holding whole conversations behind the scenes in order to achieve a goal.  This pattern is termed 'mediation'.  The mediation pattern also may be particularly relevant in the case where the target agent is in fact another human user (e.g. where an autonomous agent acts on behalf of a user to book an appointment with a doctor or restaurant).

There is no limit to the depth of a channeling or mediation chain and delegation can happen at any level in such a chain.  Any agent that is hosting a mediated or channeled conversation will act as the conversation floor manager to those agents it is hosting.

The patterns described above allow for conversation between one user and multiple agents where it is clear which agent has the conversational floor at any given moment.  As noted the channeling and mediation pattern do allow for more than one conversational agent to be involved in the conversation at the same time.

#### 0.4 Multi-Party Conversations

<img width="350" alt="Multi-Party Conversations" src="round-table-configuration.png">

\
**Figure 2.  Multi-party conversations hosted by a floor manager and a convener agent.**\
\
This specification also supports the implementation of simultaneous multi-party conversation where multiple users and agents may be listening to the conversation simultaneously and take turns to speak or even speak over one another. Figure 2 shows how this works.  It extends Figure 1 to show multiple agents taking part in a conversations simultaneously.  As in Figure 1, the floor manager manages the conversational interaction.  

A paper describing the evolution of this approach can be found in [7].  Support for multi-party conversations is maturing but is still somewhat experimental. Additional features or small changes may be necessary as the use-cases and patterns mature.

The multi-party conversation paradigm can also be used as a framework-free agentic framework where autonomous AI agents collaborate using a shared floor to achieve a goal.  The Open-Floor approach offers a symmetrical peer-to-peer way for agents to collaborate which is in contrast to other asymmetric user/agent models. 

#### 0.4.1 Floor Manager

Any component or agent that has created a conversation and invited conversants to it is acting as the 'floor' for the users or agents in that conversation. For example all three of the following will act as a floor manager:

- An open-floor compliant host browser acting as the media interface with a user and inviting agents to that conversation under the control of the user.  
- A floor-manager component that hosts multi-party conversation with many conversants invited to the floor at once.
- An agent that channels or mediates communication through to another agent.

The floor manager maintains the _conversation_ section of the envelope. Using simple deterministic rules, the floor manager decides which agents should receive which events. In general, all events are sent to all conversants to decide which events to respond to (or not). There are some special cases for certain events, particularly regarding the _private_ flag. 

The floor manager should exhibit predictable, autonomic behaviour that is standardized. All discretionary actions such as handling invitations or floor requests can be delegated by the floor manager to a designated convener agent. In general autonomic floor behaviour will be sufficient for conversations with a single user and a single agent at any time. In the case of Multi-party conversations a convener is likely to be required unless all of the participants are extremely disciplined in their behaviours.  

See the section on [Minimal Behaviours for a Floor Manager](#minimal-behaviours-for-a-floor-manager) for more details.

#### 0.4.2 Convener

In a multi-party conversation the floor will optionally invite a 'Convener' agent to the conversation.  This is an Open-Floor compliant agent but is granted special privileges. The convener acts like the chair of a meeting, mediating which conversants should be invited and if necessary removing conversants from the conversation.  It also plays a role deciding who is granted floor rights at any given moment.

Agents who are willing and able to act as conveners will publish this in their manifest.  The floor manager is the arbiter of whether to invite a convener or not. The identity of the current convener is published in the _conversation_ section of the envelope.   Only one convener is allowed at any one time.

The floor manager redirects certain events that are intended for a particular recipient to the convener. The convener then chooses whether to re-submit these events to the floor manager who will forward them on to the original target conversant.   The convener may also initiate events to manage the conversation such as revoking or granting the floor and un-inviting conversants who are behaving in a manner that is detrimental to the conversation.

Note that any conversant can invite any other conversant to the conversation. The convener will then moderate whether to honor this invite or not.

If the conversation does not have a convener assigned then the floor manager will play the role of a convener, meeting the minimum requirements for a convener.  For more details, see the section on [Minimal Behaviours for a Convener](#minimal-behaviours-for-a-convener).  There is no guarantee that a conversation without a convener will be stable but a convenerless floor can be helpful for collaboration between groups of agents that are aware of each other and strongly aligned in their ethos and goals.

#### 0.4.3 Managing the floor

The floor manager also maintains and publishes a list of which conversants currently have floor rights. (See the [_floorGranted_ section in the conversation object](#16-conversation-object) for more details.)

The Open-Floor protocol uses floor rights to help manage orderly interactions. By default a conversant has the floor until they either choose to yield the floor or the convener explicitly revokes their floor rights.  The floor manager keeps track of the floor status of each conversant but it does not enforce it.   Agents can send an utterance event whenever they choose and it will be propagated by the floor manager to the relevant conversants.  The floor granting and revoking mechanism in Open-Floor is therefore advisory and intended to facilitate orderly co-operation between well-behaved agents.  

The convener can however enforce agent behaviour.  It has a role to monitor events and if agents are not behaving in ways that are beneficial to the interaction they can be uninvited.   The floor manager will always respect the wishes of the convener regarding which conversants are currently invited or uninvited to the conversation.

Note that any conversant can request floor rights on behalf of themself or another conversant.  The convener will then moderate whether to accept this request or not.

#### 0.5 Discovery

Agents can ask other agents if they are able to satisfy a certain enquiry or whether they can recommend another agent for the task.  This pattern is called 'discovery'.   In the discovery pattern, the initiating agent asks another agent for a list of agents includes details of the task to this agent.  The recipient can then respond by:

- Proposing themself for the task (i.e. 'accept' the request to do a task)
- Proposing one or more agents for the task with a rating (i.e. act as a discovery agent)
- Proposing one or more agents to help 'find' an agent for the task (i.e. recommend another discovery agent)
- Proposing no agents (i.e. the agent cannot do the task or recommend any other agent)

In all cases the requesting agent receives one or more manifest which publishes the proposed agents identity and capabilities in a standard form.

The requesting agent can then choose to invite the proposed agent to the conversation, or simply speak directly to the proposed agent if they are already party to the conversation.  This feature can also be used to ask an agent for a manifest of its own capabilities.

By combining this discovery mechanism with the delegation and channelling patterns mentioned above rich patterns of agent interaction can emerge. Some agents can specialize as 'discovery agents' whose only role is to provide recommendations of other agents. This provides the conversational equivalent of a web search.  Agents can also recommend themselves for some enquiries and recommend other agents for others. This allows, for example, for a primary assistant to perform day to day tasks and recommend other agents for less common tasks. Agents can ask one or more agents to assist with this search who in turn can ask other agents.   Planning agents may propose steps to be taken in achieving a plan and then an orchestrating agent can then discover and invite agents to achieve parts of the plan.

#### 0.6 Agent Identity

Agents and human conversants in a conversation need to be able to identify and recognize each other during a conversation.  Conversants in this standard are located and identified by two parameters:

- **serviceUrl** - The URL of the server that hosts the agent.  
- **speakerUri** - A unique string that uniquely identifies the agent in URI syntax. 

Let's use an analogy to illustrate the difference between the two.   The _serviceUrl_ could be analogous to the exact address that can be used to locate the agent and the _speakerUri_ identifies the specific agent at that address.

The **serviceUrl** should point to an end-point that is capable of consuming and generating Open-floor message envelopes.

Agents or human conversants are free to choose any valid URI to identify themselves.  speakerUri's should be unique and ideally remain persistent for the whole lifetime of the agent or user.  Ideally, the speakerUri should be a URN [5] but any valid URI can be used.  The purpose of this URI is to provide a persistent unique key to the identity of the agent.  It is not a requirement that this URI be resolvable to an actual location on the internet.  The _serviceUrl_ is used for this purpose.

Examples of valid speakerURI are given below.

- **tag:sandro@w3.org,2004:Sandro**: A Tag URI as per [6]
- **urn:isbn:978-3-16-148410-0**:  A URN as per [5]. The isbn scheme is used for books.
- **mailto:info@example.com**: A URI that specifies an email address associated with an agent
- **tel:+1-212-555-1212**: A URI that specifies a phone number associated with an agent
- **https://openfloor.myopenflooragent.com/agent#3456**: A URI using an http address that could be the same as the agent serviceUrl.

NOTE: This standard is currently agnostic regarding the URI scheme used for an agent. Options for standardizing further might include the registration of a specific URN namespace identifier, for example, 'urn:openFloor' [5]. In the short term Tag URIs [6] represent a pragmatic way to generate a unique identifier for an agent.  In this document we use Tag URIs in all examples.

### 1 SPECIFICATION

#### 1.1 Syntax and Protocol

A conversation envelope will be represented as a JSON [1] object in a string format.  The JSON conversation envelope is expected to be a stand-alone document or object but there is no reason that it cannot be part of a larger JSON document.

JSON was chosen for the Open-Floor conversation envelope as it is an Open and Human Readable Standard format for Data Exchange that is independent of any particular protocol.  Supported protocols and the mechanisms by which two agents agree on a protocol to be used are currently outside the scope of this document.\
\
For the sake of simplicity, it is anticipated that Open-Floor implementations will initially use HTTPS as underlying communication protocol, but could include several other ones currently available (i.e. SIP, Websockets, WebRTC, etc) or any future available ones (i.e, HTTP/3, etc).

#### 1.2 AAA & Security

Authorization, Authentication, Accounting, and Security specifications are outside the scope of this document and will be defined in separate documents. 

#### 1.3 Nomenclature

This specification uses ‘camelCase’ (i.e. no spaces with new words being capitalized) for all nominal property names, for example, _eventType_ and _dialogHistory_.  

#### 1.4 Message Envelope Structure

    {
      "openFloor": {

          "schema": {
              "version": "1.1.0",      
              "url": "https://github.com/open-voice-interoperability/docs/tree/main/schemas/conversation-envelope/1.1.0/conversation-envelope-schema.json"
          },

          "conversation": {
              "id": "31050879662407560061859425913208",
              "conversants": [
                  {partial manifest speaker 1}
                  ...
                  {partial manifest speaker N}
              ]
          },
    
          "sender": {
            "speakerUri" : "tag:acmeConvenerAssistant.com,2025:0021"
          },
    
          "events": [
              {
                  "to": {
                      "serviceUrl": "URL of intended recipient A",
                      "speakerUri": "Speaker Uri of intended recipient A"
                  },
                  "eventType": "event type A",
                  "parameters": {
                    "parameter 1" : { parameter 1 values },  
                    … 
                    "parameter n" : { parameter n values }  
                  }
              },
              {
                  "to": {
                      "serviceUrl": "URL of intended recipient B",
                      "speakerUri": "Speaker Uri of intended recipient B"
                  },
                  "eventType": "event type B",
                  "parameters": {
                    "parameter 1" : { parameter 1 values },
                    … 
                    "parameter n" : { parameter n values }   
                  }
              }
          ]
      }
    }

##### Figure 3. An example of a conversation envelope #####

Figure 3 shows an example of a conversation envelope.  The envelope is wrapped in an 'openFloor' key.   This contains four sections:

* schema - the version of the conversation envelope and a schema to validate it against
* conversation - persistent information related to the current dialog
* sender - details of the sender of the envelope
* events - a list of Open-Floor 'events'

All sections are mandatory.

#### 1.5 Schema Object

    {
      "openFloor": {
        ..
        "schema": { "version": "1.1.0" }
        ..
      }
    }

##### Figure 4. Mandatory elements of the _schema_ object.

The _schema_ object specifies the format of the message in this Open-Floor envelope.  It is mandatory. It must contain a valid _version_ number for an Open-Floor envelope.  Figure 4 shows the minimal information that must be present in an Open-Floor-compliant envelope.

    {
      "openFloor": {
        ..
        "schema": {
          "version": "1.1.0",   
          "url": "https://github.com/open-voice-interoperability/docs/blob/main/schemas/conversation-envelope/1.1.0/conversation-envelope-schema.json"
        }
        ..
      }
    }

##### Figure 5. Other optional elements in the _schema_ object.

The schema for the version of the envelope specification can be found in [https://github.com/open-voice-interoperability/docs/blob/main/schemas/conversation-envelope/1.1.0/conversation-envelope-schema.json](https://github.com/open-voice-interoperability/docs/blob/main/schemas/conversation-envelope/1.1.0/conversation-envelope-schema.json).  Figure 5 shows an optional _serviceUrl_ that may also be included which should point to the correct version of that JSON schema.

#### 1.6 Conversation Object

    {
      "openFloor": {
        …        
        "conversation": { "id": "jk31050879662407560061859425913208" },
        … 
      }
    }

##### Figure 6. Mandatory elements of the _conversation_ object.

The conversation object carries persistent information related to the current conversation. 

As shown in Figure 6, the conversation section contains just one piece of mandatory information - the id of the conversation.  The id  should be a unique identifier for the current conversation with the user.  Persistent information relating to this current conversation can be keyed to this id.   The id  can be any arbitrary length character sequence that can be represented as a string in JSON.

It is the responsibility of the floor manager (or the agent playing the role of the floor manager) to maintain the contents of the conversation section.  Conversants only need to include the 'id' section in any envelopes sent. Any other sections that are included by conversants will be replaced by the floor manager to ensure accuracy and consistency.

    {
      "openFloor": {
        …        
        "conversation": { 
          "id": "jk31050879662407560061859425913208",

          "assignedFloorRoles" : { 
            "convener" : ["tag:dev.buerokratt.ee,2025:0001"] 
          },

          "floorGranted" : [
            "tag:user1.example.com,2025:1234", 
            "tag:agent2.example.com,2025:5678"
          ],

          "conversants" :[
              {      
                "identification":
                  {
                      "speakerUri" : "tag:dev.buerokratt.ee,2025:0001",
                      "serviceUrl": "https://dev.buerokratt.ee/openfloor/conversation",
                      "organization": "Government of Estonia",
                      "conversationalName": "Buerokratt",
                      "department": "Passport Office",
                      "role": "Immigration Specialist",
                      "synopsis": "Immigration specialist as part of the Beurocrat system.",
                      "openFloorRoles": {"convener": true}
                  }
              },
              {      
                "identification":
                  {
                      "speakerUri" : "tag:user1.example.com,2025:1234",
                      ...
                  }
              },
              {      
                "identification":
                  {
                      "speakerUri" : "tag:agent2.example.com,2025:5678",
                      ...
                  }
              },
          ]
        },
        … 
      }
    }

##### Figure 7. Optional elements in the _conversation_ object.

Figure 7 shows other additional elements in the conversation object. 

##### 1.6.1 The _conversants_ section

The _conversants_ section is optional if there are two or less conversants in the conversation.   It is mandatory if there are more than two conversants in the current conversation or there is an _assignedFloorRoles_ or _floorGranted_ section in the _conversation_.   It is a good practice to always have a _conversants_ section.   

The _conversants_ section contains a list of all the conversants in the conversation. Each conversant object should contain an _identification_ key. The _identification_ section should be a copy of the _identification_ section of the agent's manifest as defined in [4].   

##### 1.6.2 The _assignedFloorRoles_ section

The _assignedFloorRoles_ dictionary is a record of which conversants have been assigned specific Open-Floor roles by the floor manager. Each role maps to an array of speakerURIs for agents currently assigned that role, with some roles (like convener) having a maximum cardinality of 1. Any conversants that are assigned roles must also be listed in the "conversants" section.

The _assignedFloorRoles_ dictionary is optional in the conversation section. It is good practice to include it but if it is absent then it is assumed that no special roles have been assigned.

Conversants advertise their willingness to perform certain roles in the _Identification.openFloorRoles_ section of their manifest.   Roles are only assigned to agents by the floor manager. There is no obligation of a floor manager to assign an agent a certain role.  

Conversants are not limited to fulfilling a single role, they can have any number of roles within a conversation.

The roles that a floor manager can assign are listed below.  The default value of the _Identification.openFloorRoles_ element for each conversant are defined in [[4]](https://github.com/open-voice-interoperability/docs/blob/main/specifications/AssistantManifest/1.0.1/AssistantManifestSpec.md) and repeated below for clarity.   

|Open-Floor Role|Description|Default manifest role|Max conversants|
|-|-|-|-|
|`convener`|The agent is acting as floor convener, dealing with invites and floor grant requests|False|1|

##### 1.6.3 The _floorGranted_ section

The _floorGranted_ section is maintained by the floor manager and keeps a record of the conversants who are currently granted floor rights using the convener to make floor grant decisions if a convener is assigned.  The section contains an array of speakerURIs for conversants who have floor rights.

The _floorGranted_ list is optional in the _conversation_ section. It is good practice to include it but if it is absent then it is assumed that all conversants have floor grant rights.

Rights to the floor are granted when a _grantFloor_ event is sent and revoked when a _revokeFloor_ event is sent. By default all conversants have floor rights when they join a conversation. 

Floor grants are not policed by the floor manager and any conversant can send an _utterance_ to the floor regardless of their floor grant status. However, this is considered bad etiquette and may result in the convener revoking floor rights or even uninviting conversants.

#### 1.7 Sender Object

    {
      "openFloor": {
        …        
        "sender": {
            "speakerUri" : "tag:acmeConvenerAssistant.com,2025:0021",
            "serviceUrl": "https://acmeConvenerAssistant.com",
        },
        … 
      }
    }

##### Figure 8. Elements of the _sender_ object. 

Figure 8 shows the elements in the sender object.  _speakerUri_ is mandatory. The _serviceUrl_ is optional. It is good practice to include it if there is no _conversants_ section or the protocol being used to transport the envelopes does not carry source and destination address information.   

#### 1.8 Events Object

    {
      "openFloor": {
        ..
        "events": [
          {
            "to": {
                "speakerUri": "Speaker Uri of intended recipient A",
                "serviceUrl": "URL of intended recipient A",
                "private": false
            },
            "eventType": "event type A",
            "reason": "reason for sending event A",
            "parameters": {
              "parameter 1" : { parameter 1 values },  
              … 
              "parameter n" : { parameter n values } 
            }
          },
          {
            "to": {
                "serviceUrl": "URL of intended recipient A",
                "speakerUri": "Speaker Uri of intended recipient A"
            },
            "eventType": "event type B",
            "reason": "reason for sending event B",
            "parameters": {
              "parameter 1" : { parameter 1 values },
              … 
              "parameter n" : { parameter n values }   
            }
          }
        ]
      }
    }

##### Figure 9. The _events_ object

Figure 9 shows the structure of the _events_ object.  This should be an array of one or more objects which we will call an event object. 

Each event object must have an _eventType_, which is a string.  Other parameters may be present depending on the eventType. The _parameters_ object is a dictionary of parameter objects with standard key names specific to the event-type.  Some eventTypes support a 'bare' mode without any parameters. 

The optional _to_ section contains three parameters. The first is a _speakerUri_ of the target recipient.  The second is the _serviceUrl_ which is a valid URL of the assistant that the message is intended for.   The _to_ section is optional. If it is present then it must contain a _ServiceUrl_ or a _speakerUri_ or both.  If the _to_ section is not present then is can be assumed that the event is intended for all recipients of the envelope.   The third parameter is a _private_ boolean parameter which, when set to true, indicates that the event is only intended for the _to_ agent alone.  

The _private_ parameter is used by the floor manager to decide how to direct _utterance_ events. If true then the event is only sent to the designated agent and is not be copied by the floor manager to any other agents in a multi-participant conversation.  If it is not defined it is assumed to be _false_ i.e. any message intended for another recipient can be copied to other participants in the conversation for context. If there is not a _to_ section then the event is by default assumed to be public.  Other event types can have a _private_ parameter defined but this will not stop the floor manager sharing these events with all parties in the conversation.  For more detail see [Section 2.2](#22-Minimal-Conversation-Floor-Manager-Behaviors-on-Receipt-of-Events)


        "events ": [
          ...
          
          {
            "eventType":"revokeFloor",
            "to": {
              "speakerUri":"tag:agentBeingRevoked,2025:1234"
            },
            "reason" : "convener agent taking back the floor because @timedOut"
          }

          ...
        ]

##### Figure 10. Example of "reason" section containing a special token @timedOut.

The optional _reason_ section is a string which can be used to convey the reason that the event is being sent.  This text can contain natural language in any language but by convention special tokens can be included which have special meaning for the event.   These are prefaced by an '@' sign, for example, '@timedOut'.  Special tokens cannot contain anything that could be considered to be a word break such as white space or punctuation. For clarity, a special token is defined as any substring in the _reason_ text that matches the  regular expression: `@[a-zA-Z0-9_]+`

Figure 10 shows an example of this.

#### 1.9 Event-Types

The following are valid values for _eventTypes_.

* **speaking or sending multi-media events** (publicly or privately)
  * _utterance_  - One or more dialogEvent media objects spoken or presented (or whispered privately) from one conversant to some or all participants

* **joining or leaving conversations**
  * _invite_ - A conversant is invited to join the conversation.
  * _uninvite_ - A conversant is removed from the conversation.
  * _acceptInvite_ - A conversant is accepting an invitation to join a conversation.
  * _declineInvite_ - A conversant is declining an invitation to join a conversation.
  * _bye_ - A conversant is leaving the conversation

* **discovering other agents and establishing their capabilities**
  * _getManifests_ - Ask an agent to recommend themself or another agent for a task.
  * _publishManifests_ - Return a list of manifests for agents that can meet the request.

* **managing who has the conversational floor** (support for multi-party conversations and floor passing between agents)
  * _requestFloor_ - Used by a conversant to request the floor.
  * _grantFloor_ - Used by a convener agent to offer the floor to a conversant. 
  * _revokeFloor_ - Used by a convener agent to revoke the floor from a conversant. 
  * _yieldFloor_ - Used by a conversant to yield the floor.

The following sections define these event objects in more detail.

#### 1.10 Utterance Events

    {
      "openFloor": {
        ..
        "events": [
          {
            "to": { 
              "speakerUri" : "tag:someBotOrPerson.com,2025:0021"
            },
            "eventType": "utterance",
            "parameters": {
              "dialogEvent": {
                "speakerUri": "tag:userproxy.acme.com,2025:b5y09lky5KU5",
                "span": { "startTime": "2023-06-14 02:06:07+00:00" },
                "features": {
                  "text": {
                    "mimeType": "text/plain",
                    "tokens": [ { "value": "I need my repeat medication" } ]
                  }
                }
              }
            }
          },
          ..
        ]
      }
    }

Figure 11. Example of an Open-Floor _utterance_ event.

The utterance event is the message that is for assistants or users to 'speak' to each other.  Whilst utterances are designed to carry linguistic media events they can contain media of any type.  

The Open-Floor standard currently support four standard feature types but other arbitrary feature names and mime-types are also permitted.  The supported keys are:

- `text` - A message that is spoken or written language.
- `ssml` - A message that is to be verbalized using Speech Synthesis Markup Language.
- `html` - Multi-media content in HTML format.
- `audio` - Audio content in one of a number of audio formats.

Then dialogEvent can contain multiple feature objects but it must contain a `text` feature which should be capable of being 'verbalized' (i.e. this is content that is intended for direct consumption as written or spoken language by the recipient). For dialogEvents containing `ssml` content the `text` dialogEvent will typically be the plain text version of the message being spoken in the `ssml` element.

Figure 11 shows the structure of an event with the _eventType_ of _utterance_.
This object contains just one mandatory parameter with the key-name _dialogEvent_.
The _to_ parameter is optional and by default utterance events are public and addressed to all conversants. 
They can however be addressed to specific conversants and/or made private using the private flag in the _to_ element of the event.
A private utterance event is also termed a 'whisper'.  These can be used to convey instructions and contextual information behind the scenes between conversants.

The _dialogEvent_ element must contain a valid dialog event object as specified in [[2] Interoperable Dialog Event Object Specification Version 1.0.2](https://github.com/open-voice-interoperability/docs/blob/main/specifications/DialogEvents/1.0.2/InteropDialogEventSpecs.md)

Compliant Open-Floor dialog agents must respond to the content in the `text` feature.  All other content can be ignored and the agent will still be considered compliant.

##### 1.10.1 dialogEvent `text` Feature

The _text_ feature is **mandatory** in all dialog events.  The text feature contains content that is capable of being verbalized as an utterance.

|parameter|Description|
|-|-|
|_mimeType_|text/plain|
|_speakerUri_|The _speakerUri_ should be a unique identifier to the speaker that was or will be perceived as the social actor in the conversation.  Assistants that are channeling utterances from other agents or speakers should keep the _speakerUri_ of the original speaker.   This is one of the main distinctions between channeling and mediation.  It is the responsibility of the agent that generates the event to decide which _speakerUri_ to attach to the event.|
|_value_|Any number of values are allowed as strings in the _tokens_ section.  When concatenated together the _tokens_ should represent the orthographic representation of the utterance.|
|_valueUrl_|Any number of value URLs are allowed in the tokens section.  These URLs should locate content of type 'text/plain' and when downloaded and concatenated together the _tokens_ should represent the orthographic representation of the utterance.|

##### 1.10.2 dialogEvent `html` Feature

The _html_ feature is optional and can be used in dialog events to include HTML-formatted content for visual presentation.

|parameter|Description|
|-|-|
|_mimeType_(s)|text/html</br>application/xhtml+xml|
|"lang"||
|"encoding"|As per the 'charset' often associated with the mime-type|
|_speakerUri_|As above|
|_value_|Any number of values are allowed as strings in the _tokens_ section. Each token value should be 'valid' HTML in its own right.  For example an element within an `<html>` tag or any other bare html content such as `<h1>` or bare text. In general just include one _value_ document.|
|_valueUrl_|Any number of value URLs are allowed in the tokens section. These URLs should locate content of mime-type given when downloaded.|

##### 1.10.3 dialogEvent `audio` Feature

The _audio_ feature can be used in dialog events to transmit audio content. 

|parameter|Description|
|-|-|
|_mimeType_(s)|audio/mpeg</br>audio/mp4</br>audio/aac</br>audio/ogg</br>audio/opus</br>audio/webm</br>audio/wav</br>audio/flac</br>audio/x-flac</br>|
|_speakerUri_|As above|
|_value_|Inline audio content should be represented as base64 encoding and match the mime type specified. If more than one token value is supplied then all values must be in the same mime type and will be interpreted as sequential audio in the order presented.|
|_valueUrl_|Any number of value URLs are allowed in the tokens section. These URLs should locate content of mime-type given when downloaded.  They are ordered in the order that the audio should be presented|

##### 1.10.4 dialogEvent `ssml` Feature

The _ssml_ feature can be used in dialog events to include SSML [[8] Speech Synthesis Markup Language](https://www.w3.org/TR/speech-synthesis11/) for richer speech synthesis rendering.

|parameter|Description|
|-|-|
|_mimeType_|application/ssml+xml |
|_speakerUri_|As above|
|_value_|Any number of _value_(s) are permitted in the _tokens_ section. Each _value_ should be a _<speak>_ element wrapping valid SSML as per |
|_valueUrl_|Any number of value URLs are allowed in the tokens section. These URLs should locate content of mime-type given when downloaded. They are ordered in the order that the audio should be presented|
|_speakerUri_|As above|
|_value_|Any number of _value_ strings can be contained in the _tokens_ section. Each _value_ string should be a valid SSML `<speak>` element.|
|_valueUrl_|Any number of value URLs are allowed in the tokens section. These URLs should locate content of mime-type given when downloaded.  They are ordered in the order that the audio should be presented|


### 1.11 Extensible Dialog Event Features

The features in Dialog Events are intentionally intended to be extensible.   In addition to the dialog features described above any other arbitrary features can be added with any mime type.

For example, a video feature intended to represent Video Conversational agent communications (i.e. Avatar communications) could be added as shown in Figure 13.  This example is informative only.

      "features": {
        ...
        "video": {
          "mimeType": "video/mpeg",
          "tokens": [
            {
              "valueUrl": http://localhost/xyz1234.m4a
            }
          ]
        },
        ...
      }

#### Figure 13. Example video feature, which at present would be considered a custom feature.

#### 1.12 invite Event

    {
      "openFloor": {
          "schema": {
            "version": "1.1.0"      
          },
          "conversation": {
            "id": "someUniqueIdCreatedByTheFirstParticipant"
          },
          "sender": {
              "speakerUri": "tag:botThatOfferedTheInvite.com,2025:4567"
          },
          "events": [
              {
                  "eventType": "invite",
                  "to": { 
                    "serviceUrl": "https://botsite.botBeingInvited.com",
                    "speakerUri": "tag:botBeingInvited.com,2025:1234"
                  }
              }
          ]
      }
    }


##### Figure 15. Mandatory elements of the _invite_ object shown as a 'bare invite'

Invite events act as an invitation for the target agent to enter the conversation.  They also invite the target agent to take the conversational floor and respond to all utterances from this point onwards.  The  _to_ object is used to specify the identity of the agent that is being invited.  

The _to_ object is mandatory for an _invite_ event and must contain a _serviceUrl_.   The _speakerUri_ is optional and can be used if the inviting agent knows the specific _speakerUri_ of the agent that it wants to invite.  If a _speakerUri_ is sent then there is no obligation that the agent that responds to the invite adopts that speakerUri.

If the _to_ event is absent, then all recipients of the envelope should consider themselves invited to the conversation.

It is possible to invite an agent to a conversation without giving it any other events.  This is termed a bare invite as shown in Figure 15.  The recipient of such a bare invitation is being invited to engage with the user without being given any context.  A suitable response would be to speak a greeting and ask how the agent can help.

    {
      "openFloor": {
        "schema": {
          "version": "1.1.0"      
        },
        "conversation": {
          "id": "31050879662407560061859425913208"
        },
        "sender": {
            "serviceUrl": "https://botsite.botThatOfferedTheInvite.com",
            "speakerUri": "tag:botThatOfferedTheInvite.com,2025:4567"
        },
        "events": [
          {
            "eventType": "utterance",
            "parameters": {
              "dialogEvent": {
                "speakerUri": "tag:botThatOfferedTheInvite.com,2025:4567",
                "span": { "startTime": "2023-06-14T02:06:07Z" },
                "features": {                         
                  "text": {
                    "mimeType": "text/plain",
                    "tokens": [ { "value": "I'll pass you over to my-weather." } ]
                  }
                }
              }
            }
          },
          {
            "eventType": "invite",
            "to": { 
              "serviceUrl": "https://siteof.botThatIsBeingInvited.com",
              "speakerUri": "tag:botThatIsBeingInvited.com,2025:1234"
            },
            "parameters": {
              "dialogHistory": [
                { .. utterance dialog event N-2 .. },
                { .. utterance dialog event N-1 .. },
                {
                  "speakerUri": "tag:theUser.com,2025:3456",
                  "span": { "startTime": "2023-06-14T02:06:07Z" },
                  "features": {                         
                    "text": {
                      "mimeType": "text/plain",
                      "tokens": [ { "value": "What is the weather in Detroit right now?" } ]
                    }
                  }
                }
              ]
            }
          }
        ]
      }
    }

##### Figure 16. A typical dialog envelope for an invite, including a voiced transfer prompt and dialog history in the invite event.

Invite events may be accompanied by additional events and contain optional parameters. The _invite_ event can include an optional _dialogHistory_ parameter which is a simple list of dialog events containing some or all of the utterances in the dialog. It is good practice to order these in startTime order (in universal time) with the most recent event being the last item in the list. It is at the discretion of the sender of the _invite_ to decide how much history to include and whether to omit or anonymize certain dialogEvents in order to maintain security and confidentiality. For example, the inviting agent may decide to send the last 'N' (e.g. N=4) events in the dialog as if the invited agent had been at the floor for those N dialog turns. If the agents had not been entitled to receive some of those events then these could also be omitted from the dialogHistory array or anonymized or redacted in some fashion.

Figure 16 shows a conversation envelope where the inviting agent tells the user that they are inviting another agent to speak with them. Then the invite event issues the invitation with dialog history to help the invited bot respond appropriately.

### 1.13 uninvite Event

    {
      "openFloor": {
        "schema": {
          "version": "1.1.0"
        },
        "conversation": {
          "id": "someUniqueIdForTheConversation"
        },
        "sender": {
          "speakerUri": "tag:some_Convener.com,2025:"
        },
        "events": [
          {
            "eventType": "uninvite",
            "to": {
              "speakerUri": "tag:agentBeingUninvited,2025:1234"
            },
            "reason": "@brokenPolicy: agents should not contain content that is offensive or encourages illegal activity"
          }
        ]
      }
    }

##### Figure 17. A typical uninvite event 

The _uninvite_ event is the opposite of an _invite_ event and informs an agent that they have been removed from a conversation.  In the absence of a new _invite_ event, the agent should not expect to receive any more envelopes from this conversation.

The following special tokens have particular meaning in this event.

|Reason Token|Description|
|------|-----------|
|@timedOut|The floor manager or convener is removing the agent from the conversation because it believes that the agent has taken too long to respond.|
|@brokenPolicy|The floor manager or convener is removing the agent from the conversation because the agent has not met certain policy standards. This may be, for example, due to unsolicited or offensive contributions to the conversation.|
|@error|The floor manager or convener is removing the agent from the conversation because some kind of error has occurred which means it is no longer meaningful for the agent to continue being part of the conversation.|

### 1.14 acceptInvite Event

    {
      "openFloor": {
        "schema": {
          "version": "1.1.0"
        },
        "conversation": {
          "id": "someUniqueIdForTheConversation"
        },
        "sender": {
          "speakerUri": "tag:agentAcceptingInvite,2025:1234"
        },
        "events": [
          {
            "eventType": "acceptInvite",
            "to": {
              "speakerUri": "tag:some_Convener.com,2025:"
            },
            "reason": "Ready to support this request"
          }
        ]
      }
    }

##### Figure 18. A typical acceptInvite event

The _acceptInvite_ event can be sent in response to an _invite_ event.  It is a bare event with no parameters.  Its purpose is to accept an invite and confirm readiness to participate in the conversation.  Figure 18 shows an example.

The _reason_ section is optional.  It can be used to signal the reason that the agent chose to accept the invite.  There are no tokens with special meaning for this currently.  

### 1.15 declineInvite Event

    {
      "openFloor": {
        "schema": {
          "version": "1.1.0"
        },
        "conversation": {
          "id": "someUniqueIdForTheConversation"
        },
        "sender": {
          "speakerUri": "tag:agentBeingUninvited,2025:1234"
        },
        "events": [
          {
            "eventType": "declineInvite",
            "to": {
              "speakerUri": "tag:some_Convener.com,2025:"
            },
            "reason": "@unavailable to support this request due to lack of resources"
          }
        ]
      }
    }

##### Figure 19. A typical declineInvite event

The _declineInvite_ event can be sent in response to an _invite_ event.  It is a bare event with no parameters.  Its purpose is to decline an invite.  Figure 19 shows an example.

The following special _reason_ tokens have particular meaning in this event.

|Reason Token|Description|
|------|-----------|
|@outOfDomain|The agent is declining the invite because it cannot support the request addressed to it (and by inference another agent is needed to respond)|
|@unavailable|The agent is declining the invite because it temporarily unavailable for some reason such as lack of resources|
|@refused|The agent is declining the invite because it is not willing to handle this request|
|@error|The agent is declining the floor because it has encountered an error from which it cannot recover|

#### 1.16 bye Event

    {
      "openFloor": {
        "schema": {
          "version": "1.1.0"      
        },
        "conversation": {
          "id": "31050879662407560061859425913208"
        },
        "sender": {
          "speakerUri": "tag:botThatOfferedTheBye.com/7890"
        },
        "events": [
          {
            "eventType": "bye"
          }
        ]
      }
    }

Figure 20. A minimal _bye_ envelope detaching an agent from a conversation.

When an agent wants to leave the conversation it sends a _bye_ event.  This message indicates that the agent is leaving the dialog.   An example of the _bye_ event is shown in Figure 20. It has no _parameters_.  The optional _to_ object can be included but it is not necessary.

    {
      "openFloor": {
        "schema": {
          "version": "1.1.0"      
        },
        "conversation": {
          "id": "31050879662407560061859425913208"
        },
        "sender": {
          "serviceUrl": "https://siteof.someBot.com",
          "speakerUri": "tag:siteof.someBot.com,2025:1234"
        },
        "events": [
          {
            "eventType": "utterance",
            "parameters": {
              "dialogEvent": {
                "speakerUri": "tag:siteof.someBot.com,2025:1234",
                "span": { "startTime": "2023-06-14 02:06:07+00:00" },
                "features": {
                  "text": {
                    "mimeType": "text/plain",
                    "tokens": [ { "value": "Thank you! I am glad I could help." } ]
                  }
                }
              }
            }
          },
          {
            "eventType": "bye"
          }
        ]
      }
    }

Figure 21. A _bye_ event with a voiced farewell.

As with the _invite_ event, the _bye_ event can be accompanied by other events as shown in Figure 21.  In this example the agent indicates its intention to leave the conversation and voices a farewell as it does so.

### 1.17 getManifests Event

The _getManifests_ event can be used to ask an assistant about the services it provides or to recommend other assistants for a certain task.   There are a three use-cases for this event.

1. Asking a site or assistant (or human agent) about the tasks that it can perform.
2. Asking a site or assistant (or human agent) if they are willing and able to support a specific task.
3. Asking a site or assistant (or human agent) to recommend one or more assistants that can help with a certain task.

A _publishManifests_ event will be returned in response to the _getManifests_ event as defined in section 1.18. This will contain one or more manifests [4] each defining the location, identity, and services provided by a specific assistant.   The returned manifests will be classified as either _servicingManifests_ or _discoveryManifests_ depending on whether these agents are primarily servicing assistants or discovery assistants.

The _getManifests_ event has the following optional parameters:

- "recommendScope" : "external" | "internal" | "all"   (Default = "internal")

A _getManifests_ event can also optionally be accompanied by a private utterance event containing a natural language description of the task to be performed.

    {
      "openFloor": {
        "schema": {
          "version": "1.1.0"      
        },
        "conversation": {
          "id": "31050879662407560061859425913208"
        },
        "sender": {
          "serviceUrl": "https://someBot.com",
          "speakerUri": "tag:someBot.com,2025:4567"
        },
        "events": [
          {
            "eventType": "getManifests",
            "to": { 
              "serviceUrl": "https://dev.buerokratt.ee/openfloor/conversation"
            }
          }
        ]
      }
    }

##### Figure 22. Use Case #1. A bare getManifests event used to ask an assistant about the tasks that it can perform.

Figure 22 shows a getManifests event that is used to request the manifests of all the services provided by a certain site.   This is characterised by the following features:

- The _to_ object does not contain a _speakerUri_ indicating that the manifests of all agents served by this site are wanted.
- The _recommendedScope_ parameter is omitted or set to 'internal' value meaning that only services provided by the target server are wanted.

The returned manifest list will be expected to only contain manifests from the target server site - i.e. that have the same serviceUrl that the event is addressed to.   It is at the discretion of the target server to decide how many manifests to return. 

    {
      "openFloor": {
        "schema": {
          "version": "1.1.0"      
        },
        "conversation": {
          "id": "31050879662407560061859425913208"
        },
        "sender": {
          "serviceUrl": "https://someConvener.com",
          "speakerUri": "tag:someuser.com,2025:4567"
        },
        "events": [
          {
            "eventType": "getManifests",
            "to": { 
              "serviceUrl": "https://dev.buerokratt.ee/openfloor/conversation"
            },
            "parameters": {
              "recommendScope": "internal"
            }
          },
          {
            "eventType": "utterance",
            "to": { 
              "serviceUrl": "https://dev.buerokratt.ee/openfloor/conversation",
              "private": true
            },
            "parameters": {
              "dialogEvent": {
                "speakerUri": "tag:someuser.com,2025:4567",
                "span": { "startTime": "2023-06-14 02:06:07+00:00" },
                "features": {
                  "text": {
                    "mimeType": "text/plain",
                    "tokens": [ { "value": "Do I need a visa to enter Estonia from Spain?" } ] 
                  }
                }
              }
            }
          }
        ]
      }
    }

##### Figure 23. Use Case #2. Asking an assistant if they are willing and able to support a specific task.

Figure 23 shows the same bot as Figure 22 being asked if it supports a specific task. The private _utterance_ event is used to communicate the specific task that is being requested. It is this which distinguishes use case #1 from use case #2.   

The target assistant should return a _publishManifests_ containing any agents that it believes are capable and willing to respond to the private utterance. In the above example, the _recommendScope is explicitly set to the default value "internal".  

    {
      "openFloor": {
        "schema": {
          "version": "1.1.0"      
        },
        "conversation": {
          "id": "31050879662407560061859425913208"
        },
        "sender": {
          "serviceUrl": "https://someConvener.com",
          "speakerUri": "tag:someconvener.com,2025:4567"
        },
        "events": [
          {
            "eventType": "getManifests",
            "to": { 
              "serviceUrl": "https://myFavoriteDiscoveryBot.com"
            },
            "parameters": {
              "recommendScope": "external"
            }
          },
          {
            "eventType": "utterance",
            "to": { 
              "serviceUrl": "https://myFavoriteDiscoveryBot.com",
              "private": true
            },
            "parameters": {
              "dialogEvent": {
                "speakerUri": "tag:someconvener.com,2025:4567",
                "span": { "startTime": "2023-06-14 02:06:07+00:00" },
                "features": {
                  "text": {
                    "mimeType": "text/plain",
                    "tokens": [ { "value": "I require an expert with understanding about international visa requirements" } ] 
                  }
                }
              }
            }
          }
        ]
      }
    }

##### Figure 24. Use case #3. Asking a site or assistant to recommend one or more assistants that can help with a certain task.

Finally, Figure 24 shows use case #3 where a discovery agent is being asked to recommend some other agent to service a specific request.  The returned _publishManifests_ event should contain the manifests of any recommended assistants for the task.  

In this example the parameter _recommendScope_ has the value "external" which indicates that the assistant is not being invited to recommend itself for the task.  

In the most general case, when requested, assistants can also recommend their own services and/or the services of other agents.  The _recommendScope_ "all" is used to indicate this. 

The optional _to_ object can be used to indicate which agent is the intended recipient of the event.  If absent then all recipients should consider the request directed at them, i.e. all the conversants in the conversation are being invited simultaneously to to supply their own manifests or make recommendations.

As with the _invite_ event, there is no requirement for a _speakerUri_ on a _getManifests_ event.  If one is provided then it up to the receiving agent to decide how to take it into account.  If the event is addressed to a _serviceUrl_ without an _speakerUri_ then it is best practice to return all the manifests associated with that _serviceUrl_.  If a _speakerUri_ is sent then it is best practice to return only the manifest associated with just that _speakerUri_. If the _speakerUri_ does match then it is best practice to return an empty manifest list.  It may however be helpful for a discovery agent to return manifests of other discovery agents that it thinks might be able to help with the request.

See section 1.18 for more information on _publishManifests_ event behaviors.

### 1.18 publishManifests Event

    {
      "openFloor": {
        "schema": {
          "version": "1.1.0"      
        },
        "conversation": {
          "id": "31050879662407560061859425913208"
        },
        "sender": {
          "speakerUri": "tag://myFavoriteDiscoveryBot.com,2025:0001"
        },
        "events": [
          { 
            "to": {
              "serviceUrl": "https://someBotThatAskedForIt.com",
              "speakerUri": "tag:someBotThatAskedForIt.com,2025:1234"
            },
            "eventType": "publishManifests",
            "parameters": {
              "servicingManifests": [
                  {
                    "identification": {
                      "serviceUrl": "https://findMyAIAssistant.com",
                      "speakerUri": "tag:findMyAIAssistant.com,2025:xykz",
                      "synopsis": "A bot for those who love reading."
                      ...
                    },
                    "capabilities": {
                      ...
                    }
                    "score": 1.00
                  },
                  {
                    "identification": {
                      "serviceUrl": "https://nationalLibraryArchive.org",
                      "speakerUri": "tag:nationalLibraryArchive.org,2025:0564",
                      "synopsis": "A government catalog of every book published in the USA."
                      ...
                    },
                    "capabilities": {
                      ...
                    }
                    "score": 0.25
                  },
                  {
                    "identification": {
                      "serviceUrl": "https://booksRUs.com",
                      "speakerUri": "tag:booksRUs.com,2025:jkl12",
                      "synopsis": "Browse, sample and buy any book you desire."
                      ...
                    },
                    "capabilities": {
                      ...
                    }
                    "score": 0.14
                  }
                ],
                "discoveryManifests": [
                  {
                    "identification": {
                      "serviceUrl": "https://findMyAIAssistant.com",
                      "speakerUri": "tag:findMyAIAssistant.com,2025:searchInstance1567",
                      "synopsis": "Finds assistants anywhere in the world"
                      ...
                    },
                    "capabilities": {
                      ...
                    }
                    "score": 1.00
                  }
                ]
            }
          }     
        ]
      }
    }

##### Figure 25. A typical publishManifests event

The _publishManifests_ event is sent when one agent would like to publish the capability of itself or other agents.   This will usually be in response to a _getManifests_ event (See section 1.17) but can also be used to make a delegation suggestion in response to an _utterance_ (Section 1.10).

Once an agent receives a _getManifests_ event it can do a combination of the following:

- Recommend one or more agents (including itself) to service this request.
- Recommend one or more agents to help find who can service this request.

In order to support this the _publishManifests_ event has two optional parameters:

- _servicingManifests_ - A list of agents that can service this request.
- _discoveryManifests_ - A list of agents that can recommend other agents to service this request.

A common response from the receiver of this event will be to examine the returned manifests to decide whether to issue an _invite_ to that agent. This _invite_ event would often be accompanied by any _utterance_ event that was sent with the _getManifests_ event, suitably re-addressed to the agent that is being invited. 

If an agent receives any other event that it does not feel capable of servicing, it can also return a _publishManifests_ event as a recommendation to use the services of a different agent.   This is a soft form of delegation.  

The optional _to_ can be used to indicate a specific agent to which the manifest is addressed.  Otherwise any recipient should consider the proposal addressed to themselves.

There is no requirement for a _speakerUri_ in the _from_ section in a _publishManifests_ event.  If one is provided then it is good practice for the receiving agent to pass this speakerUri along in any subsequent _invite_ event to this agent.

Each list item in the recommendation should be in the manifest format as specified in [4].  In addition to the keys specified in that document, the manifest object can contain one additional optional key that is not present in the manifest specification:

  - _score_ - A recommendation score is a number between 0.0 and 1.0 with arbitrary precision. 

Any assistant that is returned in the _servicingManifests_ can be considered suitable to be sent an _invite_ to join the conversation and service the request.   If there are no manifests to return then a bare _publishManifests_ message can be returned or an empty array can be returned in the _servicingManifests_, _discoveryManifests_ or both.

Any assistant that is returned in the _discoveryManifests_ can be considered by the client as suitable to be re-sent the _getManifests_ event with the same accompanying utterances and context.  This allows an agent to recommend that the client uses another discovery agent to find a solution.  An agent should not recommend itself in the _discoveryManifests_.  This could lead to infinite regress.

Note that there is no requirement in the Open-Floor framework for an assistant to be exclusively either a discovery agent or a servicing agent. They can be both and the requesting assistant should be prepared to support both use case 1 or 2 - i.e. prepared for an agent to recommend itself for a task or recommend another agent for a task.  There is also nothing to stop an agent recommending servicing agents and discovery agents in its response or recommending the same agent as both a discovery agent and a servicing agent simultaneously.

The recommending agent is free to use any mechanism it wants to generate the _score_.

### 1.19 requestFloor Event

    {
      "openFloor": {
        "schema": {
          "version": "1.1.0"
        },
        "conversation": {
          "id": "someUniqueIdForTheConversation"
        },
        "sender": {
          "speakerUri": "tag:agentRequestingFloor.com,2025:1234"
        },
        "events": [
          {
            "eventType": "requestFloor",
            "to": {
              "speakerUri": "tag:some_Convener.com,2025:1234"
            },
            "reason": "more information to add"
          }
        ]
      }
    }

##### Figure 26. A typical requestFloor event

This event was added to support multi-agent mixed-initiative conversations, for example where a convener agent is present to co-ordinate the floor [7].

The _requestFloor_ event is used by agents that do not currently have the conversational floor to request it.  Figure 26 shows a typical _requestFloor_ envelope.

By default agents are given floor rights when they join a conversation.  If floor rights have been revoked for any reason, they can be requested using the _requestFloor_ event.  The _requestFloor_ event should receive a _grantFloor_ or _revokeFloor_ event in response form the floor manager (or via delegation from the convener).

The optional _reason_ section can be used to convey the reason for the floor request.  This can be used to help with the decision whether to grant the floor or not.  No special reason tokens are defined yet for this event.

### 1.20 grantFloor Event

    {
      "openFloor": {
        "schema": {
          "version": "1.1.0"
        },
        "conversation": {
          "id": "someUniqueIdForTheConversation"
        },
        "sender": {
          "speakerUri": "tag:some_Convener.com,2025:1234"
        },
        "events": [
          {
            "eventType": "grantFloor",
            "to": {
              "speakerUri": "tag:agentBeingGrantedTheFloor.com,2025:1234"
            }
          }
        ]
      }
    }

Figure 27. A bare grantFloor event

This event was added to support multi-agent mixed-initiative conversations, for example where a convener agent is present to co-ordinate the floor [7].

The _grantFloor_ event is used to grant the conversational floor to agents.    

In one use case, the _grantFloor_ event can be sent by floor managers in response to a _requestFloor_ event from an agent. Figure 27 shows a bare _grantFloor_ envelope which might be used for this purpose.  Once this message is received by an agent it is free to send _utterance_ events to the floor with the expectation that they will be delivered to the designated destination.

    {
      "openFloor": {
        "schema": {
          "version": "1.1.0"
        },
        "conversation": {
          "id": "someUniqueIdForTheConversation"
        },
        "sender": {
          "speakerUri": "tag:some_Convener.com,2025:1234"
        },
        "events": [
          {
            "eventType": "grantFloor",
            "to": {
              "speakerUri": "tag:agentBeingInvitedToTakeTheFloor.com,2025:1234"
            }
          },
          {
            "eventType": "utterance",
            "to": {
              "speakerUri": "tag:agentBeingInvitedToTakeTheFloor.com,2025:1234",
              "private": true
            },
            "reason": "new request",
            "parameters": {
              "dialogEvent": {
                "speakerUri": "tag:someConvener.com,2025:1234",
                "span": { "startTime": "2025-01-31T10:05:00Z" },
                "features": {
                  "text": {
                    "mimeType": "text/plain",
                    "tokens": [
                      { "value": "Go ahead an book a meeting at six o'clock for the user." }
                    ]
                  }
                }
              }
            }
          }
        ]
      }
    }

#### Figure 28. A grantFloor event inviting an agent to service a specific request.

Figure 28 shows an alternate use-case for the _grantFloor_ event. In this use case an agent is already present in a multi-party conversation. It does not currently have floor rights and has not requested it.  It is an observer in the conversation.  The convener, floor manager or another agent can direct a _grantFloor_ event to an agent with a private _utterance_ event to describing the purpose of the request.  This is very similar in structure and purpose to an _invite_ event but is sent to an agent that is already party to the conversation.

The optional _reason_ section can be used to convey the reason for the floor request.  No special reason tokens are defined yet for this event.   

The accompanying private _utterance_ event  explains in natural language and supporting media to the recipient describing what is requested of them.   This might be a user utterance or an instruction generated by another agent or the floor manager.   

### 1.21 revokeFloor Event

    {
      "openFloor": {
        "schema": {
          "version": "1.1.0"
        },
        "conversation": {
          "id": "someUniqueIdForTheConversation"
        },
        "sender": {
          "speakerUri": "tag:some_Convener.com,2025:1234"
        },
        "events": [
          {
            "eventType": "revokeFloor",
            "to": {
              "speakerUri": "tag:agentBeingRevoked,2025:1234"
            },
            "reason": "@override"
          }
        ]
      }
    }

##### Figure 29. A typical revokeFloor event

The _revokeFloor_ event informs an agent that they no longer have conversational floor rights.  A well-behaved agent should cease to send _utterance_ events on receipt of this event.  If the agent wants the floor after this, they should send a _requestFloor_ event.

Figure 29 shows a typical _revokeFloor_ event which shows an agent having the floor revoked because a higher precedence request has been made that needs to be serviced by a different agent.

The optional _reason_ key can be used to convey the reason that the floor has been revoked.  The following special _reason_ tokens are supported by this event type:

|Reason|Description|
|------|-----------|
|@timedOut|The convener is removing the agent's floor rights because the convener believes that the agent has taken too long to respond|
|@brokenPolicy|The convener is removing the agent's floor rights because the agent has not met certain policy standards|
|@override|The convener is removing the agent's floor rights because it is granting floor rights to another agent with higher precedence|
|@error|The convener is removing the agent's floor rights because some kind of error has occurred which means it is no longer meaningful for the agent to continue interacting.|

### 1.22 yieldFloor Event

    {
      "openFloor": {
        "schema": {
          "version": "1.1.0"
        },
        "conversation": {
          "id": "someUniqueIdForTheConversation"
        },
        "sender": {
          "speakerUri": "tag:some_agent_that_has_floor.com,2025:1234",
          "serviceUrl": "https://some_agent_that_has_floor.com"
        },
        "events": [
          {
            "eventType": "yieldFloor",
            "reason": "@complete"
          }
        ]
      }
    }

##### Figure 30. A typical yieldFloor event

The _yieldFloor_ event is sent by an agent to indicate that they no longer consider themself to have floor rights.  This means that the agent will cease to send _utterance_ events to any conversants until it is invited to the floor again.  The optional _reason_ parameter can be used to convey the reason that the floor has been yielded.

Figure 30 shows a typical _yieldFloor_ event indicating that the agent believes that they have completed the current goal that they are working on supporting and are not expecting to contribute any more utterances unless requested.

The following special _reason_ tokens are supported by this event type:

|Reason|Description|
|------|-----------|
|@outOfDomain|The agent is yielding the floor because it cannot support the request addressed to it (and by inference another agent is needed to respond)|
|@complete|The agent is yielding the floor because it believes it has completed the request|
|@timedOut|The agent is yielding the floor because it has time out waiting for responses and feels unable to help any further|
|@refused|The agent is yielding the floor because it is not willing to handle this request|
|@error|The agent is yielding the floor because it has encountered an error from which it cannot recover|

## 2 Minimal Behaviors

#### 2.1 Minimal Servicing Assistant Behaviors (on Receipt of Events)

Open-Floor compliant dialog assistants must support all event types in order to be considered fully compliant.  This section documents the minimal behavior expected from an Open-Floor compliant dialog assistant. These guidelines are informative not normative.

If any events contain a _to_ that is not addressed to the agent, then ignore the event.

If the _to_ section is addressed to the agent (or is absent) then the following minimal behaviours are recommended when receiving the following events. 

* utterance events - spoken or written natural language
  * _utterance_  -  Answer the speaker with an utterance in return <br>  (typically public utterances will have public responses and private utterances will have private responses)

* agent control events  - structure control messages
  * _invite_ - Either: 
    - Send _acceptInvite_ plus a 'hello' _utterance_ and respond to any accompanying _utterance_ events or _dialogHistory_ in the invite parameters
    - Send _declineInvite_ event with a decline reason.
  * _acceptInvite_ - Ignore this event from another assistant unless you were the agent that sent the _invite_.
  * _declineInvite_ - Ignore this event from another assistant unless you were the agent that sent the _invite_.
  * _bye_ - Ignore this event from another assistant.
  * getManifests
      - if the _to_ is addressed to you:
        - If the scope is 'internal' or 'all' - return your own manifest(s) in the _servicingManfiests_ section of a _publishManifests_ event.
        - If the scope is 'external' - ignore this event (if you are a servicing agent and not a discovery agent)
      - if the _to_ section is not specified: 
        - If the scope is 'internal' or 'all'
          - Consider whether the contents of the envelope is something you want to service.  If you are not sure, ignore this event. Otherwise return servicingManifests in a _publishManifests_ event containing the relevant manifests of the services you offer that can meet the request.
        - if the scope is 'external' - ignore this event.
  * _publishManifests_ - Ignore this event if you did not ask for mandates from another agent.
  * _uninvite_ - Leave this conversation (i.e. stop responding to all events from this conversation_id)
  
* floor management events - giving and taking the floor
  * _requestFloor_ - Ignore this message (unless you are floor manager, see below)
  * _grantFloor_ - If this is addressed to you then take the floor in a similar to receiving an _invite_.
  * _revokeFloor_ - If this is addressed to you, cease sending events and wait for either a _grantFloor_ or an _utterance_ directed specifically to you as an agent before sending any more events.  
  * _yieldFloor_ - Ignore this.

#### 2.2 Minimal Conversation Floor Manager Behaviors (on Receipt of Events)

The floor manager retains ultimate responsibility for:

- Responding to events and forwarding them to conversants. 
- Deciding which conversants are currently considered to have floor rights in the conversation.  
- Deciding which conversants are currently 'in' the conversation.

The floor manager should exhibit predictable autonomic behavior. If intelligent decisions are required then the floor manager will delegate these to a convener agent of its choosing.

Open-Floor compliant conversation floor managers (including host browsers) agents must support all normative event types in order to be considered fully compliant.

##### Curating the conversation section of envelopes

The floor manager must curate the conversation section of the envelope as follows:

- _conversant_ section
  - When the floor manager sends an invite to the intended conversant it will immediately add the conversant to the conversant list. 
  - The conversant will remain on the conversant list until either:
      - _declineInvite_ is received from that conversant.
      - _bye_ is received from that conversant.
      - _uninvite_ is sent to that conversant.

- _floorGranted_ section
  - By default, conversants are in a _floorGranted_ state as soon as they are added to the _conversant_ section.
  - conversants remain in this state until either:
    - A _yieldFloor_ is received from that conversant
    - A _revokeFloor_ is sent to that conversant
    - The conversant is removed from the conversants list (as they will no longer be part of the conversation)
  - If conversants are not in the floor granted state then they can be reinstated when:
    - A _grantFloor_ is sent to the conversant
  - For clarity the _requestFloor_ does not directly change the state of _floorGranted_

##### Delegating Events To Convener

|event|type|if no convener|
|-|-|-|
|_utterance_|Pass-Through (floorGranted=True)<br>Delegate (floorGranted=False)|Ignore|
|_invite_|Delegate to Convener|Pass-Through|
|_uninvite_|Delegate to Convener|Pass-Through|
|_declineInvite_|Pass-Through||
|_acceptInvite_|Pass-Through||
|_bye_|Pass-Through||
|_getManifests_|Pass-Through||
|_publishManifests_|Pass-Through||
|_requestFloor_|Delegate to Convener|Send _grantFloor_|
|_grantFloor_|Delegate to Convener|Pass-Through|
|_yieldFloor_|Pass-through||
|_revokeFloor_|Delegate to Convener|Pass-Through|

Floor Manager Action on Receipt of Events

For each event, the floor  manager will either pass the event through to the conversants or it will delegate the event to the convener agent.  The table above shows how each event should be treated.

In the table:
- **Pass-Through** means that the event will be sent to ALL conversants.  For utterance events the _private_ flag will cause the event to be passed to only the intended recipient.  For all other event types the _private_ flag will be ignored.     
- **Delegate to Convener** means that the event is forwarded to the convener and the convener is then responsible for returning this event back to the floor manager OR substituting it with different events.

##### Processing Envelopes and Events in Sequence [NORMATIVE]

Floor managers may be processing more than one envelope at a time and envelopes can contain multiple events.

The floor manager will process envelopes in the order that they are received and events in the order listed in the envelope.  

The floor manager should process each envelope in the order received as a separate thread taking each event in the envelope in the order declared.  
  - For each event use the Table above to decide if the event can be passed-through or needs to be delegated to the convener.
  - If an event needs to be delegated to the convener then send it in its own envelope to the convener and await a response
  - Insert any events returned from the convener at the head of the event list in the order they are returned and continue processing the event list.

#### 2.3 Ignoring events with protocols that require a response

If the messaging protocol that sent the envelope requires a response (e.g. HTTP POST) and your agent has no need to respond to any of the events in the envelope (i.e. the agent is ignoring it) then return an envelope with an _event_ object containing an empty array.(i.e. an array with no events in it).

## 3 JSON Envelope Schema

The structure of a JSON conversation envelope is defined as a JSON Schema located at [https://github.com/open-voice-interoperability/docs/tree/main/schemas/conversation-envelope/1.1.0/conversation-envelope-schema.json]

## 4 References

[1] **Interoperability of Conversational Assistants** [https://openvoicenetwork.org/docs/interoperability-of-conversational-assistants/] \
[2] **Interoperable Dialog Event Object Specification Version 1.0.2** [https://github.com/open-voice-interoperability/docs/blob/main/specifications/DialogEvents/1.0.2/InteropDialogEventSpecs.md] \
[3] **IETF RFC 9110 HTTP Semantics.** [https://datatracker.ietf.org/doc/html/rfc9110/] \
[4] **Assistant Manifest Specification Version 1.0.1** [https://github.com/open-voice-interoperability/docs/blob/main/specifications/AssistantManifest/1.0.1/AssistantManifestSpec.md] \
[5] **IETF RFC 8141 Uniform Resource Names (URNs)**[https://datatracker.ietf.org/doc/html/rfc8141] \
[6] **IETF RFC 4151 The Tag URL Scheme**[https://www.rfc-editor.org/rfc/rfc4151] \
[7] **AI Multi-Agent Interoperability Extension for Managing Multiparty Conversations.** [https://arxiv.org/abs/2411.05828]
[8] **W3C Speech Synthesis Markup Language (SSML) Version 1.1** [https://www.w3.org/TR/speech-synthesis11/]

## 5 Glossary of Terms

|Term|Definition|
|-|-|
|channeling|A conversational assistant acts as an intermediary between a user and another conversational assistant, passing through requests and returning responses. The intermediary assistant will often make no modifications to the requests or the responses but may do so, for example, increasing the speed or volume or even translating between languages.   
|confidence |A number representing a measure of the confidence that the information contained in the associated value is ‘correct’.
|conversation floor manager|A component that manages which conversants are active in a given conversation and which agent is the current focal agent. 
|delegation|A conversational assistant passes control and management of the dialog to another conversational assistant, along with a negotiated amount of context and dialog history. 
|derived specification|A derivative standard, built upon this specification, which defines a specific way to use a dialog event in a particular context.
|dialog event |A linguistic event in a spoken or written monologue or dialog between two or more speakers.  
|dialog event feature |A layer of information of a certain type associated with the dialog event.
|dialog event object|A JSON object encoding a dialog event as part of an interface to a natural language component in a text or speech processing solution or dialog system.
|dialog event object id |The unique identifier of the dialog event object
|dialog event span|Identifies the span of time for the dialog event
|dialog event speaker id|A unique id of the human or machine associated with content of the dialog event
|envelope|Structured data (hierarchical structure of data names and values) used to describe events to be communicated by a speaker or agent in a conversation.  Envelopes can contain multiple ordered events to support simple protocols such as HTTPS where servers can only respond with a single response to a single request.
|feature mime type|The type of token values in a specific dialog event feature.
|feature token|A representation of part of the information that makes up a feature value.  
|focal agent|The agent that is currently tasked with responding to agent input.
|JSON path |An unambiguous reference to part of a JSON object.
|language code|A code representing the language (e.g., American English, British English, New Norsk, etc.)
|mandatory elements|The mandatory elements that are required in the various elements of the envelope in order to be Open-Floor compliant.  These elements are enough to allow basic no-frills interoperation between agents.
|mediation|A conversational assistant acting as a user, has a conversation with another conversational assistant behind the scenes using dialog – semantic or linguistic – interfaces to achieve a goal and return to the user.
|stand-off-annotation |A method of feature layering and cross-referencing that permits the different features of an utterance or linguistic event to be kept separate but also linked logically and temporally with each other.  
|token encoding|The specific encoding used to represent text in a token.
|token link|A link from one token in a feature to part or all of another token in a feature used to implement stand-off annotation.
|token object|A JSON object representing a feature token which defines the value of the feature and other associated information such as its span and how it links to other feature tokens.
|token span|Identifies the span of time for an individual token object
|user proxy agent|A component that implements converts between a human user interacting via certain media into Open-Floor-compliant dialog envelopes and renders utterances from other conversants back to the human user in the appropriate media.

## 6 Decision Log

This section documents some of the key design decisions that were made by the team during the development of this specification.  It is informative, not normative.

|Issue Topic|Issue/Decision|
|-|-|
|Using JSON rather than other representations.|_Question:_ Why JSON and not other formats? (i.e. XML). </br>_Answer:_ JSON is Open and Human Readable Standard format for Data Exchange well suited for API designed for communications. JSON is a data format that extends from JavaScript. It does not use tags, which makes it more compact and easier to read for humans. JSON can represent the same data in a smaller file size for faster data transfer.  Furthermore JSON parsing is safer than XML, which leads JSON as the preferred format for secure communications among Conversational agents.
|Addressing Multiple Targets|_Question_: How might envelopes address more than one target? We are trying to use the envelopes to allow one agent to send events to more than one destination.</br>_Answer:_ Every event now carries an optional 'to' section allowing each event to be addressed to a different agent or conversant.|
|Go-Back|_Question:_ How can control be passed back to a previous agent?</br>_Answer:_ There is no explicit 'go-back' event or concept.  The _yeildFloor_ event supports the passing of reasons such @complete or @timedOut.   Control can be explicitly passed back to a previous agent through an explicit invite from the current focal agent.  Alternatively, the conversation floor manager can generate an invite to bring a 'favored' agent into the conversation, for example, where the current focal agent is not meeting expectations for conversational interaction.
|Control flow and exceptions|_Question:_ How do we handle timeouts and what is responsible for them?</br>_Answer:_ There is no mandated behavior regarding timeouts and exceptions.   Each conversation floor manager can choose the behavior in this regard.  The @timedOut reason is explicitly supported for yieldFloor, revokeFloor and uninvite.  This allows a conversant to yeild the floor if they time out or the floor to decide to revoke the floor or uninvite an agent if certain time expectations are not met. |
|Host Browsers and User Proxies|_Question:_ Is the host browser a user proxy or does it have unique responsibilities for control?</br>_Answer:_ The host browser is a close coupling of a user proxy and a conversation floor manager.  User proxies and floor managers can be implemented separately and communicate using dialog envelopes.  This has not been fully proven yet and there are likely to be additional control structures needed to fully support the separation.  We anticipate that early adoption of this standard will require a unified host browser.|
|location of schemas|_Question:_ Where should we publish the schema?</br>_Answer:_ Let's use https://github.com/open-voice-interoperability/lib-interop/tree/main/schemas, but add a new subfolder for each version (e.g. "1.0.1" for the current schemas).|
|reply_to |_Question_: Should reply_to be optional, mandatory (or removed)?</br>_Answer:_ The reply_to element appears to have become redundant and was retired out of the specification in version 9.9.2.|
|How are conversations started?|_Question:_ Thre is nothing in the envelope spec to allow a conversant to initiate a conversation.  How do conversations start?</br>_Answer:_ This is missing for a reason.  If the specification is used with the model of a floor running as the HTTP client and agents being HTTP servers then all agent activity needs to be in response to a POST.  For now, it is assumed that implementation of the current version of the specification will have a combined proxy agent and conversation floor manager and the initiation of a dialog will be a proprietary feature of that combined component.  If the userProxy agents are able to initiate events then a 'start' event (or some similar name) could be added in later versions of the specification.  Such an event would for example, come from the proxy agent to the conversation floor manager and result in the creation of a conversationId.Another alternative is that the floor Invites the user to the conversation - but that would require the protocol used to support long wait times until the response is received.  in short we may need a different protocol that supports truly asynchronous messaging in order to implement the separation of the floor and proxy agent.|
|Interruptions and Univiting agents.|_Question:_ How does one conversation stop the operation of another conversant?  For example, how might a user tell an agent to be quiet?  </br>_Answer:_  The event types: _uninvite_ and _revokeFloor_ support this pattern. The spec is silent about whether _revokeFloor_ should caus a real-time interruption of spoken output or revoke the floor at the end of the user utterance.|
|Multi-conversant support|_Question:_ How might this specification be extended to support multiple conversant support? </br>_Answer:_  This specification fully anticipates that the conversation floor manager could support multiple conversants.   Features to support this.</br> - Uninviting conversants (See above)</br> - Adding the to section events (to allow one conversant to specifically address another specific conversant).</br> - Adding a speakers section to the conversation object to keep track of the speakers in the conversation including their speakerUris, URLs, displayNames, and spokenNames.</br> - Adding floor management events.
|candidateAssistants|_Question_: should we rename this to be _publishManifests_ to follow the pattern that events are generally a verb phrase not a noun phrase?<br>_Answer_: It was agreed to rename this _publishManifests_.|
|'to' destinations|_Question_: There is an urgent need to agree how to express 'to' and discuss exactly how the addressing of events is managed.  <br>_Answer_: We have added an optional 'to' parameter to all events.  Agents should respond to events that do not have a 'to'section or are addressed directly to them.|
|responseCode|_Question_: This is anachronistic and may not be useful. We need to know how current users are using this parameter and considering retiring it.<br>_Answer_: We decided to deprecate the responseCode and allow the use of envelopes with empty events to act as an acknowledgement where no action is required.  Also introduced _reason_ keys on each event.|
|discovery or servicing agent in manifest|_Question_: Should manifests have explicit coding for whether an agent can provide discovery services or not? </br> _Answer_: We have deliberately left this out for now, but if we need it, we will consider additional flags on the manifest in some form.|
|speakerUri uniqueness|_Question_:Who allocates unique SpeakerIDs?  Is it the 'floor' (or client) or the agent server?<br>_Answer_: Agents should have a universal unique SpeakerId.  This will be stored in the manifest.  To guarantee uniqueness we renamed this _speakerUri_.  See the section on agent identity in the document.|
|private flag in _to_|_Question:_ Should the private flag be inside the _to_ section because it has no meaning if there is no _to_section.<br>_Answer:_ Yes|
|speakerUris in invites|_Question:_Should we allow/expect speakerUris in invites? <br>_Answer:_ These are optionally allowed. If present it will mean that the inviting agent has either received the manifest or has spoken with the agent previously. The receiving agent can ignore this parameter, especially if it not valid.|
|speakerUri in sender|_Question:_ Do we need a speakerUri in the sender parameter as well?<br>_Answer:_Yes and it is now mandatory.|
|keeping _dialogHistory_ safe|_Question_: To what extent is it safe to put dialog history into invites and findAssistant messages?<br>_Answer_: This is left to the discretion of the sender by creating a separate _context_ event type under the control of the sender.  This is similar to a warm transfer in a real telephone conversation. The consensus was that it is probably safe to pass on the last few turns as-if the target agent had been at the table. i.e. obscure any messages that this agent is not cleared to have visibility of , for example, because they were private.  More discussion will probably be needed on this issue as use cases emerge.|
|whispers or private utterances|_Question_:Now that _dialogEvent_ parameters are embedded in events such as _invite_ and there is support for the _private_ parameter in the _to_ section of an _utterance_ event, can we retire _whisper_ in favor of private _utterance_ events instead??<br>_Answer:_ Yes. The _whisper_ event has been removed.  The concept remains.|
|_context_ in dialogEvents|_Question:_ We added -context- into dialog events to support context on utterances. The intention was that this would allow the passing of context in such a way that things like language type and dialect were fully supported. However it is located outside of the 'text' feature so that is not correct.   Would we not be better simply removing _context_ as a specific extension to dialog events and considering adding 'instruct' and 'context' dialogEvent parameters to events like _invite_ rather than the generic _dialogEvent_?   That way we can more directly support the established LLM paradigm of instructions and context in all messages where _dialogEvents_ are used to convey instructions from one agent to another.<br>_Answer:_It was agreed that context would become a separate dialog event with one standard parameter (dialogHistory) and permitting any arbitrary additional keys and data structures.| 
|_to_ on _utterance_ gives away floor?|_Question:_Does _to_ on an utterance imply giving the floor to the receiver?<br>_Answer:_This remains undefined for now.|
|Size of conversation object|_Question:_ Do we need to worry about the size of the conversation object and should we allow full manifests and unlimited persistentState objects etc.<br>_Answer_ The size of the conversation object is not a great concern.  We will allow the conversant section to optionally contain the capabilities.|
|persistentState|_Question:_ Do we need to keep the persistent state? Should clients modify it directly or should there be a separate event and use the floor to modify it?<br>_Answer:_PersistentState has been removed from the specification as it was recognized that it may not be useful and may have serious state management issues when used in a multi-party conversation. Most agents will utilize their own session management based on conversation ID.|
|should _to_ always be present?|_Question_:Should we insist on a _to_ in all events and have an explicitly way of indicating 'all'?  <br>_Answer:_ If _to_ is omitted then the event is intended for all recipients.  This allows simple systems with one user and one agent to simply omit the _to_ section.|
|Include "reason" in all events|_Question_:Why not allow an optional "reason" parameter in all events? It might not be as helpful in all events, but we might as well allow it for simplicity.<br>_Answer_: Agreed - make reason an optional key in all events and allow it to be open text with special reserved words in the form '@timed-out'. Include a list of supported reserve words and also indicate in individual events how these reserved words might apply in that context.|
|Arbitrary text in "reasons"|_Question:_ Should we let "reasons"  contain arbitrary text?</br>_Answer_: Yes. We will make reason an optional key in all events and allow it to be open text with special reserved words in the form '@timed-out'. Include a list of supported reserve words and also indicate in individual events how these reserved words might apply in that context.|
|Are manifest accretive?|_Question_:  When reading section 1.15 of the Conversational Envelope I was wondering. Who are the participants that should receive a publishManifests message In case you have a sequence: Agent A - Agent B - Agent C. So A invites B and B invites C. Hence, A may not know about C but only B. How is this to be reflected in the manifest as the capabilities of C will add to those of B?<br>_Answer:_ No we are not anticipating that manifests will be cumulative. The envelope contains a 'conversants' section in the 'conversation' area. For each conversants we keep partial manifests containing the 'identity' information for each agent. Thus any party to the conversation can request full manifest information from any conversant at any time. So if tasks are delegated round-table to other agents then it is clear that the other agent is providing this service and you can use their manifest directly in this case. If an agent is using the services of other agents behind the scenes then this is their private affair. We expect an agent to include in its manifest the range of services that it offers regardless of how it provides this. So if an agent is general purpose and is 'rebadging' the services of other agents then the their manifest should explain that they are a general purpose agent. We are not currently anticipating that manifests will be dynamic in nature depending context. We are expecting that manifests might be updated as capabilities change.|
|Declining invites|_Question_:Section 1.13 of the Conversational Envelope specification describes the invite event. Can an invite be rejected? If yes, how can this be done? I remember a busy-out method in the times of IVRs. The purpose was to complete ongoing calls and not to accept new calls, e.g., if the system should go down for maintenance. Is there something comparable?<br>_Answer:_ Added a bare event 'declineInvite'|

## 7 Document Change Log

|Version|Release Date|Description|
|-|-|-|
|0.9.0|2024.01.16|Initial Published Draft|
|0.9.1|2024.04.16|- Added a new section introducing discovery</br>- Merged the 'Representation' section into the 'Syntax and Protocol' section. </br>- Replaced code example images with text</br>- Added PersistentState which was accidentally omitted from 0.9.0| 
|0.9.2|2024.07.03|- Added getManifests event</br> - Added publishManifests event</br> - Added requestManifest event</br> - Added publishManifests event </br>- Deprecated responseCode</br>- Made "to" optional on all events</br>- Removed inline schema and kept a link instead.</br>- Removed reply_to</br>|  
|0.9.3|2024.11.26|- Added private to event objects</br>- Added context parameter to whisper</br>|
|0.9.4|2025.05.13|- Changed speakerId to be speakerUri <br>- Make "to" a dictionary containing "serviceUrl" and "speakerUri" in all events</br> - Added section on identity and speakerUri</br>- Add 'floorYield" to mirror "floorRevoke"<br> - Added conversants section<br>- Added the requirement for speakerUri to be unique and persistent for each agent<br>- Removed the need for url to uniquely identify an agent<br>- Refactored requestManifest into a unified findAgent<br>- Added recommendScope to findAgent<br>- Changed publishManifests to return full array of manifests not just the synopsis<br>- Move private into 'to' of the event<br>- Added 'speakerUri' into the 'sender'<br>- Rename serviceEndpoint to serviceUrl and also rename 'url' as 'serviceUrl' in sender and to objects.<br> - Add optional "dialogHistory" section to _Invite_ and _getManifests_ events.<br>- Limit conversants to identification section only.<br>- Move persistent state into the conversant section<br>- Added section on multi-party conversations.<br>- Added description for _requestFloor_ and make it informative not normative.<br>- Added description for _grantFloor_ and make it informative not normative.<br> - Added a description for _revokeFloor_ and normative reason labels <br>- Change the score on _proposeAgent_ to be between 0 and 1.  <br>- uninvite : add description for the uninvite. <br>- Add categories for the _uninvite_ reason.<br> - remove _whisper_ in favor or private _utterance_ and embedded _dialog_events_ </br>- created a top-level context event containing a dialogHistory parameter and leaving it open for other random data to be in there. </br>- removed dialogEvent from all sub-events apart from dialogHistory and utterance </br> - re-instated getManifests, publishManifests, describeAssistant (and publishManifests)</br>- retired context in dialogEvent</br>- make it clear in the spec that utterances can be private or not and that private utterances are whispers. </br>- retire requestManifest  </br>- renamed findAssistant to be getManifests. return publishManifests.</br>- made recommendScope default to internal </br>- made -servicingManifests and discoveryManifests optional in publishManifests. </br>- made reason an optional key in all events</br>- defined special reserved key words in the _reason_ key.</br>- specified which reserved _reason_ keywords applied in which events.- Introduced a separate bare event 'declineInvite' </br> - renamed the spec as Open-floor Inter-Agent Message Specification with the key: "openFloor"|
|1.0.0|2025.05.14|-Released version 0.9.4 as 1.0.0 with final proof read</br>-Moved artwork into this repository|
|1.0.1|2026.01.13|- Added assignedFloorRoles</br>- Added floorGranted section to conversation object</br>- Added convener to assignedFloorRoles</br>- Added acceptInvite</br>- Moved dialogHistory into Invite event</br>- Removed Context event</br>- Expanded the multi-party conversation section including Convener and Floor Management sections.</br>- Removed persistentState from conversants</br>- Clarified the role of the floor manager in section 0.4.3</br>- Completed the floor management minimal behaviour including:</br>&nbsp;&nbsp;- Ignoring the privacy flag for all events apart from utterance.</br>&nbsp;&nbsp;- Simplify the table to a simple delegate/pass-through</br>&nbsp;&nbsp;- Define how requestFloor is translated into grantFloor/revokeFloor.</br>&nbsp;&nbsp;- Specify the processing order of events|
|1.1.0|2026.01.13|Version 1.0.1 up-issued and released as Version 1.1|