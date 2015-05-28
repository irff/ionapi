from flask.ext import restful
from model.user import  User
from flask_httpauth import HTTPBasicAuth
import hashlib

auth = HTTPBasicAuth()

@auth.get_password
def get_pw(username):
    user = get_user(username)
    return user.password

@auth.hash_password
def hash_pw(password):
    return hashlib.sha224(password).hexdigest()

def get_user(username):
    return  User.query.filter_by(username=username).first()

class Token(restful.Resource):
    @auth.login_required
    def get(self):
        user = User.query.filter_by(username=auth.username()).first()
        token = user.generate_auth_token()
        result = {}
        result["token"] = token
        return result