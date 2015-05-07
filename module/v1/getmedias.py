from flask.ext import restful
import ionelasticsearch

class Medias(restful.Resource):
    def get(self):
        medias = ionelasticsearch.get_medias()
        result = {}
        result["result"] = medias
        return result
