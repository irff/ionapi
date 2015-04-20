from flask import Flask
from flask.ext import restful

from module.v1.helloworld import HelloWorld
from module.v1.mediashare import MediaShare
from module.v1.keyopinionleader import KeyOpinionLeader
from module.v1.mediasummary import MediaShareSummary

app = Flask(__name__)
api = restful.Api(app)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


endpoint_pre = '/api/v1/'

api.add_resource(HelloWorld, endpoint_pre + '')
api.add_resource(MediaShare, endpoint_pre + 'mediashare')
api.add_resource(MediaShareSummary, endpoint_pre + 'mediashare/summary')
api.add_resource(KeyOpinionLeader, endpoint_pre + 'keyopinionleader')

if __name__ == '__main__':
    app.run(debug=True)