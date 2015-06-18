from flask.ext import restful
from flask import request
from elasticsearch_dsl import Search, Q
from elasticsearch_dsl.query import MultiMatch
import settings
import helper
import ionelasticsearch
import operator
from flask_httpauth import HTTPBasicAuth
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
            json_input["media"] = [];

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
            provider = Search(using=client, index=settings.ES_INDEX)
            provider.aggs.bucket("group_by_state","terms",field="provider", size=0)
            provider_result = provider.execute()
            providers = []
            for p in provider_result.aggregations.group_by_state.buckets:
                providers.append(p.key)

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
            .filter("terms",provider=providers)\
            .filter("range",**{'publish': {"from": begin,"to": end}})

        q = Q("multi_match", query=keyword, fields=['content'], type=match_type)

        s = s.query(q)
        result = s[0:s.count()].execute()
        words = {}
        for i in result:
            content = i.content.split(" ")
            for word in content:
                if(word not in words):
                    words[word] = 1
                else:
                    words[word] += 1

        resultwords = {}
        counter = 1
        for w in sorted(words.items(), key=operator.itemgetter(1), reverse=True):
            if w[0] not in(""):
                resultwords[w[0]] = w[1]

            if counter == limit:
                break
            counter += 1

        result = {}
        result["result"] = []
        result["result"].append({"words":resultwords})
        return result
