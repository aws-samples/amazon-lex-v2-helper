"""
Test cases for enhanced LexEvent features.
"""

import unittest
from amazon_lex_helper import LexEvent


class TestEnhancedLexEvent(unittest.TestCase):
    
    def setUp(self):
        """Set up test data."""
        self.sample_event = {
            "messageVersion": "1.0",
            "invocationSource": "DialogCodeHook",
            "userId": "test-user-123",
            "sessionId": "test-session-456",
            "inputMode": "Speech",
            "inputTranscript": "I want to book a hotel in London",
            "bot": {
                "name": "TestBot",
                "version": "1.0",
                "localeId": "en_US",
                "aliasId": "TestAlias"
            },
            "interpretations": [
                {
                    "intent": {
                        "name": "BookHotel",
                        "confirmationState": "None",
                        "state": "InProgress",
                        "slots": {
                            "Location": {
                                "shape": "Scalar",
                                "value": {
                                    "originalValue": "London",
                                    "interpretedValue": "London",
                                    "resolvedValues": ["London", "Greater London"]
                                }
                            },
                            "Toppings": {
                                "shape": "List",
                                "values": [
                                    {
                                        "value": {
                                            "originalValue": "pepperoni",
                                            "interpretedValue": "pepperoni",
                                            "resolvedValues": ["pepperoni"]
                                        }
                                    },
                                    {
                                        "value": {
                                            "originalValue": "cheese",
                                            "interpretedValue": "cheese",
                                            "resolvedValues": ["cheese"]
                                        }
                                    }
                                ]
                            }
                        }
                    },
                    "nluConfidence": {
                        "score": 0.85
                    },
                    "sentimentResponse": {
                        "sentiment": "POSITIVE",
                        "sentimentScore": {
                            "positive": 0.8,
                            "negative": 0.1,
                            "neutral": 0.1
                        }
                    }
                }
            ],
            "sessionState": {
                "activeContexts": [
                    {
                        "name": "testContext",
                        "contextAttributes": {
                            "key1": "value1"
                        },
                        "timeToLive": {
                            "timeToLiveInSeconds": 600,
                            "turnsToLive": 1
                        }
                    }
                ],
                "sessionAttributes": {
                    "sessionKey": "sessionValue"
                },
                "intent": {
                    "name": "BookHotel",
                    "confirmationState": "None",
                    "state": "InProgress",
                    "slots": {
                        "Location": {
                            "shape": "Scalar",
                            "value": {
                                "originalValue": "London",
                                "interpretedValue": "London",
                                "resolvedValues": ["London", "Greater London"]
                            }
                        },
                        "Toppings": {
                            "shape": "List",
                            "value": {
                                "originalValue": "pepperoni and cheese",
                                "interpretedValue": "pepperoni and cheese",
                                "resolvedValues": ["pepperoni and cheese"]
                            },
                            "values": [
                                {
                                    "value": {
                                        "originalValue": "pepperoni",
                                        "interpretedValue": "pepperoni",
                                        "resolvedValues": ["pepperoni"]
                                    }
                                },
                                {
                                    "value": {
                                        "originalValue": "cheese",
                                        "interpretedValue": "cheese",
                                        "resolvedValues": ["cheese"]
                                    }
                                }
                            ]
                        }
                    }
                }
            },
            "proposedNextState": {
                "dialogAction": {
                    "type": "ElicitSlot",
                    "slotToElicit": "CheckInDate"
                }
            }
        }
        
        self.lex_event = LexEvent(self.sample_event)
    
    def test_get_sentiment_analysis(self):
        """Test sentiment analysis retrieval."""
        sentiment = self.lex_event.get_sentiment_analysis()
        self.assertIsNotNone(sentiment)
        self.assertEqual(sentiment['sentiment'], 'POSITIVE')
        self.assertEqual(sentiment['sentimentScore']['positive'], 0.8)
    
    def test_get_transcription_confidence(self):
        """Test transcription confidence retrieval."""
        confidence = self.lex_event.get_transcription_confidence()
        self.assertEqual(confidence, 0.85)
    
    def test_get_slot_values_list(self):
        """Test multi-valued slot retrieval."""
        # Test list slot
        toppings = self.lex_event.get_slot_values_list("Toppings")
        self.assertEqual(toppings, ["pepperoni", "cheese"])
        
        # Test scalar slot (should return None)
        location_list = self.lex_event.get_slot_values_list("Location")
        self.assertIsNone(location_list)
        
        # Test non-existent slot
        non_existent = self.lex_event.get_slot_values_list("NonExistent")
        self.assertIsNone(non_existent)
    
    def test_get_slot_original_value(self):
        """Test original value retrieval."""
        original = self.lex_event.get_slot_original_value("Location")
        self.assertEqual(original, "London")
    
    def test_get_slot_resolved_values(self):
        """Test resolved values retrieval."""
        resolved = self.lex_event.get_slot_resolved_values("Location")
        self.assertEqual(resolved, ["London", "Greater London"])
    
    def test_is_multi_valued_slot(self):
        """Test multi-valued slot detection."""
        self.assertTrue(self.lex_event.is_multi_valued_slot("Toppings"))
        self.assertFalse(self.lex_event.is_multi_valued_slot("Location"))
        self.assertFalse(self.lex_event.is_multi_valued_slot("NonExistent"))
    
    def test_get_active_contexts(self):
        """Test active contexts retrieval."""
        contexts = self.lex_event.get_active_contexts()
        self.assertEqual(len(contexts), 1)
        self.assertEqual(contexts[0]['name'], 'testContext')
    
    def test_get_context_attributes(self):
        """Test context attributes retrieval."""
        attrs = self.lex_event.get_context_attributes("testContext")
        self.assertEqual(attrs, {"key1": "value1"})
        
        # Test non-existent context
        non_existent = self.lex_event.get_context_attributes("nonExistent")
        self.assertIsNone(non_existent)
    
    def test_get_bot_info(self):
        """Test bot information retrieval."""
        bot_info = self.lex_event.get_bot_info()
        self.assertEqual(bot_info['name'], 'TestBot')
        self.assertEqual(bot_info['version'], '1.0')
        self.assertEqual(bot_info['locale_id'], 'en_US')
    
    def test_get_session_id(self):
        """Test session ID retrieval."""
        session_id = self.lex_event.get_session_id()
        self.assertEqual(session_id, "test-session-456")
    
    def test_get_user_id(self):
        """Test user ID retrieval."""
        user_id = self.lex_event.get_user_id()
        self.assertEqual(user_id, "test-user-123")
    
    def test_has_alternative_intents(self):
        """Test alternative intents detection."""
        # Current test data has only one interpretation
        self.assertFalse(self.lex_event.has_alternative_intents())
    
    def test_get_nlu_confidence_score(self):
        """Test NLU confidence score retrieval."""
        confidence = self.lex_event.get_nlu_confidence_score()
        self.assertEqual(confidence, 0.85)
    
    def test_is_low_confidence_intent(self):
        """Test low confidence detection."""
        # With confidence 0.85, should not be low confidence with default threshold (0.4)
        self.assertFalse(self.lex_event.is_low_confidence_intent())
        # With confidence 0.85 and threshold 0.9, should be low confidence
        self.assertTrue(self.lex_event.is_low_confidence_intent(0.9))   # Higher threshold
        # With confidence 0.85 and threshold 0.8, should not be low confidence  
        self.assertFalse(self.lex_event.is_low_confidence_intent(0.8))   # Lower threshold
    
    def test_input_mode_checks(self):
        """Test input mode detection methods."""
        self.assertTrue(self.lex_event.is_voice_input())
        self.assertFalse(self.lex_event.is_text_input())
        self.assertFalse(self.lex_event.is_dtmf_input())


if __name__ == '__main__':
    unittest.main()
