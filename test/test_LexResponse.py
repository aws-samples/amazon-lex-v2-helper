from unittest import TestCase
from amazon_lex_helper import LexEvent, LexResponse
import pkg_resources
import json


class LexResponseTests (TestCase):

    def test_delegate_returns_not_null (self):
        path = 'samples/trade.json'
        full_path = pkg_resources.resource_filename(__name__, path)
        with open(full_path) as json_file:
            json_data = json.load(json_file)
            req = LexEvent(json_data)
            resp = LexResponse.delegate(req)
            self.assertIsNotNone(resp)
