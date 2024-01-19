from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favpeople = db.relationship('FavPeople', backref="User", lazy=True)
    favplanet = db.relationship('FavPlanet', backref="User", lazy=True) 

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.is_active = True

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            # do not serialize the password, its a security breach
        }

class People(db.Model):
    __tablename__ = 'People'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    url = db.Column(db.String(80), unique=False, nullable=False)
    favpeople = db.relationship('FavPeople', backref="People", lazy=True)
    def __repr__(self):
        return '<People %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "url": self.url
        }

class FavPeople(db.Model):
    __tablename__ = 'FavPeople'
    id = db.Column(db.Integer, primary_key=True)
    people_id = db.Column(db.Integer, db.ForeignKey("People.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("User.id"), nullable=False)

    def __init__(self, people_id, user_id):
        self.people_id = people_id
        self.user_id = user_id

    def serialize(self):
        people = People.query.get(self.people_id)
        user = User.query.get(self.user_id)
        return {
            "id": self.id,
            "people_id": self.people_id,
            "People" : people.name,
            "user_id": self.user_id,
            "User" : user.username
        }

class Planet(db.Model):
    __tablename__ = 'Planet'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    url = db.Column(db.String(80), unique=False, nullable=False)
    favplanet = db.relationship('FavPlanet', backref="Planet", lazy=True)  

    def __repr__(self):
        return '<Planets %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "url": self.url
        }

class FavPlanet(db.Model):
    __tablename__ = 'FavPlanet'
    id = db.Column(db.Integer, primary_key=True)
    idPlanet = db.Column(db.Integer, db.ForeignKey("Planet.id"), nullable=False)
    idUser = db.Column(db.Integer, db.ForeignKey("User.id"), nullable=False)

    def __init__(self, idPlanet, idUser):
        self.idPlanet = idPlanet
        self.idUser = idUser

    def serialize(self):
        planet = Planet.query.get(self.idPlanet)
        user = User.query.get(self.idUser)
        return {
            "id": self.id,
            "idPlanet": self.idPlanet,
            "Planet" : planet.name,
            "idUser": self.idUser,
            "User" : user.username
        }