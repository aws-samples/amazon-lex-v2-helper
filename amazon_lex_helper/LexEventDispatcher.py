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

from amazon_lex_helper import LexEvent, Disambiguation
from amazon_lex_helper import LexResponse
from os import getenv

logger = logging.getLogger()

def get_log_level():
    """
    Get the logging level from the LOG_LEVEL environment variable if it is valid.
    Otherwise set to WARNING
    :return: The logging level to use
    """
    DEFAULT_LEVEL = "WARNING"
    valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    requested_level = getenv("LOG_LEVEL", DEFAULT_LEVEL)
    if requested_level and requested_level in valid_levels:
        return requested_level
    return DEFAULT_LEVEL

logger.setLevel(get_log_level())

class LexEventDispatcher:

    def __init__(self):
        self.subscribers = {}
        self.ambiguity_handler: Disambiguation = None

    def subscribe(self, *intents):
        for i in intents:
            target_intent = i.get_intent_name().lower()
            assert target_intent not in self.subscribers,\
                "More than one subscriber for same intent: {}".format(target_intent)
            self.subscribers[target_intent] = i
        return self

    def set_ambiguity_handler (self, ambiguity_handler: Disambiguation):
        self.ambiguity_handler = ambiguity_handler
        return self

    def dispatch(self, lex_request: dict) -> LexResponse:
        logger.debug("Input request = {}".format(lex_request))
        event = LexEvent(lex_request)
        if self.ambiguity_handler:
            ambiguity = self.ambiguity_handler.check_ambiguity_limit(event)
            if ambiguity:
                return self.ambiguity_handler.handle_ambiguity (ambiguity["i1"], ambiguity["i2"], ambiguity["amb"])
        intent_name = event.get_intent_name().lower()
        if intent_name not in self.subscribers:
            logger.debug("Warning: no observer defined for intent '{}', using default behaviour".format(intent_name))
            response = LexResponse.delegate(event)
        else:
            response = self.subscribers[intent_name].process_request(event)
        logger.debug("Output response = {}".format(response))
        return response
