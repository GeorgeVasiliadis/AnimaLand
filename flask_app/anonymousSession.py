from flask import Blueprint
from flask import render_template, redirect, url_for
from flask import request

from . import db
from .DynamicQuotes import randomQuote
from .models import User

anonymousBlueprint = Blueprint("anonymousBlueprint", __name__)

@anonymousBlueprint.route("/")
@anonymousBlueprint.route("/index.html")
def index():

    # Generate a random quote and parse it to index
    pack = randomQuote()
    quote = pack[0]
    author = pack[1]

    return render_template("index.html", home_active="active", quote=quote, quoteAuthor=author)

@anonymousBlueprint.route("/register.html")
def register():
    return render_template("register.html",ttl="Sign Up")

@anonymousBlueprint.route("/register.html", methods=["POST"])
def register_post():
    username = request.form.get("username")
    password = request.form.get("password")
    email = request.form.get("email")

    if User.query.filter_by(email=email).first():
        return redirect(url_for("anonymousBlueprint.login"))

    user = User(email=email, username=username, password=password)
    db.session.add(user)
    db.session.commit()

    return redirect(url_for("authBlueprint.manage_accounts"))

@anonymousBlueprint.route("/login.html")
def login():
    return render_template("login.html",ttl="Login")

@anonymousBlueprint.route("/threats.html")
def threats():
    return render_template("threats.html",ttl="Threats",threats_active="active")

@anonymousBlueprint.route("/targets.html")
def targets():
    return render_template("targets.html",ttl="Targets", targets_active="active")

@anonymousBlueprint.route("/what-can-i-do.html")
def what_can_i_do():
    return render_template("what-can-i-do.html",ttl="What Can I Do", wcid_active="active")

@anonymousBlueprint.route("/sign-a-petition.html")
def sign_a_petition():
    return render_template("sign-a-petition.html",ttl="Sign a petition", wcid_active="active")

@anonymousBlueprint.route("/contact-us.html")
def contact_us():
    return render_template("contact-us.html",ttl="Contact Us", contact_us_active="active")
