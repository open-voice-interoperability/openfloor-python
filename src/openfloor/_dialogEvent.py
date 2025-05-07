import yaml
import json
import xml.etree.ElementTree as ET
from datetime import datetime
from jsonpath_ng import jsonpath, parse

# standard element names
ELMNT_speakerId='speakerID'
ELMNT_ID='id'
ELMNT_PREV_ID='previousId'
ELMNT_FEATURES='features'
ELMNT_mimeType='mimeType'
ELMNT_LANG='lang'
ELMNT_ENCODING='encoding'
ELMNT_TOKENS='tokens'
ELMNT_VALUE='value'
ELMNT_VALUE_URL='value-url'
ELMNT_LINKS='links'
ELMNT_CONFIDENCE='confidence'
ELMNT_HISTORY='history'  
ELMNT_START='startTime'
ELMNT_startOffset='startOffset'
ELMNT_END='endTime'
ELMNT_endOffset='endOffset'
ELMNT_SPAN='span'

class DialogPacket():
    '''class variables'''
    _feature_class_map={}
    _value_class_map={}

    '''Construct a packet'''
    def __init__(self,p={}):
        #print(f'p: {p}')
        self._packet={}
        #print(f'A1: {self.packet}')

    ### Getters and Setters ###
    # property: packet
    @property
    def packet(self):
        return self._packet

    @packet.setter
    def packet(self,p):
        self._packet=p

    @classmethod
    # return the feature class for the mimeType
    def add_feature_class(cls,mimeType,feature_class):
        cls._feature_class_map['mimeType']=feature_class

    @classmethod
    def add_default_feature_classes(cls):
        cls.add_feature_class('text/plain',TextFeature)

    @classmethod
    # return the feature class for the mimeType
    def feature_class(cls,mimeType):
        try:
            return cls._feature_class_map['mimeType']
        except:
            return Feature    

    @classmethod
    # return the feature class for the mimeType
    def value_class(cls,mimeType):
        try:
            return cls._value_class_map['mimeType']
        except:
            return str  

    ### Built-Ins ###
    def __str__(self):
        return str(self._packet)

    def __repr__(self):
        return repr(self._packet)

    ### Convert to/from JSON and YML ###
    '''Load the packet from a string or file handle. Also takes optional arguments for yaml.safe_load().'''
    def load_yml(self,s,**kwargs):
        self._packet=yaml.safe_load(s,**kwargs) 

    '''Convert the packet to YML and optionally save it to a file. Returns a string containing the YML. Also takes optional arguments for yaml.safe_dump().'''
    def dump_yml(self,file=None,**kwargs):
        if file:
            return yaml.safe_dump(self._packet,file,**kwargs)
        else:
            return yaml.safe_dump(self._packet,**kwargs)

    '''Load the packet from a string or file handle. Also takes optional arguments for yaml.safe_load().'''
    def load_json(self,s,**kwargs):
        self._packet=json.load(s,**kwargs) 

    '''Convert the packet to JSON and optionally save it to a file. Also takes optional arguments for json.dumps().'''
    def dump_json(self,file=None,**kwargs):
        kwargs.setdefault('default', str)
        kwargs.setdefault('indent', 4)
        
        s=json.dumps(self._packet,**kwargs)
        if file: file.write(s)
        return s

