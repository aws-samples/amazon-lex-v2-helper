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
