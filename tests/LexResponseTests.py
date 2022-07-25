from unittest import TestCase
from amazon_lex_v2_helper import IntentHandler, LexRequest, LexResponse
from amazon_lex_v2_helper import LexEventDispatcher

import json


class LexResponseTests (TestCase):

    def test_delegate_returns_not_null (self):
        with open("samples/trade.json") as json_file:
            json_data = json.load(json_file)
            req = LexRequest(json_data)
            resp = LexResponse.delegate(req)
            print(resp)
            self.assertIsNotNone(resp)
