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

from typing import Dict, List, Optional, Any


class LexEvent:

    def __init__(self, request):
        self.req = request

    def get_intent_name(self) -> str:
        return self.req['sessionState']['intent'].get('name')

    def get_intent(self):
        return self.req['sessionState']['intent']

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

    def get_interpretations(self):
        return self.req.get("interpretations")

    def get_confirmation_state (self):
        return self.req["sessionState"]["intent"].get("confirmationState")

    def is_confirmed(self):
        return self.get_confirmation_state() == "Confirmed"

    def slot_exists(self, slot_name):
        return self.get_slot(slot_name) is not None

    def get_slot(self, slot_name):
        return self.req['sessionState']['intent']["slots"].get(slot_name)

    def get_slot_interpreted_value (self, slot_name):
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

    # Enhanced methods for new Lex V2 features

    def get_sentiment_analysis(self) -> Optional[Dict]:
        """
        Get sentiment analysis data from interpretations.
        Returns sentiment score and label if available.
        """
        interpretations = self.get_interpretations()
        if interpretations and len(interpretations) > 0:
            return interpretations[0].get('sentimentResponse')
        return None

    def get_transcription_confidence(self) -> Optional[float]:
        """
        Get transcription confidence score.
        Returns confidence score between 0.0 and 1.0 if available.
        """
        interpretations = self.get_interpretations()
        if interpretations and len(interpretations) > 0:
            nlu_confidence = interpretations[0].get('nluConfidence')
            if nlu_confidence:
                return nlu_confidence.get('score')
        return None

    def get_slot_values_list(self, slot_name: str) -> Optional[List[str]]:
        """
        Get all values for a multi-valued slot (shape: "List").
        Returns list of interpreted values or None if slot doesn't exist.
        """
        slot = self.get_slot(slot_name)
        if slot and slot.get('shape') == 'List':
            values = slot.get('values', [])
            return [value['value']['interpretedValue'] for value in values if 'value' in value]
        return None

    def get_slot_original_value(self, slot_name: str) -> Optional[str]:
        """
        Get the original value (as spoken/typed by user) for a slot.
        """
        slot = self.get_slot(slot_name)
        if slot and 'value' in slot:
            return slot['value'].get('originalValue')
        return None

    def get_slot_resolved_values(self, slot_name: str) -> Optional[List[str]]:
        """
        Get all resolved values for a slot.
        """
        slot = self.get_slot(slot_name)
        if slot and 'value' in slot:
            return slot['value'].get('resolvedValues', [])
        return None

    def is_multi_valued_slot(self, slot_name: str) -> bool:
        """
        Check if a slot is multi-valued (shape: "List").
        """
        slot = self.get_slot(slot_name)
        return slot is not None and slot.get('shape') == 'List'

    def get_active_contexts(self) -> List[Dict]:
        """
        Get all active contexts from the session state.
        """
        return self.req.get('sessionState', {}).get('activeContexts', [])

    def get_context_attributes(self, context_name: str) -> Optional[Dict]:
        """
        Get attributes for a specific active context.
        """
        contexts = self.get_active_contexts()
        for context in contexts:
            if context.get('name') == context_name:
                return context.get('contextAttributes', {})
        return None

    def get_bot_info(self) -> Dict:
        """
        Get bot information including name, version, and locale.
        """
        bot = self.req.get('bot', {})
        return {
            'name': bot.get('name'),
            'version': bot.get('version'),
            'locale_id': bot.get('localeId'),
            'alias_id': bot.get('aliasId')
        }

    def get_request_attributes(self) -> Dict:
        """
        Get request attributes if available.
        """
        return self.req.get('requestAttributes', {})

    def get_session_id(self) -> Optional[str]:
        """
        Get the session ID.
        """
        return self.req.get('sessionId')

    def get_user_id(self) -> Optional[str]:
        """
        Get the user ID if available.
        """
        return self.req.get('userId')

    def has_alternative_intents(self) -> bool:
        """
        Check if there are alternative intent interpretations available.
        """
        interpretations = self.get_interpretations()
        return interpretations is not None and len(interpretations) > 1

    def get_alternative_intents(self) -> List[Dict]:
        """
        Get alternative intent interpretations.
        Returns list of alternative intents with confidence scores.
        """
        interpretations = self.get_interpretations()
        if interpretations and len(interpretations) > 1:
            return interpretations[1:]  # Skip the first one (current intent)
        return []

    def get_nlu_confidence_score(self) -> Optional[float]:
        """
        Get NLU confidence score for the current intent.
        """
        interpretations = self.get_interpretations()
        if interpretations and len(interpretations) > 0:
            nlu_confidence = interpretations[0].get('nluConfidence')
            if nlu_confidence:
                return nlu_confidence.get('score')
        return None

    def is_low_confidence_intent(self, threshold: float = 0.4) -> bool:
        """
        Check if the current intent has low confidence score.
        
        Args:
            threshold: Confidence threshold (default 0.4)
        """
        confidence = self.get_nlu_confidence_score()
        return confidence is not None and confidence < threshold

    def get_slot_elicitation_style(self, slot_name: str) -> Optional[str]:
        """
        Get the elicitation style for a slot if specified in proposed next state.
        """
        proposed_state = self.req.get('proposedNextState', {})
        dialog_action = proposed_state.get('dialogAction', {})
        slot_elicitation_style = dialog_action.get('slotElicitationStyle')
        
        if (dialog_action.get('type') == 'ElicitSlot' and 
            dialog_action.get('slotToElicit') == slot_name):
            return slot_elicitation_style
        return None

    def get_input_source(self) -> Optional[str]:
        """
        Get the input source (e.g., 'Voice', 'Text').
        """
        return self.req.get('inputSource')

    def get_message_version(self) -> Optional[str]:
        """
        Get the message version.
        """
        return self.req.get('messageVersion')

    def is_voice_input(self) -> bool:
        """
        Check if the input was voice-based.
        """
        return self.get_input_mode() == 'Speech'

    def is_text_input(self) -> bool:
        """
        Check if the input was text-based.
        """
        return self.get_input_mode() == 'Text'

    def is_dtmf_input(self) -> bool:
        """
        Check if the input was DTMF (phone keypad).
        """
        return self.get_input_mode() == 'DTMF'
