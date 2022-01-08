from flask import Flask, make_response, request, jsonify, url_for, send_from_directory
from flask_mongoengine import MongoEngine
from flask_cors import CORS
from bson.objectid import ObjectId
import os
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
# from admin import setup_admin
from random import randint

app = Flask(__name__)
cors = CORS(app)


@app.route('/')
def index():
    return "Flask API"
DB_URI = "mongodb+srv://admin:admin@cluster0.clad9.mongodb.net/notes_db?retryWrites=true&w=majority"
app.config["MONGODB_HOST"] = DB_URI

# --new lines entered--
# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "super-secrets9-09itkp0-uuy"
jwt = JWTManager(app)
# --end new lines entered--

db = MongoEngine()
db.init_app(app)

# def setup_admin(app):
#     app.secret_key = os.get('FLASK_APP_KEY', 'sample key')
#     app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
#     admin = Admin(app, name='Uconcept Admin', template_mode='bootstrap3')

# # add the admin
# setup_admin(app)

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

# ----NOTES----
#   GET /notes_db/notes -> Returns the details of ALL notes (with code 200 success code)
#   POST /notes_db/notes -> Creates a New note and returns 201 success code (empty response body)
@app.route('/notes_db/notes', methods=['GET', 'POST'])
def api_notes():
    if request.method == 'GET':
        notes = []
        for note in Notes.objects:
            notes.append(note.to_json())
        return make_response(jsonify(notes), 200)
    elif request.method == 'POST':
        content = request.json
        notes = Notes(title=content['title'], details=content['details'], user_email=content['user_email'])
        notes.save()
        return make_response("", 201)

#   GET / DELETE note by ID
@app.route('/notes_db/notes/<id>', methods=['GET', 'DELETE'])
def api_each_note(id):
    if request.method == 'GET':
        note_obj = Notes.objects(pk=ObjectId(id)).first()
        if note_obj:
            return make_response(note_obj.to_json(), 200)
        else:
            return make_response("", 404)
    elif request.method == 'DELETE':
        note_obj = Notes.objects(pk=ObjectId(id))
        note_obj.delete()
        return make_response("", 204)

#   PUT - Update a note by ID
@app.route('/notes_db/notes/<_id>', methods=['PUT'])
def api_update_note(id):
    content = request.json
    note_obj = Notes.objects(pk=ObjectId(id)).first()
    note_obj.update(title=content['title'], details=content['details'], user_email=content['user_email'])
    return make_response("", 204)

# ----USERS----
#   Get all users / add user
@app.route('/notes_db/users', methods=['GET', 'POST'])
def api_users():
    if request.method == 'GET':
        users = []
        for user in Users.objects:
            users.append(user.to_json())
        return make_response(jsonify(users), 200)
    elif request.method == 'POST':
        content = request.json
        users = Users(name=content['name'], user_email=content['user_email'])
        users.save()
        return make_response("", 201)

#   GET / DELETE user by ID
@app.route('/notes_db/users/<_id>', methods=['GET', 'DELETE'])
def api_each_user(id):
    if request.method == 'GET':
        user_obj = Users.objects(pk=ObjectId(id)).first()
        if user_obj:
            return make_response(user_obj.to_json(), 200)
        else:
            return make_response("", 404)
    elif request.method == 'DELETE':
        user_obj = Users.objects(pk=ObjectId(id))
        user_obj.delete()
        return make_response("", 204)

#   PUT - update user by ID
@app.route('/notes_db/users/<_id>', methods=['PUT'])
def api_update_user(id):
    content = request.json
    user_obj = Users.objects(pk=ObjectId(id)).first()
    user_obj.update(name=content['name'], user_email=content['user_email'])
    return make_response("", 204)

# ==== LOGIN ==== #
@app.route('/token', methods=['POST'])
def create_token():
    username = request.json.get("name", None)
    user_email= request.json.get("user_email", None)
    if username != "test" or user_email != "test@testemail.com
        return jsonify({"msg": "Bad username or email"}), 401

    access_token = create_access_token(identity=user_email)
    return jsonify(access_token=access_token)



# @app.route('/notes_db/user/login/<value>', methods=[ 'POST'])
# def findUser(value):
#     content = request.json
#     users = Users(name=content['name'], user_email=content['user_email'])
#     if db.users.find_one({"user_email": "janetgarcia007@gmail.com"}):
#         return make_response(jsonify(value), 200)

@app.route('/notes_db/login', methods=['GET', 'POST'])
def api_login():
    if request.method == 'GET':
        users = []
        for user in Users.objects:
            users.append(user)
        return make_response(jsonify(users), 200)
    elif request.method == 'POST':
        content = request.json
        users = Users(name=content['name'], user_email=content['user_email'])
        users.save()
        return make_response("", 201)
        
if __name__ == '__main__':
    app.run(debug=True)