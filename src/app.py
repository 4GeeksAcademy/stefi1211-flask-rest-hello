"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planet, FavPeople, FavPlanet
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/people', methods=['GET'])
def get_people():
    all_people = People.query.all()
    return jsonify([people.serialize() for people in all_people]), 200

@app.route('/people/<int:id>', methods=['GET'])
def get_peoplebyid(id):
    try:
        infoPeople = People.query.filter_by(id=id).one_or_none()
        return jsonify(infoPeople.serialize()), 200
    except Exception as err:
        return jsonify({"message": "Ah ocurrido un error inesperado ‼️" + str(err)}), 500

@app.route('/planets', methods=['GET'])
def get_planets():
    all_planets = Planet.query.all()
    return jsonify([planet.serialize() for planet in all_planets]), 200

@app.route('/planets/<int:id>', methods=['GET'])
def get_planetbyid(id):
    try:
        infoPlanet = Planet.query.filter_by(id=id).one_or_none()
        return jsonify(infoPlanet.serialize()), 200
    except Exception as err:
        return jsonify({"message": "Ah ocurrido un error inesperado ‼️" + str(err)}), 500

@app.route('/user', methods=['GET'])
def get_users():
    all_users = User.query.all()
    return jsonify([user.serialize() for user in all_users]), 200

@app.route('/users/favorites', methods=['GET'])
def get_AllFavorites():
    try:
        listFavs = []
        listFavsPeople = FavPeople.query.all()
        listFavsPlanets = FavPlanet.query.all()
        listFavs = listFavsPeople + listFavsPlanets
        return jsonify([favorito.serialize() for favorito in listFavs]), 200
    except Exception as err:
        return jsonify({"message": "Ah ocurrido un error inesperado ‼️" + str(err)}), 500

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def setFavoritePlanet(planet_id):
    body = request.json
    try:
        user = User.query.filter_by(id=body['id']).one_or_none()
        favorite = FavPlanet(planet_id, user.id)
        db.session.add(favorite) 
        db.session.commit()
        return jsonify(favorite.serialize()), 200
    except Exception as err:
        return jsonify({"message": "Ah ocurrido un error inesperado ‼️" + str(err)}), 500

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def setFavoritePeople(people_id):
    body = request.json  
    try:
        user = User.query.filter_by(id=body['id']).one_or_none()
        favorite = FavPeople(people_id, user.id)
        db.session.add(favorite) 
        db.session.commit()
        return jsonify(favorite.serialize()), 200
    except Exception as err:
        return jsonify({"message": "Ah ocurrido un error inesperado ‼️" + str(err)}), 500

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def deleteFavoritePlanet(planet_id):
    body = request.json 
    try:
        aux_favorite = FavPlanet.query.filter_by(
            idPlanet=planet_id, idUser=body['id']).first()
        if aux_favorite is None:
            return jsonify({"message": "No existe el elemento a eliminar."}), 200
        db.session.delete(aux_favorite)  
        db.session.commit()
        return jsonify(aux_favorite.serialize()), 200
    except Exception as err:
        return jsonify({"message": "Ah ocurrido un error inesperado ‼️" + str(err)}), 500

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def deleteFavoritePeople(people_id):
    body = request.json 
    try:
        aux_favorite = FavPeople.query.filter_by(
            people_id=people_id, user_id=body['id']).first()
        if aux_favorite is None:
            return jsonify({"message": "No existe el elemento a eliminar."}), 200
        db.session.delete(aux_favorite)  
        db.session.commit()
        return jsonify(aux_favorite.serialize()), 200
    except Exception as err:
        return jsonify({"message": "Ah ocurrido un error inesperado ‼️" + str(err)}), 500

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

