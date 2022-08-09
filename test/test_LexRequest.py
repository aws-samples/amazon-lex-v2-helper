import json
import pkg_resources
from unittest import TestCase

from amazon_lex_helper import LexEvent


class LexRequestTests (TestCase):

    def test_request_is_parsed (self):
        path = 'samples/trade.json'
        full_path = pkg_resources.resource_filename(__name__, path)
        with open(full_path) as json_file:
            json_data = json.load(json_file)
            req = LexEvent(json_data)
            self.assertEqual(req.get_current_intent()['name'], "OpenFuturesIntent")
            self.assertEqual(req.get_input_transcript(), "trade")

    def test_increase_retry(self):
        path = 'samples/trade.json'
        full_path = pkg_resources.resource_filename(__name__, path)
        with open(full_path) as json_file:
            json_data = json.load(json_file)
            req = LexEvent(json_data)
            req.increase_retry("test_slot")
            req.increase_retry("test_slot")
            self.assertEqual(req.get_session_attr("retries_test_slot"), 2)