class Span(DialogPacket):
    ### Constructor ###
    '''Construct an empty dialog event'''
    def __init__(self,startTime=None,startOffset=None,endTime=None,endOffset=None,endOffset_msec=None,startOffset_msec=None):
        super().__init__()
        if startTime is not None: 
           self.startTime=startTime
        if self.startOffset is not None:
           self.startOffset=startOffset
        if startOffset_msec is not None:
           self.startOffset=f'PT{round(startOffset_msec/1000,6)}'
        if endTime is not None: 
           self.endTime=endTime
        if endOffset is not None:
            self.endOffset=endOffset   
        if endOffset_msec is not None:
           self.endOffset=f'PT{round(endOffset_msec/1000,6)}'

    # property: startTime
    @property
    def startTime(self):
        return self._packet.get(ELMNT_START,None)

    @startTime.setter
    def startTime(self,s):
        self._packet[ELMNT_START]=s

    # property: endTime
    @property
    def endTime(self):
        return self._packet.get(ELMNT_END,None)

    @endTime.setter
    def endTime(self,s):
        self._packet[ELMNT_END]=s

    # property: startOffset
    @property
    def startOffset(self):
        return self._packet.get(ELMNT_startOffset,None)

    @startOffset.setter
    def startOffset(self,s):
        self._packet[ELMNT_startOffset]=s

    # property: endOffset
    @property
    def endOffset(self):
        return self._packet.get(ELMNT_endOffset,None)

    @endOffset.setter
    def endOffset(self,s):
        self._packet[ELMNT_endOffset]=s

class DialogEvent(DialogPacket):
    ### Constructor ###
    '''Construct an empty dialog event'''
    def __init__(self):
       super().__init__()

    # property: speeaker_id
    @property
    def speakerId(self):
        return self._packet.get(ELMNT_speakerId,None)

    @speakerId.setter
    def speakerId(self,s):
        self._packet[ELMNT_speakerId]=s

    # property: id
    @property
    def id(self):
        return self._packet.get(ELMNT_ID,None)

    @id.setter
    def id(self,s):
        self._packet[ELMNT_ID]=s

    # property: prevous_id
    @property
    def previous_id(self):
        return self._packet.get(ELMNT_PREV_ID,None)

    @previous_id.setter
    def previous_id(self,s):
        self._packet[ELMNT_PREV_ID]=s

    # property: features
    @property
    def features(self):
        return self._packet.get(ELMNT_FEATURES,None)

    @features.setter
    def features(self,s):
        self._packet[ELMNT_FEATURES]=s

    # property: span
    @property
    def span(self):
        return self._packet.get(ELMNT_SPAN,None)

    @span.setter
    def span(self,s):
        self._packet[ELMNT_SPAN]=s
        print(f'self._packet[ELMNT_SPAN]: {self._packet[ELMNT_SPAN]}')

    ### Add/Get span
    def add_span(self,span):
        if self.span is None:
            self.span={}    
        self.span=span.packet
        print(f'self.span:{self.span}')
        return span  

    ### Add/Get Features ###
    def add_feature(self,feature_name,feature):
        if self.features is None:
            self.features={}
        
        self.features[feature_name]=feature.packet
        return feature

    def get_feature(self,feature_name):
        fpacket=self.features.get(feature_name,None)
        
        if fpacket is not None: 
            feature=self.feature_class(fpacket.get(ELMNT_mimeType,None))()
            feature.packet=fpacket
            return feature
        else:
            return None

class Feature(DialogPacket):
    ### Constructor ###

    '''Construct a dialog event feature'''
    def __init__(self,mimeType=None,lang=None,encoding=None,p={},**kwargs):
        #print(f'Feature() kwargs: {kwargs}')
        super().__init__(**kwargs)        
        #print(f'A2: {self.packet}')
        self._token_class=Token
        
        if mimeType is not None: 
            self._packet[ELMNT_mimeType]=mimeType
        if lang is not None:
            self._packet[ELMNT_LANG]=lang
        if encoding is not None:
                self._packet[ELMNT_ENCODING]=encoding
        
        #Create the empty array of arrays for the tokens.
        self._packet[ELMNT_TOKENS]=[]

    def add_token(self, **kwargs):
        my_token=self._token_class(**kwargs)
        self.tokens.append(my_token.packet)
        return my_token

    def get_token(self,token_ix=0):
        try:
            token=self._token_class()
            token.packet=self.tokens[token_ix]
        except:
            token=None
        return token

    ### Getters and Setters ###
    # property: mimeType
    @property
    def mimeType(self):
        return self._packet.get(ELMNT_mimeType,None)

    # property: lang
    @property
    def lang(self):
        return self._packet.get(ELMNT_LANG,None)

    # property: encoding
    @property
    def encoding(self):
        return self._packet.get(ELMNT_ENCODING,None)

    # property: tokens
    @property
    def tokens(self):
        return self._packet.get(ELMNT_TOKENS,None)
    
