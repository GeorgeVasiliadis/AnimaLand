from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

#for the user
#user.petitions--> returns me a list of user's petitions
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)

    petitions = db.relationship('Petition', backref='user', lazy=True)
    quotes= db.relationship('Quote', backref='author', lazy=True)

#for the petitions
class Petition(db.Model):
    id_petition= db.Column(db.Integer, primary_key=True)
    signature=db.Column(db.String(120), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('person.id'),nullable=False)

#for quotes
#author.quotes--> return a list of user's quotes
class Quotes(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    quote=db.Column(db.String(120), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('person.id'),nullable=False)
