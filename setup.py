from setuptools import setup, find_packages
import os

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="amazon-lex-v2-helper",
    packages=['amazon-lex-v2-helper'],
    version="0.1",
    author="rubenafo",
    author_email='rubenafo@amazon.com',
    description="Helper classes to interact with Amazon LexV2 bots",
    url="https://github.com/aws-samples/amazon-lex-v2-helper",
    download_url = 'https://github.com/aws-samples/amazon-lex-v2-helper/amazon-lex-v2-helper-v0.1.tgz',
    keywords = ["amazon-lex", "lex", "chatbot", "voicebot", "nlp", "aws"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Utilities",
        "Development Status :: 4 - Beta",
    ],
    python_requires='>=3.6',
)
