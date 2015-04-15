from flask.ext import restful
from flask import request
from elasticsearch_dsl import Search, Q
import settings
import helper
import ionelasticsearch

class MediaShare(restful.Resource):
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

        output = []
        client = ionelasticsearch.get_instance()
        keyword = json_input["keyword"]

        date_begin = helper.create_date(json_input["begin"])
        date_end = helper.create_date(json_input["end"])

        delta = date_end - date_begin
        for i in range(delta.days + 1):
            date_data = {}

            current_date = helper.add_days_timedelta(date_begin, i)

            current_date_string = current_date.strftime("%Y-%m-%d %H:%M:%S")
            next_date_string = helper.add_days_timedelta(current_date, 1).strftime("%Y-%m-%d %H:%M:%S")


            begin = helper.create_timestamp(current_date_string)
            end = helper.create_timestamp(next_date_string)

            s = Search(using=client, index=settings.ES_INDEX)\
                .filter("term",content=keyword)\
                .filter("range",**{'publish': {"from": begin,"to": end}})
            s.aggs.bucket("group_by_state","terms",field="provider")

            result = s.execute()

            date_data["date"] = current_date_string
            date_data["data"] = []
            for a in result.aggregations.group_by_state.buckets:
                if len(json_input["media"]) == 0 or a.key in json_input["media"]:
                    data = {}
                    data[a.key] = a.doc_count
                    date_data["data"].append(data)

            output.append(date_data)

        return output
