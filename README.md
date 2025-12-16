# Amazon Lex V2 Helper Library

A comprehensive Python library for building Amazon Lex V2 Lambda functions with enhanced features including rich messages, runtime hints, multi-valued slots, sentiment analysis, and advanced slot validation.

## Features

### Core Functionality
* **LexEvent**: Enhanced Amazon Lex event class with 20+ new methods for advanced features
* **LexResponse**: Response builder with support for rich message types (SSML, Image Response Cards, Custom Payload)
* **LexEventDispatcher**: Event routing with enhanced processing hooks and ambiguity handling
* **IntentHandler**: Abstract base class with pre/post processing hooks and validation
* **BaseIntentHandler**: Simplified base class for common intent patterns with automatic slot management

### Enhanced Features (v2.0.0)
* **Rich Message Support**: SSML, Image Response Cards, Custom Payload messages with fluent builders
* **Runtime Hints**: Improve speech recognition accuracy with slot and phrase hints
* **Multi-valued Slots**: Complete support for List-shaped slots with validation utilities
* **Sentiment Analysis**: Access user sentiment data with confidence scores and custom handling
* **Enhanced Slot Validation**: Built-in validators for email, phone, date, numeric ranges, and more
* **Context Management**: Utilities for managing active contexts and conversation state
* **Message Builders**: Fluent interfaces for creating complex messages (MessageBuilder, SSMLBuilder, CardBuilder)
* **Slot Handlers**: Advanced slot manipulation, validation, and multi-value support
* **Type Safety**: Comprehensive type hints throughout the codebase

## Installation

```bash
pip install amazon-lex-helper
```

## Quick Start

### Basic Intent Handler

```python
from amazon_lex_helper import LexEventDispatcher, BaseIntentHandler

class BookHotelIntent(BaseIntentHandler):
    def __init__(self):
        super().__init__("BookHotel", required_slots=["Location", "CheckInDate"])
    
    def fulfill_intent(self, lex):
        location = lex.get_slot_interpreted_value("Location")
        check_in = lex.get_slot_interpreted_value("CheckInDate")
        
        return self.close_with_message(
            lex, f"Hotel booked in {location} for {check_in}!"
        )

def lambda_handler(event, context):
    dispatcher = LexEventDispatcher()
    dispatcher.subscribe(BookHotelIntent())
    return dispatcher.dispatch(event)
```

## Enhanced Examples

### Rich Messages with SSML and Cards

```python
from amazon_lex_helper import BaseIntentHandler, MessageBuilder, SSMLBuilder
from amazon_lex_helper import LexResponse

class BookHotelIntent(BaseIntentHandler):
    def __init__(self):
        super().__init__("BookHotel", required_slots=["Location", "CheckInDate"])
    
    def fulfill_intent(self, lex):
        location = lex.get_slot_interpreted_value("Location")
        
        # Create rich response with SSML and card
        messages = MessageBuilder() \
            .add_plain_text(f"Great! I found hotels in {location}.") \
            .add_ssml(
                SSMLBuilder()
                .speak("Perfect choice!")
                .pause("500ms")
                .emphasis(location, level="strong")
                .speak("has amazing hotels.")
                .build()
            ) \
            .add_image_response_card(
                title=f"Hotels in {location}",
                subtitle="Best available rates",
                image_url="https://example.com/hotel.jpg",
                buttons=[
                    {"text": "Book Now", "value": "book"},
                    {"text": "See More", "value": "more"}
                ]
            ).build()
        
        return LexResponse.close_with_rich_messages(
            lex.get_session_attrs(),
            lex.get_intent(),
            {},
            messages
        )
```

### Runtime Hints for Better Speech Recognition

```python
from amazon_lex_helper import RuntimeHintsBuilder, LexResponse

class FlightBookingIntent(BaseIntentHandler):
    def process_request(self, lex):
        if lex.is_requesting_slot("Origin"):
            # Add runtime hints for airport codes
            hints = RuntimeHintsBuilder() \
                .add_slot_hint("Origin", ["JFK", "LAX", "ORD", "SFO"]) \
                .add_phrase_hints(["John F Kennedy", "Los Angeles International"]) \
                .build()
            
            messages = [{"contentType": "PlainText", "content": "Which airport?"}]
            
            return LexResponse.elicit_slot_with_rich_messages(
                lex, "Origin", messages, runtime_hints=hints
            )
        
        return super().process_request(lex)
```

### Multi-valued Slots

