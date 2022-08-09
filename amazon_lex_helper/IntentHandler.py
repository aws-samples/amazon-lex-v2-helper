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

import logging
from abc import abstractmethod

from amazon_lex_helper import LexEvent

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


class IntentHandler:
    """
    Handles a Lex event received by the dispatcher.
    Each intent handler is subscribed to the dispatcher by intent name, so only one handler is allowed for each
    of the intents defined in the Lex bot.
    """
    def __init__(self, intent_name):
        self.intent_name = intent_name

    def get_intent_name(self):
        return self.intent_name

    @abstractmethod
    def process_request(self, request: LexEvent):
        pass

    def log(self):
        return logger

    def valid_intent(self, lex: LexEvent):
        valid = False
        slots = lex.get_session_slots()
        if slots:
            none_slots = [slot_name for slot_name in slots if not slots[slot_name]]
            logger.debug("intent list = {}".format(none_slots))
            valid = len(none_slots) == 0
        return valid