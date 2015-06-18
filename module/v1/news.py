from flask.ext import restful
from flask import request
from elasticsearch_dsl import Search, Q
import settings
import helper
import ionelasticsearch
from flask_httpauth import HTTPBasicAuth
from model.user import  User

auth = HTTPBasicAuth()

@auth.get_password
def get_pw(username):
    ip =  request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    if ip not in ['128.199.120.29','127.0.0.1']:
        return "unused"

    user = User.verify_auth_token(username)
    if user:
        return "unused"
    else:
        return "block"

class News(restful.Resource):
    @auth.login_required
    def get(self):
        return {'hello': 'world'}

    @auth.login_required
    def post(self):
        """
        to get news
        :return: newsresponse
        """

        #check all input
        json_input = request.get_json(force=True)

        if "media" not in json_input:
            json_input["media"] = []

        if "keyword" not in json_input:
            return {"error":"keyword required"}

        if "begin" not in json_input:
            return {"error":"begin date required"}

        if "end" not in json_input:
            return {"error":"begin end required"}

        if "page_size" not in json_input:
            json_input["page_size"] = 20

        if "from_page" not in json_input:
            json_input["from_page"] = 0


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

        page_size = json_input["page_size"]
        from_page = json_input["from_page"]
        keyword = json_input["keyword"].lower()
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
            .filter("terms",provider=providers,execution="or")\
            .filter("range",**{'publish': {"from": begin,"to": end}})
        q = Q("multi_match", query=keyword, fields=['content'], type=match_type)
        s = s.query(q).extra(from_=from_page, size=page_size)
        result = s.execute()

        total = result.hits.total

        news = []
        for i in result:
            item = {}
            item["title"] = i.title
            item["url"] = i.url
            item["content"] = i.content
            item["publish"] = i.publish

            if(isinstance(i.author, basestring)):
                item["auhtor"] = i.author
            else:
                item["author"] = str(i.author)

            if(isinstance(i.location, basestring)):
                item["location"] = i.location
            else:
                item["location"] = i.location[0]

            item["provider"] = i.provider
            item["date_crawl"] = i.timestamp
            news.append(item)

        result = {}
        result["result"] = []
        result["result"].append({"news":news})
        result["total"] = total
        return result
