## amazon-lex-helper

This repository contains a list of helper classes to handle Amazon Lex V2 responses and create custom requests.
More specifically, it provides the following functionality:
* LexEvent: Amazon Lex event class
* LexResponse: builder to create Amazon Lex responses
* LexEventDispatcher: utility class to define your intent handlers
* IntentHandler: base class providing basic intent functionality

## Quick Install
```python
pip install amazon-lex-helper
```

## Example
*LexEventDispatcher* class provides an [observer](https://refactoring.guru/design-patterns/observer/python/example#:~:text=Observer%20is%20a%20behavioral%20design,that%20implements%20a%20subscriber%20interface.) approach to register intent handlers which scales better and is more modular than just a simple loop, as in the [examples](https://docs.aws.amazon.com/lex/latest/dg/ex-book-trip-create-lambda-function.html):   
For example, let's add extra validation to the [Book Hotel example](https://docs.aws.amazon.com/lex/latest/dg/ex-book-trip-create-bot.html) .
First step is to create our own BookHotel class to handle the intent. Notice the intent name (_BookHotel_) must match the intent name defined in Amazon Lex.   
```python
from amazon_lex_helper import LexEventDispatcher

from BookHotelIntent import BookHotelIntent

def lambda_handler(event, context):
    lexEventDispatcher = LexEventDispatcher()
    lexEventDispatcher.subscribe(
        BookHotelIntent("BookHotel")
    )
    return lexEventDispatcher.dispatch(event)
```

*BookHotelIntent* class adds some extra behaviour to the intent handling.    
In this case we will:
1. allow only reservations for London and Bristol cities
2. if the city is Bristol, we will set number of nights (_Nights_)to 5.
```python
from amazon_lex_helper import IntentHandler, LexEvent, LexResponse

class BookHotelIntent (IntentHandler):
    
    def process_request(self, req: LexEvent):

        if req.slot_exists("Location"):
            location = req.get_slot_interpreted_value("Location")
            if location not in ["London", "Bristol"]:
                return LexResponse.elicit_slot(req, "Location", message="Sorry, location can only be London or Bristol")
                
            if location == "Bristol":
                return LexResponse.delegate(req, "Nights", "5")
        
        return LexResponse.delegate(req)
```

## AWS Lambda usage

You can clone this repo and execute ./create_layer.sh script, which will create a .zip file inside /layer folder.  
That zip can be then used to create a layer for your [AWS Lambda function](https://docs.aws.amazon.com/lambda/latest/dg/adding-layers.html).


## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.

