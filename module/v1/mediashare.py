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

class MediaShare(restful.Resource):
    DAILY = "D"
    WEEKLY = "W"
    MONTHLY = "M"
    QUARTERLY = "Q"

    @auth.login_required
    def get(self):
        return {'hello': 'world'}

    @auth.login_required
    def post(self):
        """
        to get media share
        :return: media share response
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

        if helper.check_datetime(json_input["begin"]) == False:
            return {"error":"begin date format exception"}

        if helper.check_datetime(json_input["end"]) == False:
            return {"error":"begin date format exception"}

        output = {}
        output["result"] = []
        client = ionelasticsearch.get_instance()
        keyword = json_input["keyword"].lower()

        date_begin = helper.create_date(json_input["begin"])
        date_end = helper.create_date(json_input["end"])


        provider = Search(using=client, index=settings.ES_INDEX)
        provider.aggs.bucket("group_by_state","terms",field="provider", size=0)
        provider_result = provider.execute()
        providers = provider_result.aggregations.group_by_state.buckets

        delta = date_end - date_begin

        interlude = self.DAILY
        if "interlude" not in json_input:
            total_days = delta.days + 1
            if total_days > 14 and total_days < 30 * 3:
                interlude = self.WEEKLY
            elif total_days >= 30 * 3 and total_days < 30 * 24:
                interlude = self.MONTHLY
            elif total_days >= 30 * 24:
                interlude = self.QUARTERLY
        else:
            interlude = json_input["interlude"]

        data = self.create_new_data(json_input, providers)

        for i in range(delta.days + 1):
            date_data = {}

            current_date = helper.add_days_timedelta(date_begin, i)

            current_date_string = current_date.strftime("%Y-%m-%d %H:%M:%S")
            new_current_date_string = current_date_string[0:10]

            next_date_string = helper.add_days_timedelta(current_date, 1).strftime("%Y-%m-%d %H:%M:%S")

            begin = helper.create_timestamp(current_date_string)
            end = helper.create_timestamp(next_date_string)

            s = Search(using=client, index=settings.ES_INDEX)\
                .filter("range",**{'publish': {"from": begin,"to": end}})

            match_type = "best_fields"
            new_keyword = keyword
            if helper.check_keyword_phrase(keyword):
                """
                if a phrase, change match_type with phrase_prefix
                it make Elasticsearch searching keyword as phrases like "nama saya"
                if match_type use best_fields, Elasticsearch will search with "nama" or "saya"
                """
                match_type = "phrase_prefix"
                new_keyword = keyword.replace("*","")

            q = Q("multi_match", query=new_keyword, fields=['content'], type=match_type)
            s = s.query(q)
            s.aggs.bucket("group_by_state","terms",field="provider", size=0)

            result = s.execute()

            date_data["date"] = new_current_date_string
            date_data["media"] = {}

            for a in result.aggregations.group_by_state.buckets:
                if len(json_input["media"]) == 0 or a.key in json_input["media"]:
                    if interlude == self.DAILY:
                        data[a.key] = a.doc_count
                    else:
                        data[a.key] += a.doc_count

            if (interlude == self.DAILY) or ((i + 1) % 7 == 0 and interlude == self.WEEKLY) or ((i + 1) % 30 == 0 and interlude == self.MONTHLY) or ((i + 1) % 120 == 0 and interlude == self.QUARTERLY):

                if "rakyat.com" in data and "pikiran" in data:
                    data["pikiran-rakyat.com"] = data["rakyat.com"]
                    data.pop("rakyat.com")
                    data.pop("pikiran")

                if "bbc.co.uk" in data and "indonesia" in data:
                    data["bbc.co.uk/indonesia"] = data["bbc.co.uk"]
                    data.pop("bbc.co.uk")
                    data.pop("indonesia")

                date_data["media"] = data
                output["result"].append(date_data)

                data = self.create_new_data(json_input, providers)

        return output

    def create_new_data(self, json_input, providers):
        data = {}

        if len(json_input["media"]) > 0:
            for a in json_input["media"]:
                data[a] = 0
        else:
            for a in providers:
                data[a.key] = 0

        return data