import email
from flask import Flask, make_response, request, jsonify, url_for, send_from_directory
from flask_jwt_extended.utils import get_jwt_header
from flask_mongoengine import MongoEngine
from flask_cors import CORS, cross_origin
from bson.objectid import ObjectId
import os
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from flask_jwt_extended import get_jwt, unset_jwt_cookies
from random import randint
from datetime import datetime, timedelta, timezone

app = Flask(__name__)
cors = CORS(app)
DB_URI = "mongodb+srv://admin:admin@cluster0.clad9.mongodb.net/notes_db?retryWrites=true&w=majority"
app.config["MONGODB_HOST"] = DB_URI
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)

# --Setup the Flask-JWT-Extended extension--
app.config["JWT_SECRET_KEY"] = "super-!x@1-!if;=D;sl:LIew=secrets9-09itkp0-uuy"
jwt = JWTManager(app)
# --end new lines entered--

db = MongoEngine()
db.init_app(app)
# Notes db squema via class - request Body
class Notes(db.Document):
    title = db.StringField()
    details = db.StringField()
    user_email = db.StringField()
    def to_json(self):
        # converts this document to JSON format
        return {
            "_id": str(self.pk),
            "title": self.title,
            "details": self.details,
            "user_email": self.user_email
        }
        
# Users db squema via class - request Body
class Users(db.Document):
    name = db.StringField()
    user_email = db.StringField()
    def to_json(self):
        # converts this document to JSON format
        return {
            "_id": str(self.pk),
            "name": self.name,
            "user_email": self.user_email
        }
@app.route('/')
def index():
    return "Flask API"

# ----NOTES----
#   GET /notes_db/notes -> Returns the details of ALL notes (with code 200 success code)
#   POST /notes_db/notes -> Creates a New note and returns 201 success code (empty response body)
@app.route('/notes_db/notes', methods=['GET', 'POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
@jwt_required()
def api_notes():
    if request.method == 'GET':  
        notes = []
        for note in Notes.objects:
            notes.append(note.to_json())
        return make_response(jsonify(notes), 200)
    elif request.method == 'POST':
        user_token = get_jwt_header()
        Authorization: user_token
        content = request.json
        notes = Notes(title=content['title'], details=content['details'], user_email = content['user_email'])
        notes.save()
        return make_response("", 201)

# =============GET / DELETE note by ID=============#
@app.route('/notes_db/notes/<id>', methods=['GET', 'DELETE'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
@jwt_required() 
def api_each_note(id):
    if request.method == 'GET':
        user_token = get_jwt_header()
        Authorization: user_token
        note_obj = Notes.objects(pk=ObjectId(id)).first()
        if note_obj:
            return make_response(note_obj.to_json(), 200)
        else:
            return make_response("", 404)
    elif request.method == 'DELETE':
        user_token = get_jwt_header()
        Authorization: user_token
        note_obj = Notes.objects(pk=ObjectId(id))
        note_obj.delete()
        return make_response("", 204)

# =============PUT - Update a note by ID=============#
@app.route('/notes_db/notes/<_id>', methods=['PUT'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
@jwt_required() 
def api_update_note(_id):
    user_token = get_jwt_header()
    Authorization: user_token
    content = request.json
    note_obj = Notes.objects(pk=ObjectId(_id)).first()
    note_obj.update(title=content['title'], details=content['details'], user_email=content['user_email'])
    return make_response("", 204)

# ============= LOGIN ============ #
@app.route('/login', methods=['POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def create_token():
    print(request.json.get("name", None))
    print(request.json.get("user_email", None))
    users = Users.objects(name=request.json.get("name"), user_email=request.json.get("user_email",None))
    print(users.to_json())
    if users:
        access_token = create_access_token(identity=request.json.get("user_email", None))
        return jsonify(access_token=access_token), 200
    return jsonify({"msg":"Invalid user name or email. "}), 401

# @app.after_request
# # @cross_origin(origin='*',headers=['Content-Type','Authorization'])
# def refresh_expiring_jwt(response):
#     try:
#         exp_timestamp = get_jwt()["exp"]
#         now = datetime.now(timezone.utc)
#         target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
#         if target_timestamp > exp_timestamp:
#             access_token = create_access_token(identity=get_jwt_identity())
#             return response
#     except (RuntimeError, KeyError):
#         # Return original response if there is no valid JWT.
#         return response

# ============= LOGOUT ============ #
@app.route("/logout", methods=["POST"])
def logout():
    response = jsonify({"msg": "Logout successful"})
    unset_jwt_cookies(response)
    return response

if __name__ == '__main__':
    app.run(debug=True)
