from elasticsearch import Elasticsearch
import settings

def get_instance():
    return Elasticsearch(
        [settings.ES_URL]
    )