```python
from amazon_lex_helper import SlotHandler, SlotValidator

class OrderPizzaIntent(BaseIntentHandler):
    def validate_slots(self, lex):
        errors = {}
        
        # Handle multi-valued toppings slot
        if lex.is_multi_valued_slot("Toppings"):
            toppings = lex.get_slot_values_list("Toppings")
            
            # Validate count
            if len(toppings) > 5:
                errors["Toppings"] = "Please choose no more than 5 toppings."
            
            # Validate each topping
            valid_toppings = ["pepperoni", "mushrooms", "cheese"]
            for topping in toppings:
                if not SlotValidator.validate_choice(topping, valid_toppings):
                    errors["Toppings"] = f"{topping} is not available."
                    break
        
        return errors
```

### Sentiment Analysis and Enhanced Validation

```python
class CustomerServiceIntent(BaseIntentHandler):
    def handle_negative_sentiment(self, lex):
        """Handle frustrated customers with empathy."""
        messages = MessageBuilder() \
            .add_plain_text("I understand your frustration. Let me help you right away.") \
            .add_ssml(
                SSMLBuilder()
                .prosody("I'm here to help", rate="slow", volume="soft")
                .build()
            ).build()
        
        return LexResponse.elicit_intent_with_rich_messages(
            lex, "CustomerService", "InProgress", messages
        )
    
    def validate_slots(self, lex):
        errors = {}
        
        # Validate email with built-in validator
        email = lex.get_slot_interpreted_value("Email")
        if email and not SlotValidator.validate_email(email):
            errors["Email"] = "Please provide a valid email address."
        
        return errors
```

### Context Management

```python
from amazon_lex_helper import ContextManager, ConversationState

class ShoppingIntent(BaseIntentHandler):
    def __init__(self):
        super().__init__("Shopping")
        self.conversation_state = ConversationState("shoppingCart")
    
    def process_request(self, lex):
        contexts = lex.get_active_contexts()
        
        # Get current cart items
        cart_items = self.conversation_state.get_state_value(contexts, "items")
        
        if cart_items:
            message = f"You have {cart_items} in your cart. What else would you like?"
        else:
            message = "Welcome! What would you like to shop for today?"
        
        # Update conversation state
        contexts = self.conversation_state.update_state(contexts, {
            "last_interaction": "shopping_start"
        })
        
        response = LexResponse.elicit_intent_with_rich_messages(
            lex, "Shopping", "InProgress", [{"contentType": "PlainText", "content": message}]
        )
        response['sessionState']['activeContexts'] = contexts
        
        return response
```

## Available Utilities

### Message Builders
- **MessageBuilder**: Fluent interface for creating multiple message types
- **SSMLBuilder**: Create SSML content with prosody, emphasis, pauses
- **CardBuilder**: Create image response cards with buttons
- **RuntimeHintsBuilder**: Create runtime hints for speech recognition

### Slot Utilities
- **SlotHandler**: Create and manipulate scalar and list slots
- **SlotValidator**: Built-in validators (email, phone, date, numeric range, etc.)

### Context Utilities
- **ContextManager**: Manage active contexts and attributes
- **ConversationState**: Maintain conversation state across turns

### Enhanced LexEvent Methods

#### Sentiment and Confidence
```python
sentiment = lex.get_sentiment_analysis()
confidence = lex.get_nlu_confidence_score()
is_low_confidence = lex.is_low_confidence_intent(threshold=0.5)
```

#### Multi-valued Slots
```python
if lex.is_multi_valued_slot("Toppings"):
    toppings = lex.get_slot_values_list("Toppings")
    original_values = [lex.get_slot_original_value(slot) for slot in toppings]
```

#### Context Access
```python
contexts = lex.get_active_contexts()
bot_info = lex.get_bot_info()
session_id = lex.get_session_id()
```

#### Input Mode Detection
```python
if lex.is_voice_input():
    # Handle voice-specific logic
elif lex.is_text_input():
    # Handle text-specific logic
```

### Quick Functions
```python
from amazon_lex_helper import quick_text_message, quick_ssml_message, quick_card_message

# Quick message creation
text_msg = quick_text_message("Hello!")
ssml_msg = quick_ssml_message("<speak>Hello <emphasis>world</emphasis>!</speak>")
card_msg = quick_card_message("Title", "Subtitle", buttons=[{"text": "OK", "value": "ok"}])
```

## Advanced Features

### Custom Slot Validation

```python
class BookingIntent(BaseIntentHandler):
    def validate_slots(self, lex):
        errors = {}
        
        # Email validation
        email = lex.get_slot_interpreted_value("Email")
        if email and not SlotValidator.validate_email(email):
            errors["Email"] = "Please provide a valid email address."
        
        # Phone validation
        phone = lex.get_slot_interpreted_value("Phone")
        if phone and not SlotValidator.validate_phone_number(phone):
            errors["Phone"] = "Please provide a valid phone number."
        
        # Custom validation
        booking_date = lex.get_slot_interpreted_value("BookingDate")
        if booking_date:
            from datetime import datetime, timedelta
            try:
                date_obj = datetime.strptime(booking_date, "%Y-%m-%d")
                if date_obj < datetime.now() + timedelta(days=1):
                    errors["BookingDate"] = "Booking must be at least 1 day in advance."
            except ValueError:
                errors["BookingDate"] = "Please provide a valid date in YYYY-MM-DD format."
        
        return errors
```

