__author__ = 'Kandito Agung'

from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
import hashlib
import settings

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/iondashboard'
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    iduser = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(45), index = True)
    password = db.Column(db.String(128))
    email = db.Column(db.String(45))
    firstname = db.Column(db.String(65))
    lastname = db.Column(db.String(65))

    def __init__(self, username, password, email, firstname, lastname):
        self.username = username
        self.password = hashlib.sha224(password).hexdigest()
        self.email = email
        self.firstname = firstname
        self.lastname = lastname

    def __repr__(self):
        return '<User %r>' % self.username

    def hash_password(self, password):
        self.password = hashlib.sha224(password).hexdigest()

    def generate_auth_token(self, expiration = 600):
        s = Serializer(settings.SECRET_KEY, expires_in = expiration)
        return s.dumps({ 'id': self.iduser })

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(settings.SECRET_KEY)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None # valid token, but expired
        except BadSignature:
            return None # invalid token
        user = User.query.get(data['id'])
        return user