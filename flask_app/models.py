from . import db

#for the user
#user.petitions--> returns me a list of user's petitions
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(80), nullable=False)

#for the petitions
class Petition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    signature=db.Column(db.String(120), unique=True, nullable=False)

#for quotes
#author.quotes--> return a list of user's quotes
class Quote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quote = db.Column(db.String(120), unique=True, nullable=False)
