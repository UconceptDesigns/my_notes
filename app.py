from flask import Flask, make_response, request, jsonify
from flask_mongoengine import MongoEngine
from flask_cors import CORS
from bson.objectid import ObjectId
import os
from random import randint

app = Flask(__name__)
cors = CORS(app)

@app.route('/')
def index():
    return "Flask API"
DB_URI = "mongodb+srv://admin:admin@cluster0.clad9.mongodb.net/notes_db?retryWrites=true&w=majority"
app.config["MONGODB_HOST"] = DB_URI
db = MongoEngine()
db.init_app(app)

# Notes db squema via class - request Body
class Notes(db.Document):
    # note_id = db.IntField()
    title = db.StringField()
    details = db.StringField()
    user_email = db.StringField()
    def to_json(self):
        # converts this document to JSON format
        return {
            "_id": ObjectId(),
            # "note_id": self.note_id,
            "title": self.title,
            "details": self.details,
            "user_email": self.user_email
        }
        
# Users db squema via class - request Body
class Users(db.Document):
    user_id = db.IntField()
    name = db.StringField()
    user_email = db.StringField()
    def to_json(self):
        # converts this document to JSON format
        return {
            "user_id": self.user_id,
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
            notes.append(note)
        return make_response(jsonify(notes), 200)
    elif request.method == 'POST':
        content = request.json
        notes = Notes(title=content['title'], details=content['details'], user_email=content['user_email'])
        notes.save()
        return make_response("", 201)

#   GET / DELETE note by ID
@app.route('/notes_db/notes/<_id>', methods=['GET', 'DELETE'])
def api_each_note(_id):
    if request.method == 'GET':
        note_obj = Notes.objects(_id).first()
        if note_obj:
            return make_response(jsonify(note_obj.to_json()), 200)
        else:
            return make_response("", 404)
    elif request.method == 'DELETE':
        note_obj = Notes.objects(_id).first()
        note_obj.delete()
        return make_response("", 204)

#   PUT - Update a note by ID
@app.route('/notes_db/notes/<_id>', methods=['PUT'])
def api_update_note(_id):
    content = request.json
    note_obj = Notes.objects(_id).first()
    note_obj.update(title=content['title'], details=content['details'], user_email=content['user_email'])
    return make_response("", 204)

# ----USERS----
#   Get all users / add user
@app.route('/notes_db/users', methods=['GET', 'POST'])
def api_users():
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

#   GET / DELETE user by ID
@app.route('/notes_db/users/<_id>', methods=['GET', 'DELETE'])
def api_each_user(_id):
    if request.method == 'GET':
        user_obj = Users.objects(_id).first()
        if user_obj:
            return make_response(jsonify(user_obj.to_json()), 200)
        else:
            return make_response("", 404)
    elif request.method == 'DELETE':
        user_obj = Users.objects(_id).first()
        user_obj.delete()
        return make_response("", 204)

#   PUT - update user by ID
@app.route('/notes_db/users/<_id>', methods=['PUT'])
def api_update_user(_id):
    content = request.json
    user_obj = Users.objects(_id).first()
    user_obj.update(name=content['name'], user_email=content['user_email'])
    return make_response("", 204)

#   LOGIN
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