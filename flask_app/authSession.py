from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from .models import User, Petition
from . import db

authBlueprint = Blueprint("authBlueprint", __name__)

@authBlueprint.route("/manage-accounts.html")
@login_required
def manage_accounts():
    users = User.query.all()
    return render_template("manage-accounts.html", title="Manage Accounts", users=users)

@authBlueprint.route("/manage/delete/account/<int:id>")
@login_required
def delete_account(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    flash("User was deleted!", "success")
    return redirect(url_for("authBlueprint.manage_accounts"))

@authBlueprint.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("anonymousBlueprint.index"))

@authBlueprint.route("/petition-form.html")
def petition_form():
    return render_template("petition-form.html", title="Petition Form")

@authBlueprint.route("/manage/create/petition", methods=["POST"])
def create_petition():
    title = request.form.get("title")
    content = request.form.get("content")
    goal = request.form.get("goal")

    petition = Petition.query.filter_by(title=title).first()

    if petition:
        flash(
        "There is another petition with the same title. Please choose another name!",
        "danger")
        return redirect(url_for("authBlueprint.petition_form"))

    #todo: content should be checked for markup
    petition = Petition(title=title, content=content, goal=goal)
    db.session.add(petition)
    db.session.commit()

    return redirect(url_for("anonymousBlueprint.sign_a_petition"))
