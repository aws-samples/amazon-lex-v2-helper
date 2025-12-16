# Changelog

All notable changes to the amazon-lex-helper library will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2025-01-29

### Major Release - Enhanced Lex V2 Features

This major release adds comprehensive support for advanced Amazon Lex V2 features while maintaining full backward compatibility.

### Added

#### Rich Message Support
- **MessageBuilder**: Fluent interface for creating multiple message types in a single response
- **SSMLBuilder**: Create complex SSML content with prosody, emphasis, pauses, and more
- **CardBuilder**: Build image response cards with titles, subtitles, images, and buttons
- **Enhanced LexResponse functions**: 
  - `elicit_slot_with_rich_messages()` - Elicit slots with multiple message types
  - `elicit_intent_with_rich_messages()` - Elicit intents with rich content
  - `confirm_intent_with_rich_messages()` - Confirm intents with enhanced messages
  - `close_with_rich_messages()` - Close conversations with rich responses
  - `delegate_with_rich_messages()` - Delegate with enhanced message support
- **Message creation functions**:
  - `create_plain_text_message()` - Create plain text messages
  - `create_ssml_message()` - Create SSML messages
  - `create_custom_payload_message()` - Create custom payload messages
  - `create_image_response_card()` - Create image response cards

#### Runtime Hints for Speech Recognition
- **RuntimeHintsBuilder**: Improve speech recognition accuracy with slot and phrase hints
- **Slot hints**: Provide expected values for specific slots
- **Phrase hints**: Boost recognition of common phrases
- **Integration**: Runtime hints support in all enhanced response functions

#### Multi-valued Slot Support
- **LexEvent enhancements**:
  - `get_slot_values_list()` - Get all values from List-shaped slots
  - `is_multi_valued_slot()` - Check if a slot is multi-valued
  - `get_slot_original_value()` - Get original user input
  - `get_slot_resolved_values()` - Get all resolved values
- **SlotHandler utility**:
  - `create_scalar_slot()` - Create scalar slot structures
  - `create_list_slot()` - Create multi-valued slot structures
  - `add_value_to_list_slot()` - Add values to existing list slots
  - `merge_slot_values()` - Merge slot values intelligently

#### Sentiment Analysis
- **LexEvent enhancements**:
  - `get_sentiment_analysis()` - Access user sentiment data
  - `get_transcription_confidence()` - Get speech recognition confidence
  - `get_nlu_confidence_score()` - Get NLU confidence scores
  - `is_low_confidence_intent()` - Detect low confidence requests
- **IntentHandler enhancements**:
  - `is_negative_sentiment()` - Detect negative user sentiment
  - `handle_negative_sentiment()` - Custom negative sentiment handling
  - `handle_low_confidence()` - Custom low confidence handling

#### Enhanced Slot Validation
- **SlotValidator utility** with built-in validators:
  - `validate_email()` - Email format validation
  - `validate_phone_number()` - Phone number validation
  - `validate_date_format()` - Date format validation
  - `validate_numeric_range()` - Numeric range validation
  - `validate_string_length()` - String length validation
  - `validate_choice()` - Choice validation with case sensitivity options
- **SlotHandler validation**:
  - `validate_slot_value()` - Validate against allowed values
  - `validate_slot_pattern()` - Regex pattern validation
  - Error tracking and retry logic

#### Context Management
- **ContextManager utility**:
  - `create_context()` - Create context structures
  - `get_context_by_name()` - Find contexts by name
  - `update_context_attributes()` - Update context attributes
  - `add_context()` - Add new contexts
  - `remove_context()` - Remove contexts
  - `extend_context_ttl()` - Extend context time-to-live
- **ConversationState utility**:
  - `get_state()` / `set_state()` - Manage conversation state
  - `update_state()` - Update specific state values
  - `clear_state()` - Clear conversation state
  - `is_state_active()` - Check if state is active

#### Enhanced Intent Handlers
- **BaseIntentHandler**: Simplified base class for common intent patterns
  - Automatic slot validation
  - Required slots management
  - Built-in fulfillment flow
- **Enhanced IntentHandler**:
  - `pre_process_request()` - Pre-processing hooks
  - `post_process_response()` - Post-processing hooks
  - `validate_slots()` - Custom slot validation
  - `handle_slot_validation_error()` - Validation error handling
  - `get_multi_valued_slot()` - Multi-valued slot access
  - `log_request_info()` - Enhanced logging

#### LexEvent Enhancements
- **Context access**:
  - `get_active_contexts()` - Get all active contexts
  - `get_context_attributes()` - Get specific context attributes
