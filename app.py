from flask import Flask
from flask.ext import restful

from module.v1.helloworld import HelloWorld
from module.v1.mediashare import MediaShare

app = Flask(__name__)
api = restful.Api(app)

endpoint_pre = '/api/v1/'

api.add_resource(HelloWorld, endpoint_pre + '')
api.add_resource(MediaShare, endpoint_pre + 'mediashare')

if __name__ == '__main__':
    app.run(debug=True)