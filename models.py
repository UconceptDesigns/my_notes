from flask_mongoengine import MongoEngine
db = MongoEngine()

class Users(db.Model):
    name = db.StringField()
    user_email = db.StringField()
    
    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "_id": str(self.pk),
            "name": self.name,
            "user_email": self.user_email
        }