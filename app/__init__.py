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
        resp = genius_api.get_song(id)
        song = resp['response']['song']
        return __clean_song(song)

    @app.route('/v1/lyrics/<string:path>', methods=['GET'])
    def getLyrics(path):
        return genius_api.get_lyrics(path)

    @app.route('/v1/lyrics', methods=['GET'])
    def searchLyrics():
        q = request.args.get('q')
        resp = genius_api.search(q)
        song = resp['response']['hits'][0]['result']
        lyrics = genius_api.get_lyrics(song['path'])
        song['lyrics'] = lyrics
        return __clean_song(song)

    def __clean_song(song):
        keys = [
            'description',
            'embed_content',
            'fact_track', 
            'stats', 
            'current_user_metadata',
            'custom_performances', 
            'description_annotation',
            'song_relationships'
        ]
        for key in keys:
            song.pop(key, None)
        return song

    return app