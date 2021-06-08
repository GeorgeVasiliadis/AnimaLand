import os
from functools import wraps

from flask import Blueprint, render_template, redirect, url_for
from flask import request, flash, current_app
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename

from .models import User, Petition, signs
from . import db, allowed_file

authBlueprint = Blueprint("authBlueprint", __name__)

def admin_required(f):
    @wraps(f)
    def wrapping_function(*args, **kwargs):
        if hasattr(current_user, "isAdmin") and \
            current_user.isAdmin and \
            current_user.is_authenticated:
            return f(*args, **kwargs)
        else:
            flash("This page is intended only for admin!", "danger")
            return redirect(url_for("anonymousBlueprint.index"))
    return wrapping_function

@authBlueprint.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("anonymousBlueprint.index"))

@authBlueprint.route("/petition/<int:id>/sign", methods=["POST"])
@login_required
def sign_petition(id):
    petition = Petition.query.get_or_404(id)

    if current_user in petition.signees:
        flash("You have already signed this petition.", "info")
    else:
        petition.signees.append(current_user)
        petition.signCount += 1
        db.session.commit()
        flash("Petition was signed successfully!", "success")
    return redirect(url_for("anonymousBlueprint.display_petition", id=id))

@authBlueprint.route("/petition/<int:id>/unsign", methods=["POST"])
@login_required
def unsign_petition(id):
    petition = Petition.query.get_or_404(id)

    if current_user in petition.signees:
        petition.signees.remove(current_user)
        petition.signCount -= 1
        db.session.commit()
        flash("Petition was unsigned successfully!", "success")
    else:
        flash("You have't signed this petition yet.", "info")
    return redirect(url_for("anonymousBlueprint.display_petition", id=id))

@authBlueprint.route("/manage-accounts.html")
@admin_required
def manage_accounts():
    users = User.query.all()
    return render_template("manage-accounts.html", title="Manage Accounts", users=users)

@authBlueprint.route("/manage/delete/account/<int:id>")
@admin_required
def delete_account(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    flash("User was deleted!", "success")
    return redirect(url_for("authBlueprint.manage_accounts"))

@authBlueprint.route("/petition-form.html")
@admin_required
def petition_form():
    return render_template("petition-form.html", title="Petition Form")

@authBlueprint.route("/manage/create/petition", methods=["POST", "GET"])
@admin_required
def create_petition():
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        goal = request.form.get("goal")
        file = request.files['image']

        try:
            goal = int(goal)
        except ValueError:
            flash("Goal should be an integer", "danger")
            return redirect(url_for("authBlueprint.create_petition"))
        if goal <= 0:
            flash("Goal should be a possitive intger", "danger")
            return redirect(url_for("authBlueprint.create_petition"))

        # Attached file `file` is the petition thumbnail
        if not file.filename:
            flash("No image was selected!", "danger")
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config["UPLOAD_FOLDER"], filename))

        petition = Petition.query.filter_by(title=title).first()

        if petition:
            flash(
            "There is another petition with the same title. Please choose another name!",
            "danger")
            return redirect(url_for("authBlueprint.petition_form"))

        #todo: content should be checked for markup
        petition = Petition(title=title, content=content, goal=goal, imagePath=filename)
        db.session.add(petition)
        db.session.commit()

        return redirect(url_for("anonymousBlueprint.sign_a_petition"))