### Processing Hooks

```python
class EnhancedIntent(BaseIntentHandler):
    def pre_process_request(self, lex):
        # Log request details
        self.log_request_info(lex)
        
        # Check for negative sentiment
        if self.is_negative_sentiment(lex):
            return self.handle_negative_sentiment(lex)
        
        # Continue with normal processing
        return None
    
    def post_process_response(self, lex, response):
        # Add custom headers or modify response
        response['customData'] = {
            'processed_at': datetime.now().isoformat(),
            'confidence': lex.get_nlu_confidence_score()
        }
        return response
```

## Migration from v1.x

The library maintains full backward compatibility. Existing code will continue to work without changes.

### Optional Enhancements:

1. **Replace IntentHandler with BaseIntentHandler** for simpler intent handling
2. **Add rich messages** using MessageBuilder and enhanced response functions
3. **Use runtime hints** for better speech recognition
4. **Access sentiment analysis** with `lex.get_sentiment_analysis()`
5. **Handle multi-valued slots** with `lex.get_slot_values_list()`

### Migration Example:

```python
# Old way (still works)
class MyIntent(IntentHandler):
    def process_request(self, lex):
        if not self.valid_intent(lex):
            return LexResponse.delegate(lex)
        return LexResponse.close(session_attrs, intent, {}, "Done!")

# New way (recommended)
class MyIntent(BaseIntentHandler):
    def __init__(self):
        super().__init__("MyIntent", required_slots=["Slot1", "Slot2"])
    
    def fulfill_intent(self, lex):
        messages = MessageBuilder().add_plain_text("Done!").build()
        return LexResponse.close_with_rich_messages(
            lex.get_session_attrs(), lex.get_intent(), {}, messages
        )
```

## Testing

Run the test suite:

```bash
# Install test dependencies
pip install pytest

# Run all tests
python -m pytest test/ -v

# Run specific test files
python -m pytest test/test_enhanced_lex_event.py -v
python -m pytest test/test_message_builder.py -v
```

## AWS Lambda Usage

### Creating a Lambda Layer

You can create a Lambda layer for easy deployment:

```bash
# Clone the repository
git clone https://github.com/aws-samples/amazon-lex-v2-helper.git
cd amazon-lex-v2-helper

# Create the layer
./create_layer.sh
```

This creates a .zip file in the `/layer` folder that can be used as an [AWS Lambda layer](https://docs.aws.amazon.com/lambda/latest/dg/adding-layers.html).

### Lambda Function Example

```python
import json
from amazon_lex_helper import LexEventDispatcher, BaseIntentHandler, MessageBuilder

class WelcomeIntent(BaseIntentHandler):
    def __init__(self):
        super().__init__("Welcome")
    
    def fulfill_intent(self, lex):
        messages = MessageBuilder() \
            .add_plain_text("Welcome to our service!") \
            .add_image_response_card(
                title="Welcome",
                subtitle="How can I help you today?",
                buttons=[
                    {"text": "Book Hotel", "value": "book_hotel"},
                    {"text": "Check Booking", "value": "check_booking"}
                ]
            ).build()
        
        return self.close_with_rich_messages(lex, messages)

def lambda_handler(event, context):
    dispatcher = LexEventDispatcher()
    dispatcher.subscribe(WelcomeIntent())
    
    try:
        response = dispatcher.dispatch(event)
        return response
    except Exception as e:
        print(f"Error processing request: {str(e)}")
        return {
            "sessionState": {
                "dialogAction": {"type": "Close"},
                "intent": {"name": "FallbackIntent", "state": "Failed"}
            },
            "messages": [{
                "contentType": "PlainText",
                "content": "I'm sorry, I encountered an error. Please try again."
            }]
        }
```

## Requirements

- Python 3.6+
- No external dependencies (uses only Python standard library)
- Compatible with AWS Lambda Python runtime

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Security

See [CONTRIBUTING.md](CONTRIBUTING.md#security-issue-notifications) for security issue reporting.

## License

This library is licensed under the MIT-0 License. See the [LICENSE](LICENSE) file for details.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for detailed information about changes in each version.

## Support

- **Documentation**: Check the examples in the `/examples` directory
- **Issues**: Report bugs or request features via GitHub Issues
- **AWS Lex V2 Documentation**: [Official AWS Documentation](https://docs.aws.amazon.com/lexv2/)

## Version

Current version: **2.0.0** - Major enhancement release with comprehensive Lex V2 feature support.

