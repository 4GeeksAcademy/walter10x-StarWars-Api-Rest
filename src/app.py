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
from models import db, User, People, Planet
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

#INICIO DE CODIGO

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():
    all_user=User.query.all()
    results = list(map(lambda user: user.serialize(), all_user))
    return jsonify(results), 200

 #Enpoind para buscar people pero por (ID)  
@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    return jsonify(user.serialize()), 200

#Enpoind para buscar people 

@app.route('/people', methods=['GET'])
def get_peoples():
    all_peoples=People.query.all()
    results = list(map(lambda people: people.serialize(), all_peoples))
    return jsonify(results), 200

   


    #Enpoind para buscar people pero por (ID)  
@app.route('/people/<int:people_id>', methods=['GET'])
def get_people(people_id):
    people = People.query.filter_by(id=people_id).first()
    return jsonify(people.serialize()), 200

    #Enpoind para buscar planets 
@app.route('/planets', methods=['GET'])
def get_planet():
    all_planets=Planet.query.all()
    results = list(map(lambda planet: planet.serialize(), all_planets))
    return jsonify(results), 200

#Enpoind para buscar people pero por (ID)  
@app.route('/planets/<int:planet_id>', methods=['GET'])
def planet(planet_id):
    planet = Planet.query.filter_by(id=planet_id).first()
    return jsonify(planet.serialize()), 200


#CREAR ENDPOINT PARA CREAR PLANETAS  [POST]

   
@app.route('/planet', methods=['POST'])
def create_planet():
    data = request.json
    if not 'name' in data:
        return jsonify('error :missing fields'), 400
    
    if data['name'] == "":
     return jsonify({'error': 'Name cannot be empty', 'hint': 'Please enter a valid name'}), 400

    planet = Planet(name = data['name'], description = data['description'])
    db.session.add(planet)
    db.session.commit()
    response_body = {
        "msg": "Planet created successfully"
    }
    return jsonify(response_body), 201

    #CREAR ENDPOINT PARA CREAR PLANETAS  [POST]

@app.route('/people', methods=['POST'])
def create_people():
    data = request.json
    if not 'name' in data:
        return jsonify('error :missing fields'), 400
    
    if data['name'] == "":
     return jsonify({'error': 'Name cannot be empty', 'hint': 'Please enter a valid name'}), 400

    people = People(name = data['name'], description = data['description'])
    db.session.add(people)
    db.session.commit()
    response_body = {
        "msg": "People created successfully"
    }
    return jsonify(response_body), 201
   
    
    # CREAR ENDPOINT PARA ELIMINAR UN PLANETA

@app.route('/planet/<int:planet_id>', methods=['DELETE'])
def delete_planet(planet_id):
     planet = Planet.query.get(planet_id)
     if not planet:
      return jsonify({'message': 'El planeta no existe'}), 404
     
     try:
        db.session.delete(planet)
        db.session.commit()
        return jsonify({'message': 'The planet was successfully eliminated.'}), 200
     except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error while deleting the planet', 'error': str(e)}), 500
     







#FIN CODIGO 

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
