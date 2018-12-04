from flask_api import FlaskAPI
from instance.config import app_config
from flask import request, jsonify, abort
from genius.api import GeniusApi
from app.response_cleaner import GeniusResponseCleaner


def create_app(config_name):

    config = app_config[config_name]
    genius_api = GeniusApi(config.GENIUS_ACCESS_TOKEN)
    cleaner = GeniusResponseCleaner()

    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(config)
    app.config.from_pyfile('config.py')

    @app.route('/v1/search', methods=['GET'])
    def search():
        q = request.args.get('q')
        resp = genius_api.search(q)
        return list(map(lambda d: cleaner.clean_song(d['result']), resp['response']['hits']))

    @app.route('/v1/song/<int:id>', methods=['GET'])
    def get_song(id):
        resp = genius_api.get_song(id)
        song = resp['response']['song']
        return cleaner.clean_song(song)

    @app.route('/v1/artist/<int:id>') 
    def get_artist(id):
        resp = genius_api.get_artist(id)
        artist = resp['response']['artist']
        return cleaner.clean_artist(artist)

    @app.route('/v1/album/<int:id>') 
    def get_album(id):
        resp = genius_api.get_album(id)
        album = resp['response']['album']
        return cleaner.clean_album(album)

    @app.route('/v1/lyrics/<string:path>', methods=['GET'])
    def get_lyrics(path):
        return genius_api.get_lyrics(path)

    @app.route('/v1/lyrics', methods=['GET'])
    def search_lyrics():
        q = request.args.get('q')
        resp = genius_api.search(q)
        song = resp['response']['hits'][0]['result']
        lyrics = genius_api.get_lyrics(song['path'])
        song['lyrics'] = lyrics
        return cleaner.clean_song(song)

    return app