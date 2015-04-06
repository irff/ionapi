from flask.ext import restful
from flask import request

class MediaShare(restful.Resource):
    def get(self):
        return {'hello': 'world'}

    def post(self):
        json_input = request.get_json(force=True)
        return json_input
