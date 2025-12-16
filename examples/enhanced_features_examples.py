"""
Enhanced Amazon Lex V2 Helper Examples

This file demonstrates the new features added to the amazon-lex-helper library:
- Rich message types (SSML, Image Response Cards, Custom Payload)
- Runtime hints for improved speech recognition
- Multi-valued slot handling
- Sentiment analysis
- Enhanced slot validation
- Context management
"""

from amazon_lex_helper import (
    LexEvent, LexEventDispatcher, BaseIntentHandler,
    MessageBuilder, SSMLBuilder, CardBuilder, RuntimeHintsBuilder,
    SlotHandler, SlotValidator, ContextManager, ConversationState,
    quick_text_message, quick_ssml_message, quick_card_message
)
from amazon_lex_helper import LexResponse


# Example 1: Enhanced Intent Handler with Rich Messages
class BookHotelIntentEnhanced(BaseIntentHandler):
    """Enhanced BookHotel intent with rich messages and validation."""
    
    def __init__(self):
        super().__init__("BookHotel", required_slots=["Location", "CheckInDate", "Nights"])
    
    def validate_slots(self, lex: LexEvent):
        """Custom slot validation."""
        errors = {}
        
        # Validate location
        location = lex.get_slot_interpreted_value("Location")
        if location and not SlotValidator.validate_choice(
            location, ["London", "Bristol", "Manchester"], case_sensitive=False
        ):
            errors["Location"] = "Sorry, we only have hotels in London, Bristol, and Manchester."
        
        # Validate nights
        nights = lex.get_slot_interpreted_value("Nights")
        if nights and not SlotValidator.validate_numeric_range(nights, min_val=1, max_val=30):
            errors["Nights"] = "Please choose between 1 and 30 nights."
        
        return errors
    
    def handle_negative_sentiment(self, lex: LexEvent):
        """Handle negative sentiment with empathetic response."""
        messages = MessageBuilder() \
            .add_plain_text("I understand you might be frustrated. Let me help you find the perfect hotel.") \
            .add_ssml(
                SSMLBuilder()
                .prosody("I'm here to help", rate="slow", volume="soft")
                .build()
            ).build()
        
        return LexResponse.elicit_slot_with_rich_messages(
            lex, "Location", messages
        )
    
    def fulfill_intent(self, lex: LexEvent):
        """Fulfill the hotel booking with rich response."""
        location = lex.get_slot_interpreted_value("Location")
        nights = lex.get_slot_interpreted_value("Nights")
        check_in = lex.get_slot_interpreted_value("CheckInDate")
        
        # Create rich response with card
        messages = MessageBuilder() \
            .add_plain_text(f"Great! I've found hotels in {location} for {nights} nights starting {check_in}.") \
            .add_image_response_card(
                title=f"Hotels in {location}",
                subtitle=f"{nights} nights from {check_in}",
                image_url="https://example.com/hotel-image.jpg",
                buttons=[
                    {"text": "Book Now", "value": "book_hotel"},
                    {"text": "See More Options", "value": "more_options"}
                ]
            ).build()
        
        return LexResponse.close_with_rich_messages(
            lex.get_session_attrs(),
            lex.get_intent(),
            {},
            messages
        )


# Example 2: Multi-valued Slot Handler
class OrderPizzaIntent(BaseIntentHandler):
    """Pizza ordering intent with multi-valued toppings slot."""
    
    def __init__(self):
        super().__init__("OrderPizza", required_slots=["Size", "Toppings"])
    
    def validate_slots(self, lex: LexEvent):
        """Validate pizza order slots."""
        errors = {}
        
        # Validate toppings (multi-valued slot)
        if lex.is_multi_valued_slot("Toppings"):
            toppings = lex.get_slot_values_list("Toppings")
            if len(toppings) > 5:
                errors["Toppings"] = "Please choose no more than 5 toppings."
            
            # Validate each topping
            valid_toppings = ["pepperoni", "mushrooms", "cheese", "sausage", "peppers", "onions"]
            for topping in toppings:
                if not SlotValidator.validate_choice(topping, valid_toppings, case_sensitive=False):
                    errors["Toppings"] = f"Sorry, {topping} is not available. Choose from: {', '.join(valid_toppings)}"
                    break
        
        return errors
    
    def fulfill_intent(self, lex: LexEvent):
        """Fulfill pizza order."""
        size = lex.get_slot_interpreted_value("Size")
        toppings = lex.get_slot_values_list("Toppings") or [lex.get_slot_interpreted_value("Toppings")]
        
        toppings_text = ", ".join(toppings)
        
        # Create SSML response
        ssml_content = SSMLBuilder() \
            .speak("Perfect! I've ordered a") \
            .emphasis(size, level="strong") \
            .speak("pizza with") \
            .emphasis(toppings_text, level="moderate") \
            .pause("500ms") \
            .speak("Your order will be ready in 20 minutes.") \
            .build()
        
        messages = MessageBuilder() \
            .add_plain_text(f"Perfect! I've ordered a {size} pizza with {toppings_text}. Your order will be ready in 20 minutes.") \
            .add_ssml(ssml_content) \
            .build()
        
        return LexResponse.close_with_rich_messages(
            lex.get_session_attrs(),
            lex.get_intent(),
            {},
            messages
        )


