import requests
import os
from bs4 import BeautifulSoup

class GeniusApi:

    site_url = 'https://genius.com'
    api_url = 'https://api.genius.com'

    def __init__(self, token):
        """initialize with Genius API Token."""
        self.headers = {
            'Authorization': 'Bearer ' + token,
            'Content-Type': 'application/json; charset=utf-8'
        }
    
    def search(self, query):
        search_url = self.api_url + '/search'
        params = {'q': query}
        return requests.get(search_url, params=params, headers=self.headers).json()

    def get_song(self, id):
        song_url = self.api_url + '/songs/' + str(id)
        return requests.get(song_url, headers=self.headers).json()

    def get_artist(self, id):
        artist_url = self.api_url + '/artists/' + str(id)
        return requests.get(artist_url, headers=self.headers).json()

    def get_album(self, id):
        album_url = self.api_url + '/albums/' + str(id)
        return requests.get(album_url, headers=self.headers).json()

    def get_lyrics(self, path):
        page_url = self.site_url + self.__prepare_path(path)
        page = requests.get(page_url)
        return self.__extract_lyrics(page)

    def __extract_lyrics(self, page):
        html = BeautifulSoup(page.text, 'html.parser')
        return html.find('div', class_='lyrics').get_text()

    def __prepare_path(self, path):
        if path[0] == '/':
            return path
        else:
            return '/' + path