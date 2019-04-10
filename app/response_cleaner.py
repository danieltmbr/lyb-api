
class GeniusResponseCleaner:

    __clean_album_keys = [
        'api_path',
        'comment_count',
        'custom_header_image_url',
        'header_image_url',
        'lock_state',
        'pyongs_count',
        'release_date_components',
        'current_user_metadata',
        # 'cover_arts',
        'description_annotation',
        'performance_groups',
        'song_performances',
        'song_pageviews',
    ]

    __clean_artist_keys = [
        'followers_count',
        'is_meme_verified',
        'is_verified',
        'header_image_url',
        'translation_artist',
        'user',
        'api_path',
        'description',
        'current_user_metadata',
        'description_annotation',
        'iq',
    ]

    __clean_song_keys = [
        'annotation_count',
        'api_path',
        'header_image_thumbnail_url',
        'header_image_url',
        'lyrics_owner_id',
        'pyongs_count',
        'song_art_image_thumbnail_url',
        'apple_music_id',
        'apple_music_player_url',
        'pyongs_count',
        'lyrics_marked_complete_by',
        'verified_annotations_by',
        'verified_contributors',
        'verified_lyrics_by',
        'description',
        'embed_content',
        'fact_track', 
        'stats', 
        'current_user_metadata',
        'custom_performances', 
        'description_annotation',
        'song_relationships',
        'recording_location',
    ]

    def clean_song(self, song):
        song = self.__clean(song, self.__clean_song_keys)

        if 'album' in song: 
            song['album'] = self.clean_album(song['album'])

        if 'primary_artist' in song: 
            song['primary_artist'] = self.clean_artist(song['primary_artist'])

        if 'writer_artists' in song: 
            song['writer_artists'] = list(map(lambda a: self.clean_artist(a), song['writer_artists']))

        if 'producer_artists' in song: 
            song['producer_artists'] = list(map(lambda a: self.clean_artist(a), song['producer_artists']))

        if 'featured_artists' in song: 
            song['featured_artists'] =  list(map(lambda a: self.clean_artist(a), song['featured_artists']))

        return song

    def clean_artist(self, artist):
        return self.__clean(artist, self.__clean_artist_keys)

    def clean_album(self, album):
        if 'artist' in album: 
            album['artist'] =  self.clean_artist(album['artist'])

        if 'song_performances' in album:
            for item in album['song_performances']:
                if item['label'] == 'Featuring':
                    album['featurings'] = list(map(lambda a: self.clean_artist(a), item['artists']))
                elif item['label'] == 'Producers':
                    album['producers'] = list(map(lambda a: self.clean_artist(a), item['artists']))
                elif item['label'] == 'Writers':
                    album['writers'] = list(map(lambda a: self.clean_artist(a), item['artists']))
                elif item['label'] == 'Executive Producer':
                    album['executive_producers'] = list(map(lambda a: self.clean_artist(a), item['artists']))
                elif item['label'] == 'Label':
                    album['labels'] = list(map(lambda a: self.clean_artist(a), item['artists']))
                else:
                    continue

        album = self.__clean(album, self.__clean_album_keys)

        return album

    def __clean(self, obj, keys):
        for key in keys:
            obj.pop(key, None)
        return obj