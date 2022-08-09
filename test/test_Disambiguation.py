import json
import unittest
import pkg_resources

from amazon_lex_helper import LexEvent
from amazon_lex_helper import Disambiguation


class DisambiguationTests(unittest.TestCase):

    def test_ambiguity_limit_below_threshold (self):
        path = 'samples/trade.json'
        full_path = pkg_resources.resource_filename(__name__, path)
        with open(full_path) as json_file:
            json_data = json.load(json_file)
            req = LexEvent(json_data)
            d = Disambiguation(0.2)
            ambiguity_data = d.check_ambiguity_limit(req)
            self.assertIsNone(ambiguity_data)

    def test_ambiguity_limit_over_threshold (self):
        path = 'samples/trade.json'
        full_path = pkg_resources.resource_filename(__name__, path)
        with open(full_path) as json_file:
            json_data = json.load(json_file)
            req = LexEvent(json_data)
            d = Disambiguation(0.5)
            ambiguity_data = d.check_ambiguity_limit(req)
            self.assertIsNotNone(ambiguity_data)