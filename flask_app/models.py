from flask_login import UserMixin
from . import db

# Simple table defining the many-to-many relationship between Users and Petitions
signs = db.Table("signs",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column("petition_id", db.Integer,db.ForeignKey("petition.id"), primary_key=True)
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(80), nullable=False)
    isAdmin = db.Column(db.Boolean, nullable=False, default=False)
    signedPetitions = db.relationship("Petition", secondary=signs, lazy="subquery",
        backref=db.backref("signees", lazy=True)
    )

class Petition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False, unique=True)
    content = db.Column(db.Text, nullable=False)
    goal = db.Column(db.Integer, nullable=False)
    imagePath = db.Column(db.String(200), nullable=False)

    def signCount(self):
        return len(self.signees)
