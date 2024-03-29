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
    if ip in ['128.199.120.29','127.0.0.1']:
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

        if "sort_by" not in json_input:
            json_input["sort_by"] = "publish"

        if "order" not in json_input:
            json_input["order"] = "asc"

        if helper.check_datetime(json_input["begin"]) == False:
            return {"error":"begin date format exception"}

        if helper.check_datetime(json_input["end"]) == False:
            return {"error":"begin date format exception"}


        client = ionelasticsearch.get_instance()

        if len(json_input["media"]) > 0:
            providers = json_input["media"]
        else:
            providers = ionelasticsearch.get_medias()

        page_size = json_input["page_size"]
        from_page = json_input["from_page"]
        keyword = json_input["keyword"].lower()
        if json_input["sort_by"] in ["timestamp","publish","title"]:
            sort_by = json_input["sort_by"]
        else:
            sort_by = "publish"

        if json_input["order"] in ["asc","desc"]:
            order = json_input["order"]
        else:
            order = "asc"

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
        s = s.query(q).sort({sort_by : {"order":order}}).extra(from_=from_page, size=page_size)
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

        # Because field title is analyzed, so elasticsearch will sort with full text sorting
        # so, we use manual sort of string for title
        if sort_by == "title":
            if order == "desc":
                news = sorted(news, key=lambda x: x["title"], reverse=True)
            else:
                news = sorted(news, key=lambda x: x["title"], reverse=False)

        result = {}
        result["result"] = []
        result["result"].append({"news":news})



        result["total"] = total
        return result
