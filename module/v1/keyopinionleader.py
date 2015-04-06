from flask.ext import restful
from flask import request
from elasticsearch_dsl import Search, Q
import json
import settings
import ionelasticsearch

class KeyOpinionLeader(restful.Resource):
    def get(self):
        return {'hello': 'world'}

    def post(self):
        json_input = request.get_json(force=True)

        iones = ionelasticsearch.get_instance()
        output = {}
        for leader in json_input['name']:
            client = ionelasticsearch.get_instance()
            s = Search(using=client, index=settings.ES_INDEX)\
                .query("term",content=leader)

            result = s.execute()
            output[leader] = result.hits.total

        return output
