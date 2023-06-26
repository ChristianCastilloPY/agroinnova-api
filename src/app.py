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
from models import db, User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

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

@app.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200

@app.route('/create/user', methods = ['POST'])
def create_user():
    body = request.json
    new_user = User.create(body)
    if not isinstance(new_user, User):
        return jsonify({
            "message": new_user["message"],
            "success": False
        }), new_user["status"]
    user = User.query.filter_by(email=new_user.email).one_or_none()
    return jsonify({
        "success": True,
        "message": "User created successfully",
        "data": user.serialize()
    }), 201

@app.route('/login', methods = ["POST"])
def login():
    body = request.json
    valid_credentials = User.verify_credentials(email=body["email"], password=body["password"])
    if not isinstance(valid_credentials, User):
        return jsonify({
            "message": valid_credentials["message"],
            "success": False
        }), valid_credentials["status"]
    access_token = create_access_token(identity=valid_credentials.id)
    return jsonify({
        "message": "Successfully verification",
        "success": True,
        "data": {"token": access_token}
    }), 200

@app.route('/user', methods = ["GET", 'POST'])
@jwt_required()
def get_data_user():
    if request.method == "GET":
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return jsonify({
                "message": "Error getting user info",
                "success": False
            }), 404
        return jsonify({
            "data": user.serialize()
        }), 200
    if request.method == "POST":
        user_id = get_jwt_identity()
        body = request.json
        user_updated = User.update_user(body, user_id)
        if not isinstance(user_updated, User):
            return jsonify({
                "message": user_updated["message"],
                "success": False
            }), user_updated["status"]
        return jsonify({
            "success": True,
            "message": "User updated successfully",
            "data": user_updated.serialize()
        }), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
