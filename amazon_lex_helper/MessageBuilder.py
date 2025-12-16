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

"""
Rich message builder utilities for Amazon Lex V2.
Provides fluent interface for creating complex messages with multiple content types.
"""

from typing import Dict, List, Optional, Any


class MessageBuilder:
    """Fluent builder for creating rich Lex V2 messages."""
    
    def __init__(self):
        self.messages = []
    
    def add_plain_text(self, content: str) -> 'MessageBuilder':
        """Add a plain text message."""
        self.messages.append({
            "contentType": "PlainText",
            "content": content
        })
        return self
    
    def add_ssml(self, ssml_content: str) -> 'MessageBuilder':
        """Add an SSML message for enhanced speech output."""
        self.messages.append({
            "contentType": "SSML",
            "content": ssml_content
        })
        return self
    
    def add_custom_payload(self, payload: Dict) -> 'MessageBuilder':
        """Add a custom payload message for platform-specific responses."""
        self.messages.append({
            "contentType": "CustomPayload",
            "content": payload
        })
        return self
    
    def add_image_response_card(self, title: str, subtitle: str = None, 
                               image_url: str = None, buttons: List[Dict] = None) -> 'MessageBuilder':
        """
        Add an image response card message.
        
        Args:
            title: Card title
            subtitle: Optional card subtitle
            image_url: Optional image URL
            buttons: Optional list of buttons with 'text' and 'value' keys
        """
        card = {
            "contentType": "ImageResponseCard",
            "imageResponseCard": {
                "title": title
            }
        }
        
        if subtitle:
            card["imageResponseCard"]["subtitle"] = subtitle
        
        if image_url:
            card["imageResponseCard"]["imageUrl"] = image_url
        
        if buttons:
            card["imageResponseCard"]["buttons"] = buttons
        
        self.messages.append(card)
        return self
    
    def build(self) -> List[Dict]:
        """Build and return the list of messages."""
        return self.messages.copy()
    
    def clear(self) -> 'MessageBuilder':
        """Clear all messages and start fresh."""
        self.messages.clear()
        return self


class SSMLBuilder:
    """Builder for creating SSML content."""
    
    def __init__(self):
        self.content = []
    
    def speak(self, text: str) -> 'SSMLBuilder':
        """Add plain text to speak."""
        self.content.append(text)
        return self
    
    def pause(self, duration: str = "1s") -> 'SSMLBuilder':
        """Add a pause with specified duration."""
        self.content.append(f'<break time="{duration}"/>')
        return self
    
    def emphasis(self, text: str, level: str = "moderate") -> 'SSMLBuilder':
        """
        Add emphasized text.
        
        Args:
            text: Text to emphasize
            level: Emphasis level ("strong", "moderate", "reduced")
        """
        self.content.append(f'<emphasis level="{level}">{text}</emphasis>')
        return self
    
    def prosody(self, text: str, rate: str = None, pitch: str = None, 
                volume: str = None) -> 'SSMLBuilder':
        """
        Add text with prosody modifications.
        
        Args:
            text: Text to modify
            rate: Speech rate ("x-slow", "slow", "medium", "fast", "x-fast")
            pitch: Speech pitch ("x-low", "low", "medium", "high", "x-high")
            volume: Speech volume ("silent", "x-soft", "soft", "medium", "loud", "x-loud")
        """
        attributes = []
        if rate:
            attributes.append(f'rate="{rate}"')
        if pitch:
            attributes.append(f'pitch="{pitch}"')
        if volume:
            attributes.append(f'volume="{volume}"')
        
        attr_str = " ".join(attributes)
        self.content.append(f'<prosody {attr_str}>{text}</prosody>')
        return self
    
    def say_as(self, text: str, interpret_as: str, format_attr: str = None) -> 'SSMLBuilder':
        """
        Add text with specific interpretation.
        
        Args:
            text: Text to interpret
            interpret_as: How to interpret ("spell-out", "digits", "date", "time", etc.)
            format_attr: Format attribute for dates/times
        """
        if format_attr:
            self.content.append(f'<say-as interpret-as="{interpret_as}" format="{format_attr}">{text}</say-as>')
        else:
            self.content.append(f'<say-as interpret-as="{interpret_as}">{text}</say-as>')
        return self
    
    def phoneme(self, text: str, alphabet: str, ph: str) -> 'SSMLBuilder':
        """
        Add phonetic pronunciation.
        
        Args:
            text: Text to pronounce
            alphabet: Phonetic alphabet ("ipa" or "x-sampa")
            ph: Phonetic pronunciation
        """
        self.content.append(f'<phoneme alphabet="{alphabet}" ph="{ph}">{text}</phoneme>')
        return self
    
    def substitute(self, text: str, alias: str) -> 'SSMLBuilder':
        """
        Substitute text with alias for pronunciation.
        
        Args:
            text: Original text
            alias: Text to speak instead
        """
        self.content.append(f'<sub alias="{alias}">{text}</sub>')
        return self
    
    def build(self) -> str:
        """Build and return the SSML content wrapped in speak tags."""
        content_str = "".join(self.content)
        return f'<speak>{content_str}</speak>'
    
    def clear(self) -> 'SSMLBuilder':
        """Clear all content and start fresh."""
        self.content.clear()
        return self


