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

        if helper.check_datetime(json_input["begin"]) == False:
            return {"error":"begin date format exception"}

        if helper.check_datetime(json_input["end"]) == False:
            return {"error":"begin date format exception"}


        client = ionelasticsearch.get_instance()

        keyword = json_input["keyword"]
        begin =  helper.create_timestamp(json_input["begin"])
        end = helper.create_timestamp(json_input["end"])

        body = "{" \
                 "\"size\": 0,"\
                  "\"query\": {"\
                    "\"filtered\": {"\
                      "\"query\": {"\
                        "\"query_string\": {"\
                          "\"query\": \"" + keyword + "\","\
                          "\"analyze_wildcard\": true"\
                        "}"\
                      "},"\
                      "\"filter\": {"\
                        "\"bool\": {"\
                          "\"must\": ["\
                            "{"\
                              "\"range\": {"\
                                "\"publish\": {"\
                                  "\"from\": \"" + begin + "\","\
                                  "\"to\": \"" + end + "\""\
                                "}"\
                              "}"\
                            "}"\
                          "],"\
                          "\"must_not\": []"\
                        "}"\
                      "}"\
                    "}"\
                  "},"\
                  "\"aggs\": {"\
                    "\"2\": {"\
                      "\"terms\": {"\
                        "\"field\": \"content\","\
                        "\"size\": 20,"\
                        "\"order\": {"\
                          "\"_count\": \"desc\""\
                        "}"\
                      "}"\
                    "}"\
                  "}"\
                "}"

        res = client.search(index=settings.ES_INDEX, body=body)

        output = {}
        for a in res["aggregations"]["2"]["buckets"]:
            if a["key"] != keyword:
                output[a["key"]] = a["doc_count"]

        result = {}
        result["result"] = [];
        result["result"].append({"words":output})
        return result
