"""
Test cases for MessageBuilder and related utilities.
"""

import unittest
from amazon_lex_helper import (
    MessageBuilder, SSMLBuilder, CardBuilder, RuntimeHintsBuilder,
    quick_text_message, quick_ssml_message, quick_card_message
)


class TestMessageBuilder(unittest.TestCase):
    
    def test_message_builder_plain_text(self):
        """Test MessageBuilder with plain text."""
        messages = MessageBuilder().add_plain_text("Hello World").build()
        
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0]['contentType'], 'PlainText')
        self.assertEqual(messages[0]['content'], 'Hello World')
    
    def test_message_builder_ssml(self):
        """Test MessageBuilder with SSML."""
        ssml_content = "<speak>Hello <emphasis>World</emphasis></speak>"
        messages = MessageBuilder().add_ssml(ssml_content).build()
        
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0]['contentType'], 'SSML')
        self.assertEqual(messages[0]['content'], ssml_content)
    
    def test_message_builder_custom_payload(self):
        """Test MessageBuilder with custom payload."""
        payload = {"platform": "test", "data": "value"}
        messages = MessageBuilder().add_custom_payload(payload).build()
        
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0]['contentType'], 'CustomPayload')
        self.assertEqual(messages[0]['content'], payload)
    
    def test_message_builder_image_response_card(self):
        """Test MessageBuilder with image response card."""
        messages = MessageBuilder().add_image_response_card(
            title="Test Card",
            subtitle="Test Subtitle",
            image_url="https://example.com/image.jpg",
            buttons=[{"text": "Button 1", "value": "value1"}]
        ).build()
        
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0]['contentType'], 'ImageResponseCard')
        
        card = messages[0]['imageResponseCard']
        self.assertEqual(card['title'], 'Test Card')
        self.assertEqual(card['subtitle'], 'Test Subtitle')
        self.assertEqual(card['imageUrl'], 'https://example.com/image.jpg')
        self.assertEqual(len(card['buttons']), 1)
        self.assertEqual(card['buttons'][0]['text'], 'Button 1')
    
    def test_message_builder_chaining(self):
        """Test MessageBuilder method chaining."""
        messages = MessageBuilder() \
            .add_plain_text("Hello") \
            .add_ssml("<speak>World</speak>") \
            .add_image_response_card("Card Title") \
            .build()
        
        self.assertEqual(len(messages), 3)
        self.assertEqual(messages[0]['contentType'], 'PlainText')
        self.assertEqual(messages[1]['contentType'], 'SSML')
        self.assertEqual(messages[2]['contentType'], 'ImageResponseCard')
    
    def test_message_builder_clear(self):
        """Test MessageBuilder clear functionality."""
        builder = MessageBuilder().add_plain_text("Hello")
        messages1 = builder.build()
        self.assertEqual(len(messages1), 1)
        
        builder.clear().add_plain_text("World")
        messages2 = builder.build()
        self.assertEqual(len(messages2), 1)
        self.assertEqual(messages2[0]['content'], 'World')


class TestSSMLBuilder(unittest.TestCase):
    
    def test_ssml_builder_basic(self):
        """Test basic SSML building."""
        ssml = SSMLBuilder().speak("Hello World").build()
        self.assertEqual(ssml, "<speak>Hello World</speak>")
    
    def test_ssml_builder_pause(self):
        """Test SSML pause."""
        ssml = SSMLBuilder().speak("Hello").pause("1s").speak("World").build()
        self.assertEqual(ssml, '<speak>Hello<break time="1s"/>World</speak>')
    
    def test_ssml_builder_emphasis(self):
        """Test SSML emphasis."""
        ssml = SSMLBuilder().emphasis("important", level="strong").build()
        self.assertEqual(ssml, '<speak><emphasis level="strong">important</emphasis></speak>')
    
    def test_ssml_builder_prosody(self):
        """Test SSML prosody."""
        ssml = SSMLBuilder().prosody("slow speech", rate="slow", volume="soft").build()
        expected = '<speak><prosody rate="slow" volume="soft">slow speech</prosody></speak>'
        self.assertEqual(ssml, expected)
    
    def test_ssml_builder_say_as(self):
        """Test SSML say-as."""
        ssml = SSMLBuilder().say_as("12345", "digits").build()
        self.assertEqual(ssml, '<speak><say-as interpret-as="digits">12345</say-as></speak>')
    
    def test_ssml_builder_complex(self):
        """Test complex SSML building."""
        ssml = SSMLBuilder() \
            .speak("Welcome") \
            .pause("500ms") \
            .emphasis("valued customer", level="moderate") \
            .speak("to our service") \
            .build()
        
        expected = '<speak>Welcome<break time="500ms"/><emphasis level="moderate">valued customer</emphasis>to our service</speak>'
        self.assertEqual(ssml, expected)


