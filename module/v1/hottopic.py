from flask.ext import restful
from flask import request
from flask_httpauth import HTTPBasicAuth
from elasticsearch_dsl import Search, Q
import settings
import helper
import ionelasticsearch
import nltk
from nltk.util import ngrams
from collections import Counter
import time
import string

from model.user import  User

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

class HotTopic(restful.Resource):

    def __init__(self):
        self.words = Counter()
        # get stop words
        self.stopwords = None
        with open("stopwords.txt") as f:
            self.stopwords = f.read().splitlines()

    @auth.login_required
    def get(self):
        return {'hello': 'world'}

    @auth.login_required
    def post(self):
        """
        to get word frequency
        :return: word frequency response
        """

        #check all input
        json_input = request.get_json(force=True)

        if "date" not in json_input:
            json_input["date"] = time.strftime("%Y-%m-%d %I:%M:%S")

        if helper.check_datetime(json_input["date"]) == False:
            return {"error":"begin date format exception"}

        if "limit" not in json_input:
            json_input["limit"] = 100

        client = ionelasticsearch.get_instance()

        providers = ionelasticsearch.get_medias()

        limit = json_input["limit"]
        end = helper.create_timestamp(json_input["date"])

        begin = helper.add_days_timedelta(helper.create_date(json_input["date"]), -2)
        begin_string = begin.strftime("%Y-%m-%d %H:%M:%S")
        begin = helper.create_timestamp(begin_string)

        s = Search(using=client, index=settings.ES_INDEX) \
            .filter("terms",provider=providers,execution="or")\
            .filter("range",**{'publish': {"from": begin,"to": end}})
        q = Q("match_all")
        s = s.query(q).sort({"publish" : {"order":"asc"}}).extra(from_=0, size=1000)
        result = s.execute()

        self.count_generator(result)

        resultwords = {}
        for w in self.words.most_common(limit):
            if w[0] not in(""):
                resultwords[w[0]] = w[1]

        result = {}
        result["result"] = []
        result["result"].append({"words": resultwords})
        return result

    def count_generator(self, result):
        for i in result:
            self.count_content(i.title)

    def count_content(self, title):
        title = title.lower()
        title = title.replace(",","").replace(".","")
        title = title.replace(";","").replace(":","")
        title = title.replace("?","").replace("!","")
        title = title.replace("<","").replace(">","")
        title = title.replace("(","").replace(")","")
        title = title.replace("{","").replace("}","")
        title = title.replace("[","").replace("]","")
        title = title.replace("+","").replace("-","")
        title = title.replace("\\","").replace("/","")
        title = title.replace("=","").replace("*","")
        title = title.replace("'","").replace("\"","")
        title = title.replace("@","").replace("#","").replace("$","").replace("%","").replace("^","")
        title = title.replace("~","")

        stopwords_set = set(self.stopwords)
        tokenize = nltk.word_tokenize(title)
        tokenize = [w for w in tokenize if not w in stopwords_set]

        for phrase in ngrams(tokenize, 2):
            if all(word not in string.punctuation for word in phrase):
                self.words[self.untokenize(phrase)] += 1

        for phrase in ngrams(tokenize, 3):
            if all(word not in string.punctuation for word in phrase):
                self.words[self.untokenize(phrase)] += 1


    def untokenize(self, ngram):
        tokens = list(ngram)
        return "".join([" "+ i if not i.startswith("'") and \
                             i not in string.punctuation and \
                             i != "n't"
                          else i for i in tokens]).strip()