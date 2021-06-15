"""
Module used to load a random quote from a standard file.
"""
import random
import json

QUOTES_FILENAME = "flask_app/quotes.json"
LOG_FILENAME = "DQ_log.txt"

def randomQuote():

    # Initialize quotelist with at least one hard-coded quote, as safety-net
    quotes = [["The Earth is a fine place and worth fighting for.", "Ernest Hemingway"]]

    # Try to load quotes from file. If loading fails, log a message to a file
    try:
        with open(QUOTES_FILENAME) as f_in:
            quotes = json.load(f_in)
    except:
        open(LOG_FILENAME, "w").write(f"{ __name__ } Warning: Missing source file `{QUOTES_FILENAME}`!")

    return random.choice(quotes)