class TestCardBuilder(unittest.TestCase):
    
    def test_card_builder_basic(self):
        """Test basic card building."""
        card = CardBuilder("Test Title").build()
        
        self.assertEqual(card['contentType'], 'ImageResponseCard')
        self.assertEqual(card['imageResponseCard']['title'], 'Test Title')
        self.assertNotIn('buttons', card['imageResponseCard'])
    
    def test_card_builder_with_subtitle(self):
        """Test card with subtitle."""
        card = CardBuilder("Title").subtitle("Subtitle").build()
        
        self.assertEqual(card['imageResponseCard']['subtitle'], 'Subtitle')
    
    def test_card_builder_with_image(self):
        """Test card with image."""
        card = CardBuilder("Title").image_url("https://example.com/image.jpg").build()
        
        self.assertEqual(card['imageResponseCard']['imageUrl'], 'https://example.com/image.jpg')
    
    def test_card_builder_with_buttons(self):
        """Test card with buttons."""
        card = CardBuilder("Title") \
            .add_button("Button 1", "value1") \
            .add_button("Button 2", "value2") \
            .build()
        
        buttons = card['imageResponseCard']['buttons']
        self.assertEqual(len(buttons), 2)
        self.assertEqual(buttons[0]['text'], 'Button 1')
        self.assertEqual(buttons[0]['value'], 'value1')
        self.assertEqual(buttons[1]['text'], 'Button 2')
        self.assertEqual(buttons[1]['value'], 'value2')


class TestRuntimeHintsBuilder(unittest.TestCase):
    
    def test_runtime_hints_slot_hint(self):
        """Test runtime hints with slot hints."""
        hints = RuntimeHintsBuilder() \
            .add_slot_hint("City", ["London", "Paris", "New York"]) \
            .build()
        
        self.assertIn('slotHints', hints)
        self.assertIn('City', hints['slotHints'])
        
        city_hint = hints['slotHints']['City']
        self.assertIn('runtimeHintValues', city_hint)
        self.assertEqual(len(city_hint['runtimeHintValues']), 3)
        self.assertEqual(city_hint['runtimeHintValues'][0]['phrase'], 'London')
    
    def test_runtime_hints_phrase_hints(self):
        """Test runtime hints with phrase hints."""
        hints = RuntimeHintsBuilder() \
            .add_phrase_hints(["book a flight", "cancel reservation"]) \
            .build()
        
        self.assertIn('phraseHints', hints)
        self.assertEqual(len(hints['phraseHints']), 2)
        self.assertEqual(hints['phraseHints'][0]['value'], 'book a flight')
        self.assertEqual(hints['phraseHints'][1]['value'], 'cancel reservation')
    
    def test_runtime_hints_combined(self):
        """Test runtime hints with both slot and phrase hints."""
        hints = RuntimeHintsBuilder() \
            .add_slot_hint("Airport", ["JFK", "LAX"]) \
            .add_phrase_hints(["airport code"]) \
            .build()
        
        self.assertIn('slotHints', hints)
        self.assertIn('phraseHints', hints)
        self.assertEqual(len(hints['slotHints']['Airport']['runtimeHintValues']), 2)
        self.assertEqual(len(hints['phraseHints']), 1)


class TestQuickFunctions(unittest.TestCase):
    
    def test_quick_text_message(self):
        """Test quick text message function."""
        messages = quick_text_message("Hello World")
        
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0]['contentType'], 'PlainText')
        self.assertEqual(messages[0]['content'], 'Hello World')
    
    def test_quick_ssml_message(self):
        """Test quick SSML message function."""
        ssml_content = "<speak>Hello World</speak>"
        messages = quick_ssml_message(ssml_content)
        
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0]['contentType'], 'SSML')
        self.assertEqual(messages[0]['content'], ssml_content)
    
    def test_quick_card_message(self):
        """Test quick card message function."""
        messages = quick_card_message(
            "Card Title",
            subtitle="Card Subtitle",
            buttons=[{"text": "OK", "value": "ok"}]
        )
        
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0]['contentType'], 'ImageResponseCard')
        
        card = messages[0]['imageResponseCard']
        self.assertEqual(card['title'], 'Card Title')
        self.assertEqual(card['subtitle'], 'Card Subtitle')
        self.assertEqual(len(card['buttons']), 1)


if __name__ == '__main__':
    unittest.main()
