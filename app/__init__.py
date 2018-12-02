from flask_api import FlaskAPI
from instance.config import app_config
from flask import request, jsonify, abort
from genius.api import GeniusApi

def create_app(config_name):

    config = app_config[config_name]
    genius_api = GeniusApi(config.GENIUS_ACCESS_TOKEN)

    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(config)
    app.config.from_pyfile('config.py')

    @app.route('/v1/search', methods=['GET'])
    def search():
        q = request.args.get('q')
        resp = genius_api.search(q)
        return resp['response']['hits']

    @app.route('/v1/song/<int:id>', methods=['GET'])
    def getSong(id):
        return genius_api.get_song(id)

    @app.route('/v1/lyrics/<string:path>', methods=['GET'])
    def getLyrics(path):
        return genius_api.get_lyrics(path)

    return app