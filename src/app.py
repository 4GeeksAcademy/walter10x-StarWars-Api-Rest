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
    print(results)
    return jsonify(results), 200


#Enpoind para buscar people 

@app.route('/people', methods=['GET'])
def get_peoples():

    all_peoples=People.query.all()
   
    results = list(map(lambda people: people.serialize(), all_peoples))
    print(results)
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

   
    
    
    






#FIN CODIGO 

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
