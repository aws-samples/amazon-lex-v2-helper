from unittest import TestCase


class LexEventDispatcherTests (TestCase):

    def test_duplicated_intent_raises_exception(self):
        a = IntentHandler()
        #event_dispatcher = LexEventDispatcher()
