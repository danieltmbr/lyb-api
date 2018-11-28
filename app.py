from flask import Flask, request
from flask_restful import Resource, Api
from geniusapi.geniusapi import genius_api

app = Flask(__name__)
api = Api(app)

class Search(Resource):
    def get(self):
        q = request.args.get('q')
        return genius_api.search(q)

class Songs(Resource):
    def get(self, id):
        return genius_api.get_song(id)

class Lyrics(Resource):
    def get(self, path):
        return genius_api.get_lyrics(path)

api.add_resource(Search, '/search')
api.add_resource(Songs, '/songs/<int:id>')
api.add_resource(Lyrics, '/lyrics/<string:path>')

if __name__ == '__main__':
    app.run()