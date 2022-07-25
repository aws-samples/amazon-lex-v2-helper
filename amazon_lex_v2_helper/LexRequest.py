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
This class is compatible with Amazon Lex V2 data structure.
It allows to retrieve specific attributes of the object by means of getter methods
and to modify attributes by means of setters.
"""


class LexRequest:

    def __init__(self, request):
        self.req = request

    def is_input_user_request(self):
        return self.req.get("invocationSource") == "DialogCodeHook"

    def intent_is_fulfilled (self):
        return self.req.get("invocationSource") == "FulfillmentCodeHook"

    def get_input_mode (self):
        return self.req.get("inputMode")

    def get_input_transcript (self):
        return self.req.get("inputTranscript")

    def get_session_attr (self, attr):
        return self.req["sessionState"]["sessionAttributes"].get(attr)

    def set_session_attr(self, attr, attr_val):
        self.req["sessionState"]["sessionAttributes"][attr] = attr_val
        return self

    def get_session_attrs(self):
        return self.req["sessionState"].get("sessionAttributes")

    def get_current_intent_slot (self, slot_name):
        current_intent_slots = self.req['currentIntent']['slots']
        return current_intent_slots.get(slot_name)

    def get_interpretations(self):
        return self.req.get("interpretations")

    def get_confirmation_state (self):
        return self.req["sessionState"]["intent"].get("confirmationState")

    def is_confirmed(self):
        return self.get_confirmation_state() == "Confirmed"

    def get_slot(self, slot_name):
        return self.req['sessionState']['intent']["slots"].get(slot_name)

    def get_current_intent(self):
        return self.req['sessionState']['intent']
