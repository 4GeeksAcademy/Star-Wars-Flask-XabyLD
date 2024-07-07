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
from models import db, User, Planets, Characters, UserFavourites
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


#Get para traenos todos los usuarios de nuestra BBDD
@app.route('/user', methods = ['GET'])
def get_all_characters():

    users = User.query.all()
    all_users = list(map(lambda x: x.serialize(), users))

    return jsonify(all_users), 200
#Get para traer un único usuario de nuestra BBDD
@app.route('/user/<int:id>', methods = ['GET'])
def get_single_character(id):
    #Utilizamos User.query.get para buscar un único elemento en nuestra BBDD
    user = User.query.get(id)
    if user:
        return jsonify(user.serialize()), 200
    else:
        return jsonify({'message': 'No se encuentra el usuario'}),404



#Post para añadir usuarios a nuestra BBDD
@app.route('/user', methods = ['POST'])
def create_new_user():
    request_body = request.get_json()
    new_user = User(
       
        username = request_body['username'],
        password = request_body['password'],
        email = request_body['email']
    )

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify(new_user.serialize()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error creating your username', 'error' : str(e)}), 500   
#Método para borrar 1 usuario
@app.route('/user/<int:id>', methods = ['DELETE'])
def delete_user(id):

    user = User.query.get(id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify('msg  El usuario se ha borrado correctamente')       
    else:
        return jsonify('msg: Error no encontramos al usuario')
#Método para hacer el get de TODOS los planetas
@app.route('/planets', methods = ['GET'])
def get_all_planets():
    planets = Planets.query.all()
    all_planets = list(map(lambda p : p.serialize(), planets))

    return jsonify(all_planets), 200
#Método para hacer el get de un Único planeta
@app.route('/planets/<int:id>', methods = ['GET'])
def get_planet(id):
    planet = Planets.query.get(id)  

    return jsonify(planet.serialize()), 200  

#Post de planetas
@app.route('/planets' , methods= ['POST'])
def create_new_planet():
    request_body = request.get_json()
    new_planet = Planets(
        planet_id = request_body['planet_id'],
        name = request_body['name'],
        distance = request_body['distance'],
        description = request_body['description']
    )

    db.session.add(new_planet)
    db.session.commit()
    return jsonify(new_planet.serialize()),201
#Delete de planeta
@app.route('/planets/<int:id>', methods= ['DELETE'])
def delete_planet(id):
    planet = Planets.query.get(id)

    if planet: 
        db.session.delete(planet)
        db.session.commit()
        return jsonify({"msg": "Planeta eliminado"})
    else:
        return jsonify({"msg": "No se ha encontrado la id del planeta que desea eliminar"})    

#Método para hacer el get de TODOS los personajes
@app.route('/character', methods = ['GET'])
def get_all_character():
    characters = Characters.query.all()
    all_characters = list(map(lambda p : p.serialize(), characters))

    return jsonify(all_characters), 200
#Método para hacer el get de un Único personaje
@app.route('/character/<int:id>', methods = ['GET'])
def get_character(id):
    character = Characters.query.get(id)  

    return jsonify(character.serialize()), 200  

#Post de personaje
@app.route('/character' , methods= ['POST'])
def create_new_character():
    request_body = request.get_json()
    new_character = Characters(
     #character_id = request_body['character.id'],
    name = request_body['name'],
    age = request_body['age'],
    description =request_body['description'],
    gender = request_body['gender'],
    species = request_body['species']
    )

    db.session.add(new_character)
    db.session.commit()
    return jsonify(new_character.serialize()),201
#Delete de character
@app.route('/character/<int:id>', methods= ['DELETE'])
def delete_character(id):
    character = Characters.query.get(id)

    if character: 
        db.session.delete(character)
        db.session.commit()
        return jsonify({"msg": "Personaje eliminado"})
    else:
        return jsonify({"msg": "No se ha encontrado la id del personaje que desea eliminar"})  

#Post de favoritos
@app.route('/favourite/planet/<int:planet_id>', methods=['POST'])
def favourites_planets(planet_id):
    request_body = request.get_json()
    user_id = request_body.get('user_id')

    if not user_id:
        return jsonify({"msg": "User ID is required"}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404

    planet_select = Planets.query.get(planet_id)
    if not planet_select:
        return jsonify({"msg": "Planet not found"}), 404

    user_favourite = UserFavourites(
        user_id=user.id,
        id_planeta=planet_id
    )
    
    db.session.add(user_favourite)
    db.session.commit()
    
    return jsonify(user_favourite.serialize()), 201
#Post de personajes favoritos del usuario
@app.route('/favourite/character/<int:character_id>', methods=['POST'])
def favourites_characters(character_id):
    request_body = request.get_json()
    user_id = request_body.get('user_id')

    if not user_id:
        return jsonify({"msg": "User ID is required"}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404

    character_select = Characters.query.get(character_id)
    if not character_select:
        return jsonify({"msg": "Character not found"}), 404

    user_favourite = UserFavourites(
        user_id=user.id,
        id_personaje=character_id
    )
    
    db.session.add(user_favourite)
    db.session.commit()
    
    return jsonify(user_favourite.serialize()), 201

#Get de todos los favoritos de todos los usuarios
@app.route('/user/favourite', methods=['GET']) 
def get_favourites():
    favourites = UserFavourites.query.all()
    all_favourites = list(map(lambda x: x.serialize(), favourites))

    return jsonify(all_favourites), 201


#Delete de planetas favoritos
@app.route('/favourite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favourite_planet(planet_id):
    request_body = request.get_json()
    user_id = request_body.get('user_id')

    if user_id is None:
        return jsonify({"msg": "Se requiere user_id en el cuerpo de la solicitud"}), 400

    delete_planet = UserFavourites.query.filter_by(user_id=user_id, id_planeta=planet_id).first()

    if delete_planet:
        db.session.delete(delete_planet)
        db.session.commit()
        return jsonify({"msg": "Planeta favorito eliminado con éxito"}), 200
    else:
        return jsonify({"msg": "No se encontró el planeta favorito para eliminar"}), 404 


@app.route('/favourite/character/<int:character_id>', methods = ['DELETE'])
def delete_favourite_character(character_id):
    request_body = request.get_json()
    user_id = request_body.get('user_id')

    eliminar_personaje = UserFavourites.query.filter_by(user_id = user_id , id_personaje = character_id).first()

    if eliminar_personaje:
        db.session.delete(eliminar_personaje)
        db.session.commit()
        return jsonify({'msg': 'Personaje elimiado correctamente'})
    else:
        return jsonify({'msg': 'No encontramos la id del personaje que desea eliminar'})            
      
# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
