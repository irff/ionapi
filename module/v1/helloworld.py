from flask.ext import restful

class HelloWorld(restful.Resource):
    def get(self):
        return {'hello': 'world'}
