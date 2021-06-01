import random

# General format of pack: Tuple of quote and author - ("quote", "author")
# Quotes is a list of packs

quotes = [
("Love the Earth as you would love yourself.", None),
("Be a part of the solution, not a part of the pollution.", None),
("The Earth does not belong to man. Man belongs to the Earth!", None),
("The Earth is what we all have in common.", "Wendell Berry"),
("Nature is painting for us, day after day, pictures of infinite beauty.", "Jon Ruskin"),
("The Earth is a fine place and worth fighting for.", "Ernest Hemingway"),
("What I stand for, is what I stand on.", "Wendell Berry"),
("The world owes you nothing. It was here first.", "Mark Twain"),
("If you love the Earth, it will love you back.", None),
("Make the planet great again.", None),
("The Best Way To Get Started Is To Quit Talking And Begin Doing.", "Walt Disney")
]

def randomQuote():
    pack = random.choice(quotes)
    return pack
