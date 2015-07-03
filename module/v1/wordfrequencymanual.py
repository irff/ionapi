from flask.ext import restful
from flask import request
from flask_httpauth import HTTPBasicAuth
from elasticsearch_dsl import Search, Q
import settings
import helper
import ionelasticsearch
import operator
from collections import Counter

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

class WordFrequencyManual(restful.Resource):

    def __init__(self):
        self.words = Counter()
        # get stop words
        self.stopwords = None
        with open(settings.STOPWORDS_LOCATION) as f:
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

        if "media" not in json_input:
            json_input["media"] = []

        if "keyword" not in json_input:
            return {"error":"keyword required"}

        if "begin" not in json_input:
            return {"error":"begin date required"}

        if "end" not in json_input:
            return {"error":"begin end required"}

        if "limit" not in json_input:
            json_input["limit"] = 100


        if helper.check_datetime(json_input["begin"]) == False:
            return {"error":"begin date format exception"}

        if helper.check_datetime(json_input["end"]) == False:
            return {"error":"begin date format exception"}

        client = ionelasticsearch.get_instance()

        if len(json_input["media"]) > 0:
            providers = json_input["media"]
        else:
            providers = ionelasticsearch.get_medias()

        keyword = json_input["keyword"].lower()
        limit = json_input["limit"]
        begin = helper.create_timestamp(json_input["begin"])
        end = helper.create_timestamp(json_input["end"])

        match_type = "best_fields"
        if helper.check_keyword_phrase(keyword):
            """
            if a phrase, change match_type with phrase_prefix
            it make Elasticsearch searching keyword as phrases like "nama saya"
            if match_type use best_fields, Elasticsearch will search with "nama" or "saya"
            """
            match_type = "phrase_prefix"
            keyword = keyword.replace("*","")

        s = Search(using=client, index=settings.ES_INDEX) \
            .filter("terms",provider=providers,execution="or")\
            .filter("range",**{'publish': {"from": begin,"to": end}})
        q = Q("multi_match", query=keyword, fields=['content'], type=match_type)
        s = s.query(q).sort({"publish" : {"order":"asc"}}).extra(from_=0, size=1000)
        result = s.execute()

        self.count_generator(result, keyword)

        resultwords = {}
        for w in self.words.most_common(limit):
            if w[0] not in(""):
                resultwords[w[0]] = w[1]

        result = {}
        result["result"] = []
        result["result"].append({"words": resultwords})
        return result

    def count_generator(self, result, keyword):
        for i in result:
            self.count_content(i.content, keyword)

    def count_content(self, content, keyword):
        content = content.lower()
        content = content.replace(",","").replace(".","")
        content = content.replace(";","").replace(":","")
        content = content.replace("?","").replace("!","")
        content = content.replace("<","").replace(">","")
        content = content.replace("(","").replace(")","")
        content = content.replace("{","").replace("}","")
        content = content.replace("[","").replace("]","")
        content = content.replace("+","").replace("-","")
        content = content.replace("\\","").replace("/","")
        content = content.replace("=","").replace("*","")
        content = content.replace("'","").replace("\"","")
        content = content.replace("@","").replace("#","").replace("$","").replace("%","").replace("^","")
        content = content.replace("~","")
        for word in content.split(" "):
            if(word not in self.stopwords and not word.isdigit() and word not in keyword.split(" ")):
                self.words[word] += 1