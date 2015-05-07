from flask.ext import restful
from flask import request
from elasticsearch_dsl import Search, Q
import settings
import helper
import ionelasticsearch
import json

class WordFrequency(restful.Resource):
    def get(self):
        return {'hello': 'world'}

    def post(self):
        json_input = request.get_json(force=True)

        if "keyword" not in json_input:
            return {"error":"keyword required"}

        if "begin" not in json_input:
            return {"error":"begin date required"}

        if "end" not in json_input:
            return {"error":"begin end required"}

        if "media" not in json_input:
            return {"error":"media required"}

        if "limit" not in json_input:
            json_input["limit"] = 100

        json_input["limit"] += 1

        if helper.check_datetime(json_input["begin"]) == False:
            return {"error":"begin date format exception"}

        if helper.check_datetime(json_input["end"]) == False:
            return {"error":"begin date format exception"}


        client = ionelasticsearch.get_instance()

        keyword = json_input["keyword"].lower()
        begin =  helper.create_timestamp(json_input["begin"])
        end = helper.create_timestamp(json_input["end"])

        if len(json_input["media"]) > 0:
            s = Search(using=client, index=settings.ES_INDEX) \
                .filter("term",provider=json_input["media"])\
                .filter("range",**{'publish': {"from": begin,"to": end}})
        else:
            s = Search(using=client, index=settings.ES_INDEX) \
                .filter("range",**{'publish': {"from": begin,"to": end}})

        q = Q("multi_match", query=keyword, fields=['content'])
        s = s.query(q)
        result = s.execute()

        output = {}
        for a in result.aggregations.group_by_state.buckets:
            if keyword != a.key:
                output[a.key] = a.doc_count

        result = {}
        result["result"] = [];
        result["result"].append({"words":output})
        return result
