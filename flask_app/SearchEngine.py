from . import db
from .models import Petition

def scorePetition(petition, *keywords):
    score = 0
    for key in keywords:
        key = key.lower()
        title = petition.title.lower()
        content = petition.content.lower()

        titleScore = title.count(key)
        contentScore = content.count(key)
        score += titleScore*50 + contentScore
    return score

def search(*keywords):

    # Fetch
    petitions = Petition.query.all()

    # Score
    relevanceList = []
    for petition in petitions:
        score = scorePetition(petition, *keywords)
        relevanceList.append((score, petition))

    # Sort: put more relevant first
    relevanceList.sort(key=lambda struct: struct[0], reverse=True)

    # Clean: remove zero-occurancies
    relevanceList = [x[1] for x in relevanceList if x[0] > 0]

    return relevanceList
