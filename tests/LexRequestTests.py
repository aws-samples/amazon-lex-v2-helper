import json
from unittest import TestCase

from amazon_lex_v2_helper import LexRequest


class LexRequestTests (TestCase):

    def test_request_is_parsed (self):
        with open("samples/trade.json") as json_file:
            json_data = json.load(json_file)
            req = LexRequest(json_data)
            self.assertEqual(req.get_current_intent_name(), "OpenFuturesIntent")
            self.assertEqual(req.get_input_transcript(), "trade")

    def test_increase_retry(self):
        with open("samples/trade.json") as json_file:
            json_data = json.load(json_file)
            req = LexRequest(json_data)
            req.increase_retry("test_slot")
            req.increase_retry("test_slot")
            print(req.get_session_attrs())
            self.assertEqual(req.get_session_attr("retries_test_slot"), 2)

