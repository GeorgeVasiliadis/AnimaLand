from flask import Flask, render_template

def create_app():
    app = Flask(__name__)

    @app.route("/")
    @app.route("/index.html")
    def index():
        return render_template("index.html",ttl="Home")

    @app.route("/register.html")
    def register():
        return render_template("register.html",ttl="Sign Up")

    @app.route("/login.html")
    def login():
        return render_template("login.html",ttl="Login")

    @app.route("/threats.html")
    def threats():
        return render_template("threats.html",ttl="Threats")

    @app.route("/targets.html")
    def targets():
        return render_template("targets.html",ttl="Targets")

    @app.route("/what-can-i-do.html")
    def what_can_i_do():
        return render_template("what-can-i-do.html",ttl="What Can I Do")

    @app.route("/sign-a-petition.html")
    def sign_a_petition():
        return render_template("sign-a-petition.html",ttl="Sign a petition")

    @app.route("/contact-us.html")
    def contact_us():
        return render_template("contact-us.html",ttl="Contact Us")
    return app
