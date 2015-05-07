from elasticsearch import Elasticsearch
import settings
from elasticsearch_dsl import Search, Q

def get_instance():
    return Elasticsearch(
        [settings.ES_URL]
    )

def get_medias():
    client = Elasticsearch(
        [settings.ES_URL]
    )

    s = Search(using=client, index=settings.ES_INDEX)
    s.aggs.bucket("group_by_state","terms",field="provider",size=0)

    result = s.execute()

    medias = []
    for a in result.aggregations.group_by_state.buckets:
        name = a.key
        if name == "rakyat.com":
            name = "pikiran-rakyat.com"

        if name == "bbc.co.uk":
            name = "bbc.co.uk/indonesia"

        if name not in ["indonesia","pikiran"]:
            medias.append(name)
    return medias
