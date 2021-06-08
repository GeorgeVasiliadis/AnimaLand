from flask_app import create_app, db
from flask_app.models import User, Petition

def createUsers():
    users = [
        User(username="admin", email="admin@animaland.com", password="admin"),
        User(username="Nikos", email="nikosyro@csd.auth.gr", password="Nikos"),
        User(username="Margarita", email="margsoui@csd.auth.gr", password="Margarita"),
        User(username="Zoe", email="zkelepiri@csd.auth.gr", password="Zoe"),
        User(username="George", email="vgiorgos@csd.auth.gr", password="George")
    ]
    for user in users:
        db.session.add(user)
    db.session.commit()

def createPetitions():
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

    for petition in petitions:
        db.session.add(petition)
    db.session.commit()

if __name__ == "__main__":
    app = create_app()
    app.app_context().push()
    createUsers()
    createPetitions()
