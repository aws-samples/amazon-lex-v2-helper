import pkg_resources
import json
from unittest import TestCase
from amazon_lex_v2_helper import IntentHandler
from amazon_lex_v2_helper import LexEventDispatcher
from amazon_lex_v2_helper import Disambiguation
from amazon_lex_v2_helper import LexRequest

class LexEventDispatcherTests (TestCase):

    def test_duplicated_intent_raises_exception(self):
        a = IntentHandler("foo")
        b = IntentHandler("foo")
        event_dispatcher = LexEventDispatcher()
        self.assertRaises(AssertionError, event_dispatcher.register, a, b)

    def test_different_intents_are_successfully_registered(self):
        a = IntentHandler("foo")
        b = IntentHandler("bar")
        event_dispatcher = LexEventDispatcher().register(a,b)
        self.assertTrue(len(event_dispatcher.registered_intents) == 2)

    def test_use_ambiguity_handler_if_provided (self):
        path = 'samples/trade.json'
        full_path = pkg_resources.resource_filename(__name__, path)
        with open(full_path) as json_file:
            json_data = json.load(json_file)
            req = LexRequest(json_data)
            a = IntentHandler("foo")
            b = IntentHandler("bar")
            event_dispatcher = LexEventDispatcher().register(a, b)
            event_dispatcher.set_ambiguity_handler(Disambiguation(0.5))
            response = event_dispatcher.dispatch(req)

