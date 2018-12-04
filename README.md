# Lyb
**\#quick-and-dirty \#passion-project**

Lyb is a lyrics application which persists lyrics to local storage.
The idea is driven by the frustration of London underground where no network is available hence reading something or listening to something are the only options. Combining these to activity would be great, but with on-demand lyrics services it's just not possible.

### Service

Lyb Api enables clients to search for a song with its information and also scrapes its lyrics if available.
The service is backed by [Genius Api](https://docs.genius.com) and lyrics scraping is using a method described in Will Soares' [blogpost](https://dev.to/willamesoares/how-to-integrate-spotify-and-genius-api-to-easily-crawl-song-lyrics-with-python-4o62).


### Endpoints

**Base url:** https://lyb.herokuapp.com/v1/

- **search?q={_string:search_query_}:**
 
  **GET** request returning a json song list with the top results.

- **song/{_int:id_}:**
  
  **GET** request returning a json song object by id (only metainfo **NO** lyrics attached).

- **artist/{_int:id_}:**
  
  **GET** request returning a json artist object by id.

- **album/{_int:id_}:**
  
  **GET** request returning a json album object by id.
    
- **lyrics/{_string:genius_lyrics_path_}:**
  
  **GET** request returning a text with the lyrics scraped from genius html page. For path use `path` property of song object from previous endpoints' result.

- **lyrics?q={_string:search_query_}:**

  **GET** request combining `search` and `lyrics` endpoints, returning metainfo **and** lyrics as well from the very first song of search result.

### Further improvements  

**Technical stuff:**

- Error handling
- Write tests
- Clean app architecture
