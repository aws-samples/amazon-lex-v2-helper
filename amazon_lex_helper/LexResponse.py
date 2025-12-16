"""
 Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
 SPDX-License-Identifier: MIT-0

 Permission is hereby granted, free of charge, to any person obtaining a copy of this
 software and associated documentation files (the "Software"), to deal in the Software
 without restriction, including without limitation the rights to use, copy, modify,
 merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
 permit persons to whom the Software is furnished to do so.

 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
 INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
 PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
 HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
 OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
 SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""

"""
This module is compatible with the Amazon Lex V2 data structure. 
It provides methods to build custom responses returned by the Lambda function to Amazon Lex.

For instructions on how to set up and test this bot, as well as additional samples,
visit the Lex Getting Started documentation http://docs.aws.amazon.com/lex/latest/dg/getting-started.html.
"""
from amazon_lex_helper import LexEvent
from typing import Dict, List, Optional, Union


def ask_due_to_ambiguity (req: LexEvent, intent_name, message=None):
    return elicit_intent(req, intent_name, "In Progress", message)


def elicit_intent(req: LexEvent, intent_name, state, message=None):
    resp = {
        "sessionState": {
            'activeContexts': [{
                'name': 'intentContext',
                'contextAttributes': {},
                'timeToLive': {'timeToLiveInSeconds': 600, 'turnsToLive': 1}
            }],
            'sessionAttributes': req.get_session_attrs(),
            'dialogAction': {'type': 'ElicitIntent'},
            'intent': {'name': intent_name, 'state': state},
        }
    }
    if message:
        resp['messages'] = [{'contentType': 'PlainText', 'content': message}]
    return resp


def elicit_slot(req: LexEvent, slot_to_elicit, message=None):
    resp = {
        'sessionState': {
            'activeContexts': [{
                'name': 'intentContext',
                'contextAttributes': {},
                'timeToLive': {'timeToLiveInSeconds': 600, 'turnsToLive': 1}
            }],
            'sessionAttributes': req.get_session_attrs() or {},
            'dialogAction': {
                'type': 'ElicitSlot',
                'slotToElicit': slot_to_elicit
            },
            'intent': req.get_intent()
        }
    }
    resp['sessionState']['intent']['slots'][slot_to_elicit] = None # clear any existing slot value
    if message:
        resp['messages'] = [{'contentType': 'PlainText', 'content': message}]
    return resp


def confirm_intent(session_attributes, active_contexts, intent, message=None):
    resp = {
        'sessionState': {
            'activeContexts': [{
                'name': 'intentContext',
                'contextAttributes': active_contexts,
                'timeToLive': {
                    'timeToLiveInSeconds': 600,
                    'turnsToLive': 1
                }
            }],
            'sessionAttributes': session_attributes,
            'dialogAction': {
                'type': 'ConfirmIntent'
            },
            'intent': intent
        }
    }
    if message:
        resp['messages'] = [{'contentType': 'PlainText', 'content': message}]
    return resp


def close(session_attributes, intent, context_attrs, message=None):
    resp = {
        'sessionState': {
            'activeContexts': [{
                'name': 'intentContext',
                'contextAttributes': context_attrs,
                'timeToLive': {
                    'timeToLiveInSeconds': 600,
                    'turnsToLive': 1
                }
            }],
            'sessionAttributes': session_attributes,
            'dialogAction': {'type': 'Close'},
            'intent': intent
        }
    }
    if message:
        resp['messages'] = [{'contentType': 'PlainText', 'content': message}]
    return resp


def delegate (req: LexEvent, slot_to_override=None, slot_value_to_override=None, message=None):
    """
    Returns the handling of the intent to Amazon Lex.
    It is possible to set the value of a specific slot at the same time to implement logics like
    'if slot s1 = X, then s2 = Y'.
    """
    session_attributes = req.get_session_attrs() or {}
    context_attrs = {}
    intent = req.get_intent()
    resp = {
        'sessionState': {
            'activeContexts': [{
                'name': 'intentContext',
                'contextAttributes': context_attrs,
                'timeToLive': {
                    'timeToLiveInSeconds': 600,
                    'turnsToLive': 1
                }
            }],
            'sessionAttributes': session_attributes,
            'dialogAction': {'type': 'Delegate'},
            'intent': intent
        }
    }
    if slot_to_override:
        resp['sessionState']['intent']['slots'][slot_to_override] = \
        {'shape': 'Scalar', 'value': {'originalValue': slot_value_to_override, 'resolvedValues': [slot_value_to_override], 'interpretedValue': slot_value_to_override}} # clear any existing slot value
    if message:
        resp['messages'] = [{'contentType': 'PlainText', 'content': message}]
    return resp


def initial_message(intent_name, welcome_message):
    """
    Provide Initial Message for Start of Flow
    """
    return  {
        "sessionState": {
            "dialogAction": {
            "type": "Close",
            },
        "intent": {
            "name": intent_name,
            "state": "Fulfilled"
        }
    },
    "messages": [
            {
            "contentType": "PlainText",
            "content": welcome_message
            }
        ]
    }


# Enhanced Message Creation Functions

def create_plain_text_message(content: str) -> Dict:
    """Create a plain text message."""
    return {
        "contentType": "PlainText",
        "content": content
    }


def create_ssml_message(ssml_content: str) -> Dict:
    """Create an SSML message for enhanced speech output."""
    return {
        "contentType": "SSML",
        "content": ssml_content
    }


def create_custom_payload_message(payload: Dict) -> Dict:
    """Create a custom payload message for platform-specific responses."""
    return {
        "contentType": "CustomPayload",
        "content": payload
    }


def create_image_response_card(title: str, subtitle: str = None, image_url: str = None, 
                              buttons: List[Dict] = None) -> Dict:
    """
    Create an image response card message.
    
    Args:
        title: Card title
        subtitle: Optional card subtitle
        image_url: Optional image URL
        buttons: Optional list of buttons with 'text' and 'value' keys
    """
    card = {
        "contentType": "ImageResponseCard",
        "imageResponseCard": {
            "title": title
        }
    }
    
    if subtitle:
        card["imageResponseCard"]["subtitle"] = subtitle
    
    if image_url:
        card["imageResponseCard"]["imageUrl"] = image_url
    
    if buttons:
        card["imageResponseCard"]["buttons"] = buttons
    
    return card


# Enhanced Response Functions with Rich Message Support

def elicit_slot_with_rich_messages(req: LexEvent, slot_to_elicit: str, 
                                  messages: List[Dict] = None, 
                                  runtime_hints: Dict = None) -> Dict:
    """
    Enhanced elicit_slot with support for multiple message types and runtime hints.
    
    Args:
        req: LexEvent object
        slot_to_elicit: Name of slot to elicit
        messages: List of message objects (PlainText, SSML, ImageResponseCard, etc.)
        runtime_hints: Runtime hints to improve speech recognition
    """
    resp = {
        'sessionState': {
            'activeContexts': [{
                'name': 'intentContext',
                'contextAttributes': {},
                'timeToLive': {'timeToLiveInSeconds': 600, 'turnsToLive': 1}
            }],
            'sessionAttributes': req.get_session_attrs() or {},
            'dialogAction': {
                'type': 'ElicitSlot',
                'slotToElicit': slot_to_elicit
            },
            'intent': req.get_intent()
        }
    }
    
    # Clear any existing slot value
    resp['sessionState']['intent']['slots'][slot_to_elicit] = None
    
    if messages:
        resp['messages'] = messages
    
    if runtime_hints:
        resp['sessionState']['runtimeHints'] = runtime_hints
    
    return resp


def elicit_intent_with_rich_messages(req: LexEvent, intent_name: str, state: str, 
                                    messages: List[Dict] = None) -> Dict:
    """Enhanced elicit_intent with support for multiple message types."""
    resp = {
        "sessionState": {
            'activeContexts': [{
                'name': 'intentContext',
                'contextAttributes': {},
                'timeToLive': {'timeToLiveInSeconds': 600, 'turnsToLive': 1}
            }],
            'sessionAttributes': req.get_session_attrs(),
            'dialogAction': {'type': 'ElicitIntent'},
            'intent': {'name': intent_name, 'state': state},
        }
    }
    
    if messages:
        resp['messages'] = messages
    
    return resp


def confirm_intent_with_rich_messages(session_attributes: Dict, active_contexts: Dict, 
                                     intent: Dict, messages: List[Dict] = None) -> Dict:
    """Enhanced confirm_intent with support for multiple message types."""
    resp = {
        'sessionState': {
            'activeContexts': [{
                'name': 'intentContext',
                'contextAttributes': active_contexts,
                'timeToLive': {
                    'timeToLiveInSeconds': 600,
                    'turnsToLive': 1
                }
            }],
            'sessionAttributes': session_attributes,
            'dialogAction': {
                'type': 'ConfirmIntent'
            },
            'intent': intent
        }
    }
    
    if messages:
        resp['messages'] = messages
    
    return resp


def close_with_rich_messages(session_attributes: Dict, intent: Dict, context_attrs: Dict, 
                            messages: List[Dict] = None) -> Dict:
    """Enhanced close with support for multiple message types."""
    resp = {
        'sessionState': {
            'activeContexts': [{
                'name': 'intentContext',
                'contextAttributes': context_attrs,
                'timeToLive': {
                    'timeToLiveInSeconds': 600,
                    'turnsToLive': 1
                }
            }],
            'sessionAttributes': session_attributes,
            'dialogAction': {'type': 'Close'},
            'intent': intent
        }
    }
    
    if messages:
        resp['messages'] = messages
    
    return resp


def delegate_with_rich_messages(req: LexEvent, slot_to_override: str = None, 
                               slot_value_to_override: str = None, 
                               messages: List[Dict] = None,
                               runtime_hints: Dict = None) -> Dict:
    """
    Enhanced delegate with support for multiple message types and runtime hints.
    """
    session_attributes = req.get_session_attrs() or {}
    context_attrs = {}
    intent = req.get_intent()
    
    resp = {
        'sessionState': {
            'activeContexts': [{
                'name': 'intentContext',
                'contextAttributes': context_attrs,
                'timeToLive': {
                    'timeToLiveInSeconds': 600,
                    'turnsToLive': 1
                }
            }],
            'sessionAttributes': session_attributes,
            'dialogAction': {'type': 'Delegate'},
            'intent': intent
        }
    }
    
    if slot_to_override:
        resp['sessionState']['intent']['slots'][slot_to_override] = {
            'shape': 'Scalar', 
            'value': {
                'originalValue': slot_value_to_override, 
                'resolvedValues': [slot_value_to_override], 
                'interpretedValue': slot_value_to_override
            }
        }
    
    if messages:
        resp['messages'] = messages
    
    if runtime_hints:
        resp['sessionState']['runtimeHints'] = runtime_hints
    
    return resp


# Runtime Hints Helper Functions

def create_runtime_hints(slot_hints: Dict[str, Dict] = None, 
                        phrase_hints: List[str] = None) -> Dict:
    """
    Create runtime hints to improve speech recognition.
    
    Args:
        slot_hints: Dictionary mapping slot names to hint configurations
        phrase_hints: List of phrases to boost recognition
    """
    hints = {}
    
    if slot_hints:
        hints['slotHints'] = slot_hints
    
    if phrase_hints:
        hints['phraseHints'] = [{'value': phrase} for phrase in phrase_hints]
    
    return hints


def create_slot_hint(values: List[str], subslot_hints: Dict = None) -> Dict:
    """
    Create a slot hint configuration.
    
    Args:
        values: List of expected values for the slot
        subslot_hints: Optional hints for subslots
    """
    hint = {
        'runtimeHintValues': [{'phrase': value} for value in values]
    }
    
    if subslot_hints:
        hint['subSlotHints'] = subslot_hints
    
    return hint
