from flask.ext import restful
from model.user import User
import ionelasticsearch
from flask_httpauth import HTTPBasicAuth


auth = HTTPBasicAuth()

@auth.get_password
def get_pw(username):
    user = User.verify_auth_token(username)
    if user:
        return "unused"
    else:
        return "block"

class Medias(restful.Resource):
    @auth.login_required
    def get(self):
        """
        to get list media
        :return: list of media
        """
        medias = ionelasticsearch.get_medias()
        result = {}
        result["result"] = medias
        return result