#Note need to debug default argument overrides.
class TextFeature(Feature):
    def __init__(self,**kwargs):
        #print(f'Text Feature() kwargs: {kwargs}')
        super().__init__(mimeType='text/plain',**kwargs)
        #print(f'A3: {self.packet}')
        self._token_class=Token

class AudioWavFileFeature(Feature):
    def __init__(self,**kwargs):
        #print(f'Text Feature() kwargs: {kwargs}')
        super().__init__(mimeType='audio/wav',**kwargs)
        #print(f'A3: {self.packet}')
        self._token_class=Token

class Token(DialogPacket):
    ### Constructor ###
    '''Construct a dialog event token.'''
    def __init__(self,value=None,value_url=None,links=None,confidence=None,startTime=None,startOffset=None,endTime=None,endOffset=None,endOffset_msec=None,startOffset_msec=None):
        super().__init__()

        if value is not None: 
            self.value=value
        if value_url is not None:
            self._packet[ELMNT_VALUE_URL]=value_url
        if links is not None:
            self._packet[ELMNT_LINKS]=links
        if confidence is not None:
            self._packet[ELMNT_CONFIDENCE]=confidence   
        if startTime is not None or startOffset is not None or endTime is not None or endOffset is not None or endOffset_msec is not None or startOffset_msec is not None:
            self.add_span(Span(startTime=startTime,startOffset=startOffset,endTime=endTime,endOffset=endOffset,endOffset_msec=endOffset_msec,startOffset_msec=startOffset_msec))
    
    ### Getters and Setters ###
    @property
    def value(self):
        return self._packet.get(ELMNT_VALUE,None)

    @value.setter
    def value(self,value):
        self._packet[ELMNT_VALUE]=value   

    @property    
    def confidence(self):
        return self._packet.get(ELMNT_CONFIDENCE,None)

    @confidence.setter
    def confidence(self,confidence):
        self._packet[ELMNT_CONFIDENCE]=confidence  

    # property: span
    @property
    def span(self):
        return self._packet.get(ELMNT_SPAN,None)

    @span.setter
    def span(self,s):
        self._packet[ELMNT_SPAN]=s
        print(f'self._packet[ELMNT_SPAN]: {self._packet[ELMNT_SPAN]}')

    @property
    def links(self):
        return self._packet.get(ELMNT_LINKS,None)

    @links.setter
    def links(self,links):
        self._packet[ELMNT_LINKS]=links   

    ### Add/Get span
    def add_span(self,span):
        if self.span is None:
            self.span={}    
        self.span=span.packet
        print(f'self.span:{self.span}')
        return span  
    
    ### Get linked values
    def linked_values(self,dialog_event):
        values=[]
        for l in self.links:
            print(f'l: {l}')
            jsonpath_expr = parse(l)
            for match in jsonpath_expr.find(dialog_event.features):
                if match:
                    values.append([match.full_path,match.value])
        return values

class History(DialogPacket):
    ### Constructor ###
    '''Construct a dialog history object token.'''
    def __init__(self):
        super().__init__()
        
        #Create the empty array of dialog events
        self._packet[ELMNT_HISTORY]=[]

    def add_event(self, dialog_event):
        self._packet[ELMNT_HISTORY].append(dialog_event)
        return dialog_event

    def get_event(self,ix=0):
        try:
            event=DialogEvent()
            event.packet=self._packet[ELMNT_TOKENS][ix]
        except:
            event=None
        return event