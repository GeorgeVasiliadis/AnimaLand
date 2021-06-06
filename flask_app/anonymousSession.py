from flask import Blueprint
from flask import render_template, redirect, url_for
from flask import request, flash
from flask_login import login_user

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

    return render_template("index.html", title="Home", home_active="active", quote=quote, quoteAuthor=author)

@anonymousBlueprint.route("/register.html")
def register():
    return render_template("register.html", title="Sign Up")

@anonymousBlueprint.route("/register.html", methods=["POST"])
def register_post():
    username = request.form.get("username")
    password = request.form.get("password")
    email = request.form.get("email")

    if User.query.filter_by(email=email).first():
        flash(f"{ email } is already in use!", "danger")
        return redirect(url_for("anonymousBlueprint.register"))

    user = User(email=email, username=username, password=password)
    db.session.add(user)
    db.session.commit()

    return redirect(url_for("authBlueprint.manage_accounts"))

@anonymousBlueprint.route("/login.html")
def login():
    return render_template("login.html", title="Login")

@anonymousBlueprint.route("/login.html", methods=["POST"])
def login_post():
    email = request.form.get("email")
    password = request.form.get("password")

    user = User.query.filter_by(email=email).first()

    if not user:
        flash(f"There is no user with e-mail: { email }", "danger")
        return redirect(url_for("anonymousBlueprint.login"))

    login_user(user)
    flash(f"Welcome { user.username }!", "success")
    return render_template(url_for("anonymousBlueprint.sign_a_petition"))

@anonymousBlueprint.route("/threats.html")
def threats():
    return render_template("threats.html", title="Threats",threats_active="active")

@anonymousBlueprint.route("/targets.html")
def targets():
    return render_template("targets.html", title="Targets", targets_active="active")

@anonymousBlueprint.route("/what-can-i-do.html")
def what_can_i_do():
    return render_template("what-can-i-do.html", title="What Can I Do", wcid_active="active")

@anonymousBlueprint.route("/sign-a-petition.html")
def sign_a_petition():
    return render_template("sign-a-petition.html", title="Sign a petition", wcid_active="active")

@anonymousBlueprint.route("/contact-us.html")
def contact_us():
    return render_template("contact-us.html", title="Contact Us", contact_us_active="active")
