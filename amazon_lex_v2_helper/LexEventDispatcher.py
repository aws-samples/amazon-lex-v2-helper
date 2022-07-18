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
This class is compatible with Amazon Lex V2 format.
"""
import logging

from amazon_lex_v2_helper import LexRequest

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


class LexEventDispatcher:

    def __init__(self):
        self.registered_intents = {}

    def register(self, *intents):
        for i in intents:
            target_intent = i.get_intent_name().lower()
            assert target_intent not in self.registered_intents,\
                "More than one handler for same intent: {}".format(target_intent)
            self.registered_intents[target_intent] = i
        return self

    def dispatch(self, lex_request: dict):
        intent_name = lex_request['sessionState']['intent']['name'].lower()
        response = self.registered_intents[intent_name].process_request(LexRequest(lex_request))
        logger.debug("Input request = {}".format(lex_request))
        logger.debug("Output response = {}".format(response))
        return response