class CardBuilder:
    """Builder for creating image response cards."""
    
    def __init__(self, title: str):
        self.card = {
            "contentType": "ImageResponseCard",
            "imageResponseCard": {
                "title": title,
                "buttons": []
            }
        }
    
    def subtitle(self, subtitle: str) -> 'CardBuilder':
        """Set card subtitle."""
        self.card["imageResponseCard"]["subtitle"] = subtitle
        return self
    
    def image_url(self, url: str) -> 'CardBuilder':
        """Set card image URL."""
        self.card["imageResponseCard"]["imageUrl"] = url
        return self
    
    def add_button(self, text: str, value: str) -> 'CardBuilder':
        """Add a button to the card."""
        self.card["imageResponseCard"]["buttons"].append({
            "text": text,
            "value": value
        })
        return self
    
    def add_url_button(self, text: str, url: str) -> 'CardBuilder':
        """Add a URL button to the card."""
        self.card["imageResponseCard"]["buttons"].append({
            "text": text,
            "value": url
        })
        return self
    
    def build(self) -> Dict:
        """Build and return the card."""
        # Remove empty buttons array if no buttons were added
        if not self.card["imageResponseCard"]["buttons"]:
            del self.card["imageResponseCard"]["buttons"]
        return self.card.copy()


class RuntimeHintsBuilder:
    """Builder for creating runtime hints to improve speech recognition."""
    
    def __init__(self):
        self.hints = {}
    
    def add_slot_hint(self, slot_name: str, values: List[str], 
                     subslot_hints: Dict = None) -> 'RuntimeHintsBuilder':
        """
        Add hints for a specific slot.
        
        Args:
            slot_name: Name of the slot
            values: List of expected values
            subslot_hints: Optional hints for subslots
        """
        if 'slotHints' not in self.hints:
            self.hints['slotHints'] = {}
        
        hint = {
            'runtimeHintValues': [{'phrase': value} for value in values]
        }
        
        if subslot_hints:
            hint['subSlotHints'] = subslot_hints
        
        self.hints['slotHints'][slot_name] = hint
        return self
    
    def add_phrase_hints(self, phrases: List[str]) -> 'RuntimeHintsBuilder':
        """
        Add general phrase hints to boost recognition.
        
        Args:
            phrases: List of phrases to boost
        """
        if 'phraseHints' not in self.hints:
            self.hints['phraseHints'] = []
        
        for phrase in phrases:
            self.hints['phraseHints'].append({'value': phrase})
        
        return self
    
    def build(self) -> Dict:
        """Build and return the runtime hints."""
        return self.hints.copy()
    
    def clear(self) -> 'RuntimeHintsBuilder':
        """Clear all hints and start fresh."""
        self.hints.clear()
        return self


# Convenience functions for quick message creation

def quick_text_message(content: str) -> List[Dict]:
    """Quick function to create a single plain text message."""
    return MessageBuilder().add_plain_text(content).build()


def quick_ssml_message(ssml_content: str) -> List[Dict]:
    """Quick function to create a single SSML message."""
    return MessageBuilder().add_ssml(ssml_content).build()


def quick_card_message(title: str, subtitle: str = None, image_url: str = None, 
                      buttons: List[Dict] = None) -> List[Dict]:
    """Quick function to create a single image response card message."""
    return MessageBuilder().add_image_response_card(title, subtitle, image_url, buttons).build()


def quick_mixed_message(text: str, ssml: str = None, card_title: str = None) -> List[Dict]:
    """Quick function to create a mixed message with text, optional SSML, and optional card."""
    builder = MessageBuilder().add_plain_text(text)
    
    if ssml:
        builder.add_ssml(ssml)
    
    if card_title:
        builder.add_image_response_card(card_title)
    
    return builder.build()
