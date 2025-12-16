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

import logging
from abc import abstractmethod
from typing import Dict, List, Optional, Any

from amazon_lex_helper import LexEvent

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


class IntentHandler:
    """
    Enhanced intent handler for Lex V2 events.
    Each intent handler is subscribed to the dispatcher by intent name, so only one handler is allowed for each
    of the intents defined in the Lex bot.
    
    New features:
    - Enhanced slot validation
    - Multi-valued slot support
    - Sentiment analysis access
    - Confidence score handling
    - Rich message support
    """
    def __init__(self, intent_name: str):
        self.intent_name = intent_name

    def get_intent_name(self) -> str:
        return self.intent_name

    @abstractmethod
    def process_request(self, request: LexEvent) -> Dict:
        """Process the Lex request and return a response."""
        pass

    def log(self):
        return logger

    def valid_intent(self, lex: LexEvent) -> bool:
        """Check if all required slots are filled."""
        valid = False
        intent = lex.get_intent()
        if intent and 'slots' in intent:
            slots = intent['slots']
            none_slots = [slot_name for slot_name in slots if not slots[slot_name]]
            logger.debug("empty slots = {}".format(none_slots))
            valid = len(none_slots) == 0
        return valid

    def get_required_slots(self) -> List[str]:
        """
        Override this method to define required slots for the intent.
        Returns list of slot names that must be filled.
        """
        return []

    def validate_slots(self, lex: LexEvent) -> Dict[str, str]:
        """
        Validate all slots and return validation errors.
        Override this method to implement custom slot validation.
        
        Returns:
            Dictionary mapping slot names to error messages
        """
        return {}

    def handle_slot_validation_error(self, lex: LexEvent, slot_name: str, 
                                   error_message: str) -> Dict:
        """
        Handle slot validation error. Override to customize error handling.
        
        Args:
            lex: LexEvent object
            slot_name: Name of the slot with validation error
            error_message: Error message
            
        Returns:
            Lex response dictionary
        """
        from amazon_lex_helper import LexResponse
        return LexResponse.elicit_slot(lex, slot_name, error_message)

    def is_low_confidence_request(self, lex: LexEvent, threshold: float = 0.4) -> bool:
        """
        Check if the request has low confidence score.
        
        Args:
            lex: LexEvent object
            threshold: Confidence threshold
            
        Returns:
            True if confidence is below threshold
        """
        return lex.is_low_confidence_intent(threshold)

    def handle_low_confidence(self, lex: LexEvent) -> Dict:
        """
        Handle low confidence requests. Override to customize behavior.
        
        Args:
            lex: LexEvent object
            
        Returns:
            Lex response dictionary
        """
        from amazon_lex_helper import LexResponse
        return LexResponse.elicit_intent(
            lex, 
            self.intent_name, 
            "InProgress",
            "I'm not sure I understood that correctly. Could you please rephrase?"
        )

    def get_sentiment_analysis(self, lex: LexEvent) -> Optional[Dict]:
        """
        Get sentiment analysis for the current request.
        
        Args:
            lex: LexEvent object
            
        Returns:
            Sentiment analysis data or None
        """
        return lex.get_sentiment_analysis()

    def is_negative_sentiment(self, lex: LexEvent, threshold: float = 0.5) -> bool:
        """
        Check if the user sentiment is negative.
        
        Args:
            lex: LexEvent object
            threshold: Sentiment threshold
            
        Returns:
            True if sentiment is negative above threshold
        """
        sentiment = self.get_sentiment_analysis(lex)
        if sentiment and 'sentiment' in sentiment:
            sentiment_label = sentiment['sentiment']
            if sentiment_label == 'NEGATIVE':
                sentiment_score = sentiment.get('sentimentScore', {})
                negative_score = sentiment_score.get('negative', 0)
                return negative_score >= threshold
        return False

    def handle_negative_sentiment(self, lex: LexEvent) -> Optional[Dict]:
        """
        Handle negative sentiment. Override to customize behavior.
        Return None to continue with normal processing.
        
        Args:
            lex: LexEvent object
            
        Returns:
            Lex response dictionary or None to continue normal processing
        """
        # Default: continue with normal processing
        return None

    def get_multi_valued_slot(self, lex: LexEvent, slot_name: str) -> List[str]:
        """
        Get values from a multi-valued slot.
        
        Args:
            lex: LexEvent object
            slot_name: Name of the slot
            
        Returns:
            List of slot values
        """
        return lex.get_slot_values_list(slot_name) or []

    def validate_multi_valued_slot(self, values: List[str], min_count: int = None, 
                                  max_count: int = None) -> Optional[str]:
        """
        Validate multi-valued slot constraints.
        
        Args:
            values: List of slot values
            min_count: Minimum number of values required
            max_count: Maximum number of values allowed
            
        Returns:
            Error message if validation fails, None otherwise
        """
        if min_count is not None and len(values) < min_count:
            return f"Please provide at least {min_count} values."
        
        if max_count is not None and len(values) > max_count:
            return f"Please provide no more than {max_count} values."
        
        return None

    def pre_process_request(self, lex: LexEvent) -> Optional[Dict]:
        """
        Pre-process the request before main processing.
        Override to implement pre-processing logic.
        Return a response to short-circuit normal processing.
        
        Args:
            lex: LexEvent object
            
        Returns:
            Lex response dictionary or None to continue normal processing
        """
        # Check for low confidence
        if self.is_low_confidence_request(lex):
            return self.handle_low_confidence(lex)
        
        # Check for negative sentiment
        if self.is_negative_sentiment(lex):
            response = self.handle_negative_sentiment(lex)
            if response:
                return response
        
        # Validate slots
        validation_errors = self.validate_slots(lex)
        if validation_errors:
            # Return error for first validation failure
            slot_name, error_message = next(iter(validation_errors.items()))
            return self.handle_slot_validation_error(lex, slot_name, error_message)
        
        return None

    def post_process_response(self, lex: LexEvent, response: Dict) -> Dict:
        """
        Post-process the response before returning.
        Override to implement post-processing logic.
        
        Args:
            lex: LexEvent object
            response: Generated response
            
        Returns:
            Modified response
        """
        return response

    def process_request_with_hooks(self, lex: LexEvent) -> Dict:
        """
        Process request with pre and post processing hooks.
        This method is called by the dispatcher.
        """
        # Pre-processing
        pre_response = self.pre_process_request(lex)
        if pre_response:
            return self.post_process_response(lex, pre_response)
        
        # Main processing
        response = self.process_request(lex)
        
        # Post-processing
        return self.post_process_response(lex, response)

    def create_context_attributes(self, **kwargs) -> Dict:
        """
        Create context attributes dictionary.
        
        Args:
            **kwargs: Key-value pairs for context attributes
            
        Returns:
            Context attributes dictionary
        """
        return kwargs

    def log_request_info(self, lex: LexEvent):
        """Log useful request information for debugging."""
        logger.info(f"Processing intent: {lex.get_intent_name()}")
        logger.info(f"Input mode: {lex.get_input_mode()}")
        logger.info(f"Input transcript: {lex.get_input_transcript()}")
        
        confidence = lex.get_nlu_confidence_score()
        if confidence:
            logger.info(f"NLU confidence: {confidence}")
        
        sentiment = lex.get_sentiment_analysis()
        if sentiment:
            logger.info(f"Sentiment: {sentiment.get('sentiment')}")


class BaseIntentHandler(IntentHandler):
    """
    Base intent handler with common functionality implemented.
    Extend this class for simpler intent handlers.
    """
    
    def __init__(self, intent_name: str, required_slots: List[str] = None):
        super().__init__(intent_name)
        self._required_slots = required_slots or []
    
    def get_required_slots(self) -> List[str]:
        return self._required_slots
    
    def process_request(self, lex: LexEvent) -> Dict:
        """
        Default implementation that delegates to Lex if all required slots are filled,
        otherwise continues slot elicitation.
        """
        from amazon_lex_helper import LexResponse
        
        # Check if all required slots are filled
        missing_slots = []
        for slot_name in self.get_required_slots():
            if not lex.slot_exists(slot_name):
                missing_slots.append(slot_name)
        
        if missing_slots:
            # Continue slot elicitation
            return LexResponse.delegate(lex)
        
        # All slots filled, fulfill the intent
        return self.fulfill_intent(lex)
    
    @abstractmethod
    def fulfill_intent(self, lex: LexEvent) -> Dict:
        """
        Fulfill the intent when all required slots are filled.
        Override this method to implement intent fulfillment logic.
        """
        pass