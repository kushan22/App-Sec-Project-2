from app import db
from flask_login import UserMixin
from app import login

class User(UserMixin,db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(64),index=True,unique=True)
    password_hash = db.Column(db.String(128))
    twoFactAuth = db.Column(db.String(9),unique=True)
    user_queries = db.relationship('UserQueries', backref="author", lazy="dynamic")



    def __repr__(self):
        return "<User {}>".format(self.username)


class UserQueries(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    sentence = db.Column(db.String(255))
    misspelled_words = db.Column(db.String(255))
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))

    def __repr__(self):
        return "<User {}>".format(self.sentence)



@login.user_loader
def load_user(id):
    return User.query.get(int(id))



