from flask.ext import restful
from flask import request
from elasticsearch_dsl import Search, Q
import settings
import helper
import ionelasticsearch

class MediaShareSummary(restful.Resource):
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

        if helper.check_datetime(json_input["begin"]) == False:
            return {"error":"begin date format exception"}

        if helper.check_datetime(json_input["end"]) == False:
            return {"error":"begin date format exception"}


        client = ionelasticsearch.get_instance()

        keyword = json_input["keyword"].lower()
        begin = helper.create_timestamp(json_input["begin"])
        end = helper.create_timestamp(json_input["end"])

        s = Search(using=client, index=settings.ES_INDEX) \
            .filter("range",**{'publish': {"from": begin,"to": end}})

        q = Q("multi_match", query=keyword, fields=['content'])
        s = s.query(q)
        s.aggs.bucket("group_by_state","terms",field="provider")

        result = s.execute()

        output = {}

        if len(json_input["media"]) > 0:
            for a in json_input["media"]:
                output[a] = 0
        else:
            provider = Search(using=client, index=settings.ES_INDEX)
            provider.aggs.bucket("group_by_state","terms",field="provider",size=0)

            provider_result = provider.execute()
            providers = provider_result.aggregations.group_by_state.buckets

            for a in providers:
                output[a.key] = 0

        for a in result.aggregations.group_by_state.buckets:
            if len(json_input["media"]) == 0 or a.key in json_input["media"]:
                output[a.key] = a.doc_count

        if "rakyat.com" in output and "pikiran" in output:
            output["pikiran-rakyat.com"] = output["rakyat.com"]
            output.pop("rakyat.com")
            output.pop("pikiran")

        if "bbc.co.uk" in output and "indonesia" in output:
            output["bbc.co.uk/indonesia"] = output["bbc.co.uk"]
            output.pop("bbc.co.uk")
            output.pop("indonesia")

        result = {}
        result["result"] = []
        result["result"].append({"media":output})
        return result
