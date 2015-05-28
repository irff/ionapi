from flask.ext import restful
from flask import request
from elasticsearch_dsl import Search, Q
import json
import settings
import helper
import ionelasticsearch
from flask_httpauth import HTTPBasicAuth
from model.user import  User

auth = HTTPBasicAuth()

@auth.get_password
def get_pw(username):
    user = User.verify_auth_token(username)
    if user:
        return "unused"
    else:
        return "block"

class KeyOpinionLeader(restful.Resource):
    @auth.login_required
    def get(self):
        return {'hello': 'world'}

    @auth.login_required
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

        keyword = json_input["keyword"].lower()
        match_type = "best_fields"
        if helper.check_keyword_phrase(keyword):
            match_type = "phrase_prefix"
            keyword = keyword.replace("*","")

        begin = helper.create_timestamp(json_input["begin"])
        end = helper.create_timestamp(json_input["end"])
        for leader in json_input["name"]:
            s = None

            if len(json_input["media"]) > 0:
                s = Search(using=client, index=settings.ES_INDEX)\
                    .filter("term",content=leader)\
                    .filter("terms",provider=json_input["media"])\
                    .filter("range",**{'publish': {"from": begin,"to": end}})
            else:
                s = Search(using=client, index=settings.ES_INDEX)\
                    .filter("term",content=leader)\
                    .filter("range",**{'publish': {"from": begin,"to": end}})

            q = Q("multi_match", query=keyword, fields=['content'],type=match_type)
            s = s[0:s.count()].query(q)
            result = s.execute()
            output[leader] = result.hits.total

        result = {}
        result["result"] = []
        result["result"].append({"people":output});
        return result
