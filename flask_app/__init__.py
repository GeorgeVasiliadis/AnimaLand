from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from .DynamicQuotes import randomQuote

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    db.__init__(app)

    @app.route("/")
    @app.route("/index.html")
    def index():

        # Generate a random quote and parse it to index
        pack = randomQuote()
        quote = pack[0]
        author = pack[1]

        return render_template("index.html", home_active="active", quote=quote, quoteAuthor=author)

    @app.route("/register.html")
    def register():
        return render_template("register.html",ttl="Sign Up")

    @app.route("/login.html")
    def login():
        return render_template("login.html",ttl="Login")

    @app.route("/threats.html")
    def threats():
        return render_template("threats.html",ttl="Threats",threats_active="active")

    @app.route("/targets.html")
    def targets():
        return render_template("targets.html",ttl="Targets", targets_active="active")

    @app.route("/what-can-i-do.html")
    def what_can_i_do():
        return render_template("what-can-i-do.html",ttl="What Can I Do", wcid_active="active")

    @app.route("/sign-a-petition.html")
    def sign_a_petition():
        return render_template("sign-a-petition.html",ttl="Sign a petition", wcid_active="active")

    @app.route("/contact-us.html")
    def contact_us():
        return render_template("contact-us.html",ttl="Contact Us", contact_us_active="active")

    from .authSession import authBlueprint
    app.register_blueprint(authBlueprint)

    return app
