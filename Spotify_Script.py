import json

import requests

from secrets import user_id, auth_key


class Cria_playlist:

    def __init__(self, x, y, market='BR', numero_de_playlists=20, size_of_playlist_created=10, underground=0):
        self.palavra_1 = x
        self.palavra_2 = y
        self.market = market
        self.num_playlists = numero_de_playlists
        self.num_tracks = size_of_playlist_created
        self.underground = underground
        self.criou_playlist = self.adicione_tracks_playlist()

    def pesquise_playlist(self):
        '''recebe as playlists com os parametros selecionados'''
        query = "https://api.spotify.com/v1/search?q={}%20{}&type=playlist&market={}&limit={}".format(
            self.palavra_1,
            self.palavra_2,
            self.market,
            self.num_playlists
        )
        response = requests.get(
            query, 
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(auth_key)
            }
        )
        response_json = response.json()
        return response_json
    
    def get_playlists_id(self):
        '''Retorna um dicionário com IDs das playlists'''
        spotify_data = self.pesquise_playlist()
        IDs = list()
        for items in spotify_data['playlists']['items']:
            IDs.append(items['id'])
        
        return IDs
    
    def select_songs_from_playlists(self):
        '''Picks most popular songs from playlists'''
        popular_songs = dict()
        for id in self.get_playlists_id():
            query = "https://api.spotify.com/v1/playlists/{}/tracks?fields=items(track(popularity)),items(track(uri))&limit=100".format(id)
            response = requests.get(
                query,
                headers={
                    "Content-Type": "application/json", 
                    "Authorization": "Bearer {}".format(auth_key)
                }
            )
            response_json = response.json()
            for item in response_json['items']:
                popular_songs.update({item['track']['uri']: item['track']['popularity']})
        
        '''Organizando e selecionando as músicas por popularidade'''
        if self.underground==1:
            popular_songs = sorted(popular_songs.items(), key=lambda x: x[1], reverse=True)
            popular_songs_ids = list(map(lambda x: x[0], popular_songs[-self.num_tracks:]))
        else:
            popular_songs = sorted(popular_songs.items(), key=lambda x: x[1], reverse=True)
            popular_songs_ids = list(map(lambda x: x[0], popular_songs[:self.num_tracks]))
        return popular_songs_ids

    def create_spotify_playlist(self):
        request_body = json.dumps({
            "name": self.palavra_1+'+'+self.palavra_2,
            "description": "Doidera",
            "public": True
        })
        query = "https://api.spotify.com/v1/users/{}/playlists".format(user_id)
        response = requests.post(
            query,
            data=request_body,
            headers={
                "Content-Type": "application/json", 
                "Authorization": "Bearer {}".format(auth_key)
            }
        )
        response_json = response.json()
        return response_json['id']

    def adicione_tracks_playlist(self):
        tracks_uri = self.select_songs_from_playlists()
        uri_parameter = ','.join(tracks_uri)
        query = "https://api.spotify.com/v1/playlists/{}/tracks?uris={}".format(
            self.create_spotify_playlist(),
            uri_parameter
        )
        response = requests.post(
            query,
            headers={
                "Content-Type": "application/json", 
                "Authorization": "Bearer {}".format(auth_key)
            }
        )
        return True


if __name__ == '__main__':
    playlist_1 = Cria_playlist('france', '2020', market='FR', underground=1, size_of_playlist_created=30)
    #playlist_2 = Cria_playlist('auto', 'estima', underground=0, size_of_playlist_created=20)
