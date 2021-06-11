from flask import Blueprint
from flask import render_template, redirect, url_for
from flask import request, flash
from flask_login import login_user, current_user

from . import db
from .DynamicQuotes import randomQuote
from .models import User, Petition
from . import SearchEngine as SE

anonymousBlueprint = Blueprint("anonymousBlueprint", __name__)

@anonymousBlueprint.route("/")
@anonymousBlueprint.route("/index.html")
def index():

    # Generate a random quote and parse it to index page
    # todo: maybe store quotes in DB?
    quote, author = randomQuote()

    return render_template("index.html", title="Home", home_active="active", quote=quote, quoteAuthor=author)

@anonymousBlueprint.route("/register.html")
def register():
    return render_template("register.html", title="Sign Up")

@anonymousBlueprint.route("/register.html", methods=["POST"])
def register_post():

    # Fetch form details
    username = request.form.get("username")
    password = request.form.get("password")
    email = request.form.get("email")

    # Ensure that the provided email hasn't been registered before
    if User.query.filter_by(email=email).first():
        flash(f"{ email } is already in use!", "danger")
        return redirect(url_for("anonymousBlueprint.register"))


    # Create and store new user
    user = User(email=email, username=username, password=password)
    db.session.add(user)
    db.session.commit()

    # Log in newly-created user
    login_user(user)

    flash(f"Welcome to AnimaLand {username}!", "success")
    return redirect(url_for("anonymousBlueprint.sign_a_petition"))

@anonymousBlueprint.route("/login.html")
def login():
    return render_template("login.html", title="Sign In")

@anonymousBlueprint.route("/login.html", methods=["POST"])
def login_post():

    # Fetch form details
    email = request.form.get("email")
    password = request.form.get("password")

    # Check if user is valid (aka registered)
    user = User.query.filter_by(email=email).first()
    if not user:
        flash(f"There is no user with e-mail: { email }", "danger")
        return redirect(url_for("anonymousBlueprint.login"))

    # Ensure that the user inserted the right credentials
    if not password == user.password:
        flash("The password you inserted is invalid!", "danger")
        return redirect(url_for("anonymousBlueprint.login_post"))

    # Log in user
    login_user(user)

    flash(f"Welcome back { user.username }!", "success")
    return redirect(url_for("anonymousBlueprint.sign_a_petition"))

@anonymousBlueprint.route("/threats.html")
def threats():
    return render_template("threats.html", title="Threats", threats_active="active")

@anonymousBlueprint.route("/targets.html")
def targets():
    return render_template("targets.html", title="Targets", targets_active="active")

@anonymousBlueprint.route("/what-can-i-do.html")
def what_can_i_do():
    return render_template("what-can-i-do.html", title="What Can I Do", wcid_active="active")

@anonymousBlueprint.route("/sign-a-petition.html")
def sign_a_petition():

    # Fetch stored petitions
    petitions = Petition.query.all()

    return render_template("sign-a-petition.html", title="Sign A Petition", wcid_active="active", petitions=petitions)

@anonymousBlueprint.route("/contact-us.html")
def contact_us():
    return render_template("contact-us.html", title="Contact Us", contact_us_active="active")

@anonymousBlueprint.route("/petition/<int:id>")
def display_petition(id):

    # Try to fetch requested petition
    petition = Petition.query.get_or_404(id)

    # Inform an anonymous visitor that sign feature is disabled
    if not current_user.is_authenticated:
        flash("You will not be able to sign a petition. Login with your account first!", "info")

    return render_template("petition.html", title=petition.title, petition=petition, wcid_active="active")

@anonymousBlueprint.route("/search.html", methods=["POST"])
def search_results():

    # Fetch form details
    keywords = request.form.get("keywords")

    # Tokenize keywords removing whitespace characters
    keywords = keywords.split()

    # Search and feth relevant petitions
    relevantPetitions = SE.search(*keywords)

    return render_template("search.html", title="Search Results", relevantPetitions=relevantPetitions)

@anonymousBlueprint.route("/subscribe", methods=["POST"])
def subscribe_to_newsletter():
    flash("You were successfully subscribed to our Newsletter!", "success")
    return redirect(url_for("anonymousBlueprint.index"))
