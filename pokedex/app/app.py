from flask import Flask
from flask import render_template
from flask import request

from pokedex.app.search import search

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    all_pokemons = search()
    return render_template(
        'index.html',
        pokemons=all_pokemons
    )


@app.route('/result')
def search_pokemon():
    query = request.args.get('search_query')
    pokemons_for_query = search(query)
    return render_template(
        'index.html',
        pokemons=pokemons_for_query
    )
