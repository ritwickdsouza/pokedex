import csv

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

from settings import DOC_TYPE
from settings import INDEX_NAME


def main():
    es = Elasticsearch()

    es.indices.delete(index=INDEX_NAME, ignore=404)
    es.indices.create(
        index=INDEX_NAME,
        body={
            'settings': {},
        },
    )

    index_pokemons(es)


def all_pokemons():
    with open('pokemon.csv') as csv_file:
        pokemons = csv.DictReader(csv_file)
        for pokemon in pokemons:
            pokemon['pokedex_number'] = int(pokemon['pokedex_number'])
            yield {
                "_index": INDEX_NAME,
                "_op_type": "create",
                "_type": DOC_TYPE,
                "_id": pokemon['pokedex_number'],
                "doc": pokemon
            }


def index_pokemons(es):
    """ Add a single pokemon to the pokemons index. """
    bulk(es, all_pokemons())


if __name__ == '__main__':
    main()
