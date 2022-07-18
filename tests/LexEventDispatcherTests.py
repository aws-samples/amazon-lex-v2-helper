from unittest import TestCase
from amazon_lex_v2_helper import IntentHandler
from amazon_lex_v2_helper import LexEventDispatcher


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

