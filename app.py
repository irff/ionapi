from flask import Flask
from flask.ext import restful
from flask.ext.cors import CORS
import logging

from module.v1.helloworld import HelloWorld
from module.v1.mediashare import MediaShare
from module.v1.keyopinionleader import KeyOpinionLeader
from module.v1.wordfrequency import WordFrequency
from module.v1.wordfrequencymanual import WordFrequencyManual
from module.v1.mediasummary import MediaShareSummary
from module.v1.news import News
from module.v1.getmedias import Medias

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)
cors = CORS(app)
api = restful.Api(app)

"""
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response
"""

endpoint_pre = '/api/v1/'

api.add_resource(HelloWorld, endpoint_pre + '')
api.add_resource(MediaShare, endpoint_pre + 'mediashare')
api.add_resource(MediaShareSummary, endpoint_pre + 'mediashare/summary')
api.add_resource(KeyOpinionLeader, endpoint_pre + 'keyopinionleader')
api.add_resource(WordFrequency, endpoint_pre + 'wordfrequency')
api.add_resource(WordFrequencyManual, endpoint_pre + 'wordfrequencymanual')
api.add_resource(News, endpoint_pre + 'news')
api.add_resource(Medias, endpoint_pre + 'listmedia')


if __name__ == '__main__':
    app.run(debug=True,port=8274,host="0.0.0.0")