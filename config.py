import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = '\xab\x16\x0f\xc8\xdf\nB\x08\xfb\xe7\x91\x12\x1bMQb@\r\x07\x9d\xb4\x83\xda\xfe' or 'You will never guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir,'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS  = False
