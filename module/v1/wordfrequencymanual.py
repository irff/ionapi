from flask.ext import restful
from flask import request
from elasticsearch_dsl import Search, Q
from elasticsearch_dsl.query import MultiMatch
import settings
import helper
import ionelasticsearch
import operator

class WordFrequencyManual(restful.Resource):
    def get(self):
        return {'hello': 'world'}

    def post(self):
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
        keyword = json_input["keyword"].lower()
        limit = json_input["limit"]
        begin = helper.create_timestamp(json_input["begin"])
        end = helper.create_timestamp(json_input["end"])

        s = Search(using=client, index=settings.ES_INDEX) \
            .filter("range",**{'publish': {"from": begin,"to": end}})

        q = Q("multi_match", query='python django', fields=['title', 'body'])

        s = s.query(q)
        result = s.execute()

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
