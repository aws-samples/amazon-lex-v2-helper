## amazon-lex-helper

This repository contains a list of helper classes to handle Amazon Lex responses and create custom requests.
More specifically, it provides the following functionality:
* LexEvent: parses Amazon Lex events
* LexResponse: builder to create Amazon Lex responses
* LexEventDispatcher: utility class to define your intent handlers
* IntentHandler: class providing basic intent functionality

## Quick Install
```python
pip3 install amazon-lex-helper
```

## Example
*LexEventDispatcher* class provides an [observer](https://refactoring.guru/design-patterns/observer/python/example#:~:text=Observer%20is%20a%20behavioral%20design,that%20implements%20a%20subscriber%20interface.) approach to register intent handlers which scales better and is more modular than just a simple loop, as in the [examples](https://docs.aws.amazon.com/lex/latest/dg/ex-book-trip-create-lambda-function.html):
```python
from amazon_lex_helper import LexEventDispatcher

def lambda_handler(event, context):
    lexEventDispatcher = LexEventDispatcher()
    lexEventDispatcher.subscribe(
        MyFirstIntent("FirstIntentName"), 
        MySecondIntent("SecondIntentName"),
        MyThirdIntent("ThirdIntentName")
    )
    return lexEventDispatcher.dispatch(event)
```

This module also provides a helper class to define the intents and another helper to build the responses.   
In this example, *MyFirstIntent* class is just a dummy class that uses Lex's default behaviour to process the intent conversation.
```python
from amazon_lex_helper import IntentHandler, LexEvent, LexResponse

class MyFirstIntent (IntentHandler):

    def process_request(self, req: LexEvent):
        return LexResponse.delegate(req)
```

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.

