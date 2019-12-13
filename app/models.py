
from app import db,login
from flask_login import UserMixin



class User(UserMixin,db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(64),index=True,unique=True)
    password_hash = db.Column(db.String(128))
    twoFactAuth = db.Column(db.String(11))
    user_queries = db.relationship('UserQueries', backref="author", lazy="dynamic")
    user_logs = db.relationship('UserLogs',backref='author',lazy="dynamic")



    def __repr__(self):
        return "<User {}>".format(self.username)


class UserQueries(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    sentence = db.Column(db.String(255))
    misspelled_words = db.Column(db.String(255))
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))

    def __repr__(self):
        return "<User {}>".format(self.sentence)

class UserLogs(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    login_time = db.Column(db.DateTime,nullable=True)
    logout_time = db.Column(db.DateTime,nullable=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))

    def __repr__(self):
        return "<UserLogs {}>".format(self.login_time)



@login.user_loader
def load_user(id):
    return User.query.get(int(id))



