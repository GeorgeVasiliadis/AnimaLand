from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from .models import User
from . import db

authBlueprint = Blueprint("authBlueprint", __name__)

@authBlueprint.route("/register.html", methods=["POST"])
def register_post():
    username = request.form.get("username")
    password = request.form.get("password")
    email = request.form.get("email")

    if User.query.filter_by(email=email).first():
        return redirect(url_for("login"))

    user = User(email=email, username=username, password=password)
    db.session.add(user)
    db.session.commit()

    return redirect(url_for("authBlueprint.show"))

@authBlueprint.route("/show.html")
def show():
    users = User.query.all()
    return render_template("show.html", users=users)
