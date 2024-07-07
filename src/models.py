from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Date, func
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    username = db.Column(db.String(250), nullable=False, unique=True)
    password = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False, unique=True)
    favourites = relationship('UserFavourites', back_populates ='user')
  
    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
         
          "favourites": [favourite.serialize() for favourite in self.favourites ]
            # do not serialize the password, its a security breach
        }
class Characters(db.Model):
    __tablename__ = 'characters'
    character_id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    name = db.Column(db.String(250), nullable=False)
    age = db.Column(db.Integer)
    description = db.Column(db.String(250))
    gender = db.Column(db.String(20))
    species = db.Column(db.String(20))

    def serialize(self):
        return {
            "id": self.character_id,
            "name": self.name,
            "age": self.age,
            "description": self.description,
            "gender": self.gender,
            "species": self.species
            # do not serialize the password, its a security breach
        }

class Planets(db.Model):
    __tablename__ = 'planets'
    planet_id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    name = db.Column(db.String(50), nullable=False)
    distance = db.Column(db.Integer)
    description = db.Column(db.String(250))

    def serialize(self):
        return {
            "planet_id": self.planet_id,
            "name": self.name,
            "distance": self.distance,
            "description": self.description
            # do not serialize the password, its a security breach
        }


class Vehicles(db.Model):
    __tablename__ = 'vehicles'
    vehicle_id = db.Column(db.Integer, primary_key=True,autoincrement = True)
    name = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    created = db.Column(db.DateTime, nullable=False)
    number_passengers = db.Column(db.Integer)
    capacity = db.Column(db.Integer)

class UserFavourites(db.Model):
    __tablename__ = 'user_favourites'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, ForeignKey('user.id'))
    id_personaje = db.Column(db.Integer, ForeignKey('characters.character_id'), nullable=True)
    id_planeta = db.Column(db.Integer, ForeignKey('planets.planet_id'), nullable=True)

    user = relationship("User", back_populates='favourites')
    character = relationship("Characters")
    planet = relationship("Planets")
    
    
    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "character_id": self.id_personaje,
            "planet_id": self.id_planeta
        }        