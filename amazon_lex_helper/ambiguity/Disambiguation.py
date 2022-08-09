from abc import abstractmethod

from amazon_lex_helper import LexEvent

import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Ambiguation threshold, if the two highest intent scores are within this interval, we trigger disambiguation
AMBIGUITY_LIMIT = 0.15


class Disambiguation:

    def __init__(self, ambiguity_limit=AMBIGUITY_LIMIT):
        self.ambiguity_limit = ambiguity_limit

    def check_ambiguity_limit (self, req: LexEvent) -> dict:
        """
        Checks ambiguity, and returns ambiguity details if diff is greater than AMBI
        :param req: Lex request
        :return: the ambiguity details as (first_intent, second_intent, amibiguity_diff) or None if no ambiguity
        """
        interpretations = req.get_interpretations()
        if not interpretations or len(interpretations) < 2:
            return None
        interpretations = sorted(interpretations, key=lambda x: float(x.get('nluConfidence') or 0), reverse=True)
        ambiguity_diff = float(interpretations[0].get('nluConfidence') or 0) - float(interpretations[1].get('nluConfidence') or 0)
        return {"i1":interpretations[0], "i2":interpretations[1], "amb":ambiguity_diff} if ambiguity_diff < self.ambiguity_limit else None

    @abstractmethod
    def handle_ambiguity(self, intent_1, intent_2, ambiguity_diff):
        pass
