from flask.ext import restful
from flask import request
from elasticsearch_dsl import Search, Q
import settings
import helper
import ionelasticsearch

class News(restful.Resource):
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
            json_input["limit"] = 10


        if helper.check_datetime(json_input["begin"]) == False:
            return {"error":"begin date format exception"}

        if helper.check_datetime(json_input["end"]) == False:
            return {"error":"begin date format exception"}


        client = ionelasticsearch.get_instance()
        limit = json_input["limit"]
        keyword = json_input["keyword"].lower()
        begin = helper.create_timestamp(json_input["begin"])
        end = helper.create_timestamp(json_input["end"])

        s = Search(using=client, index=settings.ES_INDEX) \
            .filter("term",content=keyword) \
            .filter("range",**{'publish': {"from": begin,"to": end}})
        result = s.execute()
        result = result[0:limit]

        news = []
        for i in result:
            item = {}
            item["title"] = i.title
            item["url"] = i.url
            item["content"] = i.content
            item["publish"] = i.publish
            item["author"] = i.author
            item["location"] = i.location
            item["privider"] = i.provider
            item["date_crawl"] = i.timestamp
            news.append(item)

        result = {}
        result["result"] = [];
        result["result"].append({"news":news})
        return result