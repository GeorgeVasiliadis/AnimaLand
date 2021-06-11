import os
from functools import wraps

from flask import Blueprint, render_template, redirect, url_for
from flask import request, flash, current_app
from flask_login import logout_user, login_required, current_user
from werkzeug.utils import secure_filename

from .models import User, Petition
from . import db, allowed_file

authBlueprint = Blueprint("authBlueprint", __name__)

def admin_required(f):
    """
    Utility decorator for managing admin permissions.

    The decorated view will run only if the current user is a fully authenticated
    admin. Otherwise, user will be redirected to index page.

    `wraps` decorator is used to ensure that the wrapped view function retains
    its original name and can be "seen" from other entities.
    """

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

# todo: maybe restrict methods=["POST"]
@authBlueprint.route("/logout")
@login_required
def logout():

    # Log out current user
    logout_user()
    return redirect(url_for("anonymousBlueprint.index"))

@authBlueprint.route("/petition/<int:id>/sign", methods=["POST"])
@login_required
def sign_petition(id):

    # Try to fetch requested petition
    petition = Petition.query.get_or_404(id)

    # If user has already signed current petition, re-signing should be forbidden
    if current_user in petition.signees:
        # Note that this check provides just safety-net functionality. This
        # state is never reached from provided Views.
        flash("You have already signed this petition.", "info")
    else:
        # Update database respecting the new sign
        petition.signees.append(current_user)
        db.session.commit()
        flash("Petition was signed successfully!", "success")

    return redirect(url_for("anonymousBlueprint.display_petition", id=id))

@authBlueprint.route("/petition/<int:id>/unsign", methods=["POST"])
@login_required
def unsign_petition(id):

    # Try to fetch requested petition
    petition = Petition.query.get_or_404(id)

    # If user has already unsigned current petition, re-unsigning should be
    # forbidden
    if current_user in petition.signees:
        # Update database respecting the new unsign
        petition.signees.remove(current_user)
        db.session.commit()
        flash("Petition was unsigned successfully!", "success")
    else:
        # Note that this check provides just safety-net functionality. This
        # state is never reached from provided Views.
        flash("You have't signed this petition yet.", "info")

    return redirect(url_for("anonymousBlueprint.display_petition", id=id))

@authBlueprint.route("/manage-accounts.html")
@admin_required
def manage_accounts():

    # Fetch all registered users
    users = User.query.all()

    # todo: should remove the admin account?
    return render_template("manage-accounts.html", title="Manage Accounts", users=users)

@authBlueprint.route("/manage/delete/account/<int:id>")
@admin_required
def delete_account(id):

    # Try to fetch requested user
    user = User.query.get_or_404(id)

    # Ensure that the admin user will never be deleted
    if user.isAdmin:
        # Note that this check provides just safety-net functionality. This
        # state is never reached from provided Views.
        flash("Admin cannot be deleted!", "danger")
        return redirect(url_for("authBlueprint.manage_accounts"))

    # Delete requested user
    db.session.delete(user)
    db.session.commit()

    flash("User was deleted!", "success")
    return redirect(url_for("authBlueprint.manage_accounts"))

@authBlueprint.route("/petition-form.html")
@admin_required
def petition_form():
    return render_template("petition-form.html", title="Petition Form")

# Both "POST" and "GET" methods should be accepted for image upload.
@authBlueprint.route("/manage/create/petition", methods=["POST", "GET"])
@admin_required
def create_petition():

    if request.method == "POST":

        # Fetch form details
        title = request.form.get("title")
        content = request.form.get("content")
        goal = request.form.get("goal")
        file = request.files['image']

        # Ensure that the given `goal` is a valid integer.
        try:
            goal = int(goal)
        except ValueError:
            # Note that this check provides just safety-net functionality. This
            # state is never reached from provided Views.
            flash("Goal should be an integer", "danger")
            return redirect(url_for("authBlueprint.create_petition"))

        # Ensure that the given `goal` is a non-negative integer.
        if goal <= 0:
            # Note that this check provides just safety-net functionality. This
            # state is never reached from provided Views.
            flash("Goal should be a possitive intger", "danger")
            return redirect(url_for("authBlueprint.create_petition"))

        # Attached file `file` is the petition thumbnail
        if not file.filename:
            flash("No image was selected!", "danger")
            return redirect(request.url)

        # If the attached file has an allowed extension and is valid, store it
        # locally (server side). Else disallow creation of petition.
        if file and allowed_file(file.filename):

            # Ensure that the filename doesn't contain special filepath
            # prefixes like `../`
            filename = secure_filename(file.filename)

            # Ensure that there is no other image stored in uploads with same
            # name to prevent overwriting images. If there are, prepend title to
            # image name.
            if Petition.query.filter_by(imagePath=filename):
                filename = title + "_" + filename

            # Store file into appropriate path
            file.save(os.path.join(current_app.config["UPLOAD_FOLDER"], filename))
        else:
            flash("Attached file is invalid.", "danger")
            return redirect(url_for("authBlueprint.petition_form"))

        # Ensure that the under-construction petition has a unique name
        petition = Petition.query.filter_by(title=title).first()
        if petition:
            flash(
            "There is another petition with the same title. Please choose another name!",
            "danger")
            return redirect(url_for("authBlueprint.petition_form"))

        #todo: content should be checked for markup
        # Create new petition and store it in database
        petition = Petition(title=title, content=content, goal=goal, imagePath=filename)
        db.session.add(petition)
        db.session.commit()

        flash(f'"{title}" was created successfully!', "success")
        return redirect(url_for("anonymousBlueprint.sign_a_petition"))
    return redirect(url_for("authBlueprint.petition_form"))
