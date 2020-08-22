from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

from pokedex.settings import DOC_TYPE
from pokedex.settings import ELASTICSEARCH_HOSTS
from pokedex.settings import INDEX_NAME


def search(term=None):
    client = Elasticsearch(ELASTICSEARCH_HOSTS)
    s = Search(using=client, index=INDEX_NAME, doc_type=DOC_TYPE)
    if not term:
        # Show all pokemons on homepage
        query = {
            'match_all': {}
        }
    else:
        # Show pokemons matching the `name`, `japanese_name`, `type1` or `type2`
        query = {
            "multi_match": {
                "query": term,
                "type": "best_fields",
                "fields": [
                    "doc.name",
                    "doc.japanese_name",
                    "doc.type1",
                    "doc.type2"
                ]
                , "operator": "and"
            },
        }
    sort = [
        {
            "doc.pokedex_number": {
                "order": "asc"
            }
        }
    ]
    docs = s.query(query).sort(*sort)[:100].execute()
    return [
        {
            'name': hit.doc.name,
            'japanese_name': hit.doc.japanese_name,
            'pokedex_number': str(hit.doc.pokedex_number).zfill(3),
        } for hit in docs]
