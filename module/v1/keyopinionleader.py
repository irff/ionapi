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

        return output
