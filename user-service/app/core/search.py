from elasticsearch import Elasticsearch
from app.core.config import settings

es = Elasticsearch(
    settings.ELASTICSEARCH_URL,
    basic_auth=(settings.ELASTICSEARCH_USER, settings.ELASTICSEARCH_PASSWORD),
    verify_certs=False,
)


def index_document(index: str, id: str, body: dict):
    """Index or update a document in Elasticsearch"""
    es.index(index=index, id=id, body=body)


def search_documents(index: str, query: dict):
    """Search documents by query"""
    return es.search(index=index, body=query)
