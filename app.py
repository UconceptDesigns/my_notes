from flask import Flask, make_response, request
from flask.json import jsonify
from flask_mongoengine import MongoEngine
from flask_cors import CORS

# flask instance
app = Flask(__name__)

DB_URI = "mongodb+srv://admin:admin@cluster0.clad9.mongodb.net/notes_db?retryWrites=true&w=majority"
app.config["MONGODB_HOST"] = DB_URI

CORS(app)
db = MongoEngine()
db.init_app(app)


# books_db Database Squema via class / sample request Body
class Notes(db.Document):
    note_id = db.IntField()
    title = db.StringField()
    details = db.StringField()
    user_email = db.StringField()

    def to_json(self):
        # converts this document to JSON format
        return {
            "note_id": self.note_id,
            "title": self.title,
            "details": self.details,
            "user_email": self.user_email
        }
@app.route('/')
def index():
    return "Flask API"

@app.route('/api', methods=['GET'])
def get_all():
   notes=Notes.objects[:5]
   notes_list = []
   for note in notes:
       print(note.title)
       notes_list.append(note)
   return make_response(jsonify(notes_list), 200)


# WHAT THIS API WILL DO:
# POST /notes_db/db_populate -> Populates the db and returns 201 success code (empty response body)
# First NOTES endpoint:

#  ---------- ADDING MULTIPLE RECORDS -------------
@app.route('/notes_db/db_populate', methods=['POST'])
def db_populate():
    note1 = Notes(note_id=4, title="Note number Four", details = "This is note number four.", user_email="janetgarcia007@gmail.com")
    note2 = Notes(note_id=5, title="Note number Five", details = "This is note number five.", user_email="acruz@gmail.com")
    note3 = Notes(note_id=6, title="Note number Six", details = "This is note number six.", user_email="acruz@gmail.com")
    note1.save()
    note2.save()
    note3.save()
    return make_response("", 201)

#  ---------- ADD SINGLE NOTE -------------
@app.route('/notes_db/add_note', methods=['POST'])
def add_note():
    note = Notes(note_id = 7, title="Note number Seven", details = "This is note number Seven.", user_email = "janetgarcia007@gmail.com")
    note.save()
    return make_response("", 201)


# GET /notes_db/notes_records -> Returns the details of all notes (with code 200 success code)
# POST /notes_db/notes_records -> Creates a new note and returns 201 success code (empty response body)
# Second endpoint

#  ---------- THIS SECTION IS NOT WORKING -------------
@app.route('/notes_db/notes', methods=['GET', 'POST'])
def api_notes():
    if request.method == 'GET':
        notes = []
        for note in Notes.objects:
            notes.append(note)
        return make_response(jsonify(notes), 200)
    elif request.method == 'POST':
        content = request.json
        notes = Notes(note_id=content['note_id'], title=content['title'], details=content['details'], user_email=content['user_email'])
        notes.save()
        return make_response("", 201)


    

# GET /notes_db/notes_records/3 -> Returns the details of note with id 3 (with 200 success code if doc found, 404 if not)
# PUT /notes_db/notes_records/3 -> Updates title and details fields of the note with id 3 (with 204 success code)
# DELETE /notes_db/notes_records -> Deletes note with id 3 (with 204 success code)
# Third endpoint

#  ---------- THIS SECTION IS WORKING -------------

@app.route('/notes_db/notes/<note_id>', methods=['GET', 'PUT', 'DELETE'])
def api_each_note(note_id):
    if request.method == 'GET':
        note_obj = Notes.objects(note_id=note_id).first()
        if note_obj:
            return make_response(jsonify(note_obj.to_json()), 200)
        else:
            return make_response("", 404)
    elif request.method == 'PUT':
        content = request.json
        note_obj = Notes.objects(note_id=note_id).first()
        note_obj.update(title=content['title'], details=content['details'], user_id=content['user_id'])
        return make_response("", 204)
    elif request.method == 'DELETE':
        note_obj = Notes.objects(note_id=note_id).first()
        note_obj.delete()
        return make_response("", 204)
        
if __name__ == '__main__':
    app.run(debug=True)




