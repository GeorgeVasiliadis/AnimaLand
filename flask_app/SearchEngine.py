"""
Module used to provide a searching engine on top of Petition objects.
"""

from . import db
from .models import Petition

def scorePetition(petition, *keywords):
    """Examine the given petition and return its relevance score againts the
    given keywords."""

    score = 0

    for key in keywords:

        # Normalize both key and strings to be searched
        key = key.lower()
        title = petition.title.lower()
        content = petition.content.lower()

        # Score eache part of the Petition depending on the number of occurancies
        titleScore = title.count(key)
        contentScore = content.count(key)

        # Give more weight to the keys found in title
        score += titleScore*50 + contentScore

    return score

def search(*keywords):

    # Fetch Petitions
    petitions = Petition.query.all()

    # For each Petition, append its score along with itself into the
    # relevanceList
    relevanceList = [
        (scorePetition(petition, *keywords), petition)
        for petition in petitions
    ]

    # Sort: place more relevant (high-scored) petitinos first
    relevanceList.sort(key=lambda struct: struct[0], reverse=True)

    # Clean: remove irrelevant (zero-occurancies)
    relevanceList = [x[1] for x in relevanceList if x[0] > 0]

    return relevanceList
