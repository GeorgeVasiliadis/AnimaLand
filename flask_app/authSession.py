from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_user, logout_user, login_required
from .models import User
from . import db

authBlueprint = Blueprint("authBlueprint", __name__)

@authBlueprint.route("/manage-accounts.html")
@login_required
def manage_accounts():
    users = User.query.all()
    return render_template("manage-accounts.html", users=users)

@authBlueprint.route("/manage/delete/account/<int:id>")
@login_required
def delete_account(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for("authBlueprint.manage_accounts"))

@authBlueprint.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("anonymousBlueprint.index"))