- **Bot information**:
  - `get_bot_info()` - Get bot name, version, locale
  - `get_session_id()` - Get session identifier
  - `get_user_id()` - Get user identifier
- **Alternative intents**:
  - `has_alternative_intents()` - Check for alternative interpretations
  - `get_alternative_intents()` - Get alternative intent options
- **Input mode detection**:
  - `is_voice_input()` - Check if input was voice
  - `is_text_input()` - Check if input was text
  - `is_dtmf_input()` - Check if input was DTMF

#### Quick Helper Functions
- `quick_text_message()` - Quick plain text message creation
- `quick_ssml_message()` - Quick SSML message creation
- `quick_card_message()` - Quick image response card creation
- `quick_mixed_message()` - Quick mixed message creation

#### Developer Experience
- **Comprehensive type hints** throughout the codebase
- **Enhanced error handling** and validation
- **Detailed documentation** and inline comments
- **Extensive examples** demonstrating all features
- **Unit tests** for new functionality

### Enhanced

#### LexEventDispatcher
- Updated to use enhanced IntentHandler processing hooks
- Backward compatibility with existing handlers
- Enhanced logging and error handling

#### LexResponse
- Added type hints for better IDE support
- Enhanced existing functions with optional rich message support
- Improved error handling and validation

### Documentation

#### New Files
- `examples/enhanced_features_examples.py` - Comprehensive usage examples
- `test/test_enhanced_lex_event.py` - Tests for enhanced LexEvent features
- `test/test_message_builder.py` - Tests for message builders
- `CHANGELOG.md` - This changelog

#### Updated Files
- `README.md` - Complete rewrite with enhanced examples and feature documentation
- Inline documentation throughout all modules

### Migration Guide

#### From v1.x to v2.0

The library maintains full backward compatibility. Existing code will continue to work without changes.

**Optional Enhancements:**

1. **Replace IntentHandler with BaseIntentHandler** for simpler intent handling:
   ```python
   # Old way (still works)
   class MyIntent(IntentHandler):
       def process_request(self, lex):
           # Manual slot checking and delegation
           return LexResponse.delegate(lex)
   
   # New way (recommended)
   class MyIntent(BaseIntentHandler):
       def __init__(self):
           super().__init__("MyIntent", required_slots=["Slot1", "Slot2"])
       
       def fulfill_intent(self, lex):
           # Called automatically when all slots are filled
           return LexResponse.close(...)
   ```

2. **Add rich messages** using MessageBuilder:
   ```python
   # Old way (still works)
   return LexResponse.close(session_attrs, intent, {}, "Simple message")
   
   # New way (enhanced)
   messages = MessageBuilder() \
       .add_plain_text("Thank you!") \
       .add_ssml(SSMLBuilder().speak("Have a great day!").build()) \
       .build()
   return LexResponse.close_with_rich_messages(session_attrs, intent, {}, messages)
   ```

3. **Use runtime hints** for better speech recognition:
   ```python
   hints = RuntimeHintsBuilder() \
       .add_slot_hint("City", ["London", "Paris", "New York"]) \
       .build()
   return LexResponse.elicit_slot_with_rich_messages(lex, "City", messages, hints)
   ```

4. **Access sentiment analysis**:
   ```python
   sentiment = lex.get_sentiment_analysis()
   if sentiment and sentiment['sentiment'] == 'NEGATIVE':
       # Handle negative sentiment
   ```

5. **Handle multi-valued slots**:
   ```python
   if lex.is_multi_valued_slot("Toppings"):
       toppings = lex.get_slot_values_list("Toppings")
       # Process list of toppings
   ```

### Fixed

- Fixed `valid_intent()` method in IntentHandler to properly access slot data
- Improved error handling in LexEventDispatcher
- Enhanced logging configuration and level management

### Security

- No security-related changes in this release
- All new features follow AWS security best practices

### Dependencies

- No new external dependencies added
- Maintains compatibility with existing Python environments
- Enhanced type hints require Python 3.6+ for full benefit

---

## [1.x] - Previous Versions

### Legacy Features (Maintained)
- Basic LexEvent functionality
- Standard LexResponse methods
- LexEventDispatcher with intent routing
- Basic IntentHandler abstract class
- Disambiguation support

All legacy features remain fully functional and supported in v2.0.0.

---

## Contributing

When contributing to this project, please:
1. Update this changelog with your changes
2. Follow semantic versioning principles
3. Maintain backward compatibility when possible
4. Add tests for new features
5. Update documentation and examples

## Support

For questions about this changelog or the library:
- Review the updated README.md for usage examples
- Check the examples/ directory for comprehensive code samples
- Refer to the AWS Lex V2 documentation for service-specific details
