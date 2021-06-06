import random
import json

# General format of pack: Tuple of quote and author - ("quote", "author")
# Quotes is a list of packs

#
quotes = []

# Try to load quotes from file. If that fails, initialize quotes to a simple quote.
try:
    with open("quotes.json") as f_in:
        quotes = json.load(f_in)
except:
    open("DQ_log.txt", "w").write(f"{ __name__ } Warning: Missing source file `quotes.json`!")
    quotes = [["The Earth is a fine place and worth fighting for.", "Ernest Hemingway"]]

def randomQuote():
    pack = random.choice(quotes)
    return pack
