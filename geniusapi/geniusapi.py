import requests
from bs4 import BeautifulSoup
from geniusapi.gat import access_token

class GeniusApi:
    
    site_url = 'https://genius.com'
    api_url = 'https://api.genius.com'
    headers = {
        'Authorization': 'Bearer ' + access_token,
        'Content-Type': 'application/json; charset=utf-8'
        }
    
    def search(self, query):
        search_url = self.api_url + '/search'
        params = {'q': query}
        return requests.get(search_url, params=params, headers=self.headers).json()

    def get_song(self, id):
        song_url = self.api_url + '/songs/' + str(id)
        return requests.get(song_url, headers=self.headers).json()

    def get_lyrics(self, path):
        page_url = self.site_url + '/' + path
        page = requests.get(page_url)
        return {'lyrics': self.extract_lyrics(page)}

    def extract_lyrics(self, page):
        html = BeautifulSoup(page.text, 'html.parser')
        return html.find('div', class_='lyrics').get_text()

genius_api = GeniusApi()