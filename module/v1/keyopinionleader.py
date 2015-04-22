from flask.ext import restful
from flask import request
from elasticsearch_dsl import Search, Q
import json
import settings
import helper
import ionelasticsearch

class KeyOpinionLeader(restful.Resource):
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
            return {"error":"end date required"}

        if "name" not in json_input:
            return {"error":"list leader name required"}

        if helper.check_datetime(json_input["begin"]) == False:
            return {"error":"begin date format exception"}

        if helper.check_datetime(json_input["end"]) == False:
            return {"error":"begin date format exception"}

        output = {}
        client = ionelasticsearch.get_instance()

        keyword = json_input["keyword"]
        begin = helper.create_timestamp(json_input["begin"])
        end = helper.create_timestamp(json_input["end"])
        for leader in json_input["name"]:
            s = None
            if keyword != "":
                if len(json_input["media"]) > 0:
                    s = Search(using=client, index=settings.ES_INDEX)\
                        .filter("term",content=leader)\
                        .filter("term",provider=json_input["media"])\
                        .filter("range",**{'publish': {"from": begin,"to": end}})\
                        .query("term",content=keyword)
                else:
                    s = Search(using=client, index=settings.ES_INDEX)\
                        .filter("term",content=leader)\
                        .filter("range",**{'publish': {"from": begin,"to": end}})\
                        .query("term",content=keyword)
            else:
                if len(json_input["media"]) > 0:
                    s = Search(using=client, index=settings.ES_INDEX)\
                        .filter("term",content=leader)\
                        .filter("term",provider=json_input["media"])\
                        .filter("range",**{'publish': {"from": begin,"to": end}})
                else:
                    s = Search(using=client, index=settings.ES_INDEX)\
                        .filter("term",content=leader)\
                        .filter("range",**{'publish': {"from": begin,"to": end}})


            result = s.execute()
            print(str(s.to_dict()))
            output[leader] = result.hits.total

        result = {}
        result["result"] = []
        result["result"].append(output)
        return result
