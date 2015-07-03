from flask.ext import restful
from flask import request
from model.user import User
import ionelasticsearch
from flask_httpauth import HTTPBasicAuth


auth = HTTPBasicAuth()

@auth.get_password
def get_pw(username):
    ip =  request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    if ip in ['128.199.120.29','127.0.0.1']:
        return "unused"

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

        # maybe it will static for long time,
        # so use static content to reduce connection to ES
        medias = ionelasticsearch.get_medias()

        result = {}
        result["result"] = medias
        return result

        # result = {}
        # result["result"] = medias
        # return result