# Example 3: Intent with Runtime Hints
class FlightBookingIntent(BaseIntentHandler):
    """Flight booking with runtime hints for better speech recognition."""
    
    def __init__(self):
        super().__init__("BookFlight", required_slots=["Origin", "Destination", "DepartureDate"])
    
    def process_request(self, lex: LexEvent):
        """Process with runtime hints for airport codes."""
        
        # If we're eliciting Origin or Destination, add runtime hints
        if lex.is_requesting_slot("Origin") or lex.is_requesting_slot("Destination"):
            # Create runtime hints for common airports
            hints = RuntimeHintsBuilder() \
                .add_slot_hint("Origin", [
                    "JFK", "LAX", "ORD", "DFW", "ATL", "SFO", "SEA", "MIA"
                ]) \
                .add_slot_hint("Destination", [
                    "JFK", "LAX", "ORD", "DFW", "ATL", "SFO", "SEA", "MIA"
                ]) \
                .add_phrase_hints([
                    "John F Kennedy Airport",
                    "Los Angeles International",
                    "O'Hare International",
                    "Dallas Fort Worth"
                ]) \
                .build()
            
            messages = quick_text_message("Which airport would you like to fly from?")
            
            return LexResponse.elicit_slot_with_rich_messages(
                lex, "Origin", messages, runtime_hints=hints
            )
        
        return super().process_request(lex)
    
    def fulfill_intent(self, lex: LexEvent):
        """Fulfill flight booking."""
        origin = lex.get_slot_interpreted_value("Origin")
        destination = lex.get_slot_interpreted_value("Destination")
        departure_date = lex.get_slot_interpreted_value("DepartureDate")
        
        messages = quick_card_message(
            title="Flight Search Results",
            subtitle=f"{origin} to {destination} on {departure_date}",
            image_url="https://example.com/flight-image.jpg",
            buttons=[
                {"text": "Book Flight", "value": "book_flight"},
                {"text": "Change Dates", "value": "change_dates"}
            ]
        )
        
        return LexResponse.close_with_rich_messages(
            lex.get_session_attrs(),
            lex.get_intent(),
            {},
            messages
        )


# Example 4: Context-Aware Intent Handler
class CustomerServiceIntent(BaseIntentHandler):
    """Customer service intent using conversation state."""
    
    def __init__(self):
        super().__init__("CustomerService")
        self.conversation_state = ConversationState("customerServiceState")
    
    def process_request(self, lex: LexEvent):
        """Process customer service request with context awareness."""
        contexts = lex.get_active_contexts()
        
        # Check if this is a returning customer
        customer_id = self.conversation_state.get_state_value(contexts, "customer_id")
        issue_type = self.conversation_state.get_state_value(contexts, "issue_type")
        
        if customer_id and issue_type:
            # Returning customer with known issue
            messages = MessageBuilder() \
                .add_plain_text(f"Welcome back! I see you're still working on your {issue_type} issue.") \
                .add_plain_text("How can I help you today?") \
                .build()
        else:
            # New customer
            messages = MessageBuilder() \
                .add_plain_text("Welcome to customer service! I'm here to help.") \
                .add_plain_text("What can I assist you with today?") \
                .build()
            
            # Set up conversation state
            contexts = self.conversation_state.set_state(contexts, {
                "session_start": "true",
                "interaction_count": "1"
            })
        
        # Update contexts in response
        response = LexResponse.elicit_intent_with_rich_messages(
            lex, "CustomerService", "InProgress", messages
        )
        response['sessionState']['activeContexts'] = contexts
        
        return response
    
    def fulfill_intent(self, lex: LexEvent):
        """This intent doesn't fulfill, it routes to other intents."""
        return LexResponse.delegate(lex)


# Example 5: Lambda Handler with Enhanced Dispatcher
def lambda_handler(event, context):
    """Enhanced lambda handler demonstrating new features."""
    
    # Create dispatcher
    dispatcher = LexEventDispatcher()
    
    # Subscribe enhanced intent handlers
    dispatcher.subscribe(
        BookHotelIntentEnhanced(),
        OrderPizzaIntent(),
        FlightBookingIntent(),
        CustomerServiceIntent()
    )
    
    # Process the request
    return dispatcher.dispatch(event)


# Example 6: Utility Functions Usage
def demonstrate_utilities():
    """Demonstrate utility functions."""
    
    # Message Builder
    messages = MessageBuilder() \
        .add_plain_text("Welcome to our service!") \
        .add_ssml(
            SSMLBuilder()
            .speak("Thank you for calling")
            .pause("500ms")
            .emphasis("premium support", level="strong")
            .build()
        ) \
        .add_image_response_card(
            title="Service Options",
            buttons=[
                {"text": "Technical Support", "value": "tech_support"},
                {"text": "Billing", "value": "billing"}
            ]
        ) \
        .build()
    
    # Slot Handler
    scalar_slot = SlotHandler.create_scalar_slot("London", "London", ["London", "Greater London"])
    list_slot = SlotHandler.create_list_slot([
        {"originalValue": "pepperoni", "interpretedValue": "pepperoni"},
        {"originalValue": "cheese", "interpretedValue": "cheese"}
    ])
    
    # Context Manager
    contexts = []
    contexts = ContextManager.add_context(
        contexts, "userPreferences", 
        {"preferred_location": "London", "loyalty_tier": "Gold"}
    )
    
    # Runtime Hints
    hints = RuntimeHintsBuilder() \
        .add_slot_hint("City", ["London", "Paris", "New York"]) \
        .add_phrase_hints(["book a flight", "cancel reservation"]) \
        .build()
    
    return {
        "messages": messages,
        "scalar_slot": scalar_slot,
        "list_slot": list_slot,
        "contexts": contexts,
        "hints": hints
    }


if __name__ == "__main__":
    # Demonstrate utilities
    demo_results = demonstrate_utilities()
    print("Enhanced features demonstration completed!")
    print(f"Created {len(demo_results['messages'])} messages")
    print(f"Created contexts: {[ctx['name'] for ctx in demo_results['contexts']]}")
