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


class LexEvent:

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
        satts = self.req["sessionState"].get("sessionAttributes")
        if not satts:
            self.req["sessionState"]["sessionAttributes"] = {}
            satts = self.req["sessionState"].get("sessionAttributes")
        return satts

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

    def get_current_intent_name(self) -> str:
        return self.req['sessionState']['intent'].get('name')

    def slot_exists(self, slot_name):
        return self.get_slot(slot_name) is not None

    def get_interpreted_value (self, slot_name):
        slot = self.get_slot(slot_name)
        if slot:
            return slot['value'].get('interpretedValue')
        else:
            return None

    def increase_retry(self, slot_name: str):
        attrs = self.get_session_attrs()
        attr_retry = 'retries_{}'.format(slot_name.lower())
        if attr_retry in attrs:
            attrs[attr_retry] = int(attrs[attr_retry]) + 1
        else:
            attrs[attr_retry] = 1
        return attrs[attr_retry]

    def is_requesting_slot (self, slot_name: str):
        dialog_action = self.req.get("proposedNextState").get("dialogAction")
        if dialog_action:
            type = dialog_action.get("type")
            slot_to_elicit = dialog_action.get("slotToElicit")
            return type == "ElicitSlot" and slot_to_elicit.lower() == slot_name.lower()
        return False
