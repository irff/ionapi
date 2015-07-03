from elasticsearch import Elasticsearch
import settings
from elasticsearch_dsl import Search, Q

def get_instance():
    return Elasticsearch(
        [settings.ES_URL]
    )

def get_medias():
    """
    to get list of media
    :return: list of media
    """

    return  [
            "kompas.com",
            "antaranews.com",
            "metrotvnews.com",
            "kontan",
            "pikiran-rakyat.com",
            "viva.co.id",
            "thejakartapost.com",
            "suara.com",
            "okezone.com",
            "cnnindonesia.com",
            "bbc.com",
            "merdeka.com",
            "reuters.com",
            "detik.com",
            "bbc.co.uk/indonesia",
            "inilah.com",
            "beritasatu",
            "news.nationalgeographic.com",
            "aljazeera.com",
            "smh.com.au",
            "mediaindonesia.com",
            "swa.co.id",
            "rmol.co",
            "edition.cnn.com",
            "thejakartaglobe.beritasatu.com",
            "bijaks.net",
            "nytimes.com",
            "huffingtonpost.com",
            "bisnis.com",
            "jawapos",
            "tempo.co"
        ]

    """
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
    """