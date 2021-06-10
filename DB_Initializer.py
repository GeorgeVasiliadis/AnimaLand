"""
Database utility module, intended to be used by the "admin" of this web-app.

It is also an important script for the developers as it automates most of the
database manual setup.
"""

import os

from flask_app import create_app, db

DB_PATH = os.path.normpath("flask_app/db.sqlite" )

def install():
    """Create a new one database at `DB_PATH` only if there is no other database
    existing there.
    """

    if not os.path.exists(DB_PATH):
        db.create_all(app=create_app())
        print(f"Database was installed successfully: {DB_PATH}")
        return True

    print(f"Database couldn't be installed. There is already another \
database in use: {DB_PATH}")

    return False

def uninstall():
    """Make sure that the database specified by `DB_PATH` will not exist after
    this operation.

    Succeeds even if the specified database couldn't be found.
    Fails if there is some file IO error.
    """

    if os.path.exists(DB_PATH):
        try:
            os.remove(DB_PATH)
            print(f"Database was uninstalled successfully: {DB_PATH}")
        except Exception as e:
            print(f"Couldn't uninstall database!")
            print(e)
            return False
    else:
        print("There is no database to be uninstalled.")

    return True

def populateUsers():
    """Create the default users and populate database."""

    from flask_app.models import User

    users = [
        User(username="admin", email="admin@animaland.com", password="admin", isAdmin=True),
        User(username="Nikos", email="nikosyro@csd.auth.gr", password="Nikos"),
        User(username="Margarita", email="margsoui@csd.auth.gr", password="Margarita"),
        User(username="Zoe", email="zkelepiri@csd.auth.gr", password="Zoe"),
        User(username="George", email="vgiorgos@csd.auth.gr", password="George")
    ]

    # Add users to database
    for user in users:
        db.session.add(user)

    db.session.commit()
    print("Users were populated successfully!")

def populatePetitions():
    """
    Create the default petitions, populate database and "upload" the dependant
    images.

    This function depends strongly on `dummy` directory which co-exists in same
    directory
    """

    from shutil import copy2
    from flask_app.models import Petition

    petitions = [
        Petition(title="Save the Sharks",
            content=open("dummy/save-the-sharks.html", "r").read(),
            goal=10,
            imagePath="shark.jpg"
        ),
        Petition(title="Animal Testing",
            content=open("dummy/animal-testing.html", "r").read(),
            goal=10,
            imagePath="mouse.jpg"
        ),
        Petition(title="Natural Destruction",
            content=open("dummy/natural-destruction.html", "r").read(),
            goal=10,
            imagePath="bavarian-forest.jpg"
        ),
        Petition(title="Save the Dolophins",
            content=open("dummy/save-the-dolphins.html", "r").read(),
            goal=10,
            imagePath="dolphins.jpg"
        ),
        Petition(title="Stop Ocean Pollution",
            content=open("dummy/stop-ocean-pollution.html", "r").read(),
            goal=10,
            imagePath="trapped-turtle.jpg"
        ),
        Petition(title="Take Climate Action",
            content=open("dummy/take-climate-action.html", "r").read(),
            goal=10,
            imagePath="iceberg.jpg"
        )
    ]

    # Add petitions to database
    for petition in petitions:
        db.session.add(petition)

    db.session.commit()
    print("Petitions were populated successfully!")

    # Copy dummy images into appropriate location in flask_app
    prefix_old = os.path.normpath("dummy/")
    prefix_new = os.path.normpath("flask_app/static/uploads/res/")

    # Ensure that the goal directory exists
    os.makedirs(prefix_new, exist_ok=True)

    for petition in petitions:
        old = os.path.join(prefix_old, petition.imagePath)
        new = os.path.join(prefix_new, petition.imagePath)
        copy2(old, new)

    print("Thumbnail images for petitions were copied successfully!")

def reset():
    """
    Uninstall (if exists) and reinstall the database. Then populate it with the
    default records.

    This function is especially useful for testing purposes when updating the
    database schema.
    """

    if not uninstall():
        print("Aborting...")
        return

    if not install():
        print("Aborting...")
        return
        
    populateUsers()
    populatePetitions()

if __name__ == "__main__":
    reset()
    input("Press any key to exit...")
