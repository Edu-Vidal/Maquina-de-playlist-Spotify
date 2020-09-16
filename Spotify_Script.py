import json

import requests

from dados_importantes import user_id, auth_key


class cria_playlist:

    def __init__(self, x, y, numero_de_playlists=5):
        self.palavra_1 = x
        self.palavra_2 = y
        self.num_playlists = numero_de_playlists
        
        self.criou_playlist = self.adicione_tracks_playlist()

    def pesquise_playlist(self):
        '''recebe as playlists com os parametros selecionados'''
        query = "https://api.spotify.com/v1/search?q={}%20{}&type=playlist&limit={}".format(
            self.palavra_1,
            self.palavra_2,
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
    
    def select_songs_from_playlists(self, size_of_playlist_created=10):
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
        popular_songs = sorted(popular_songs.items(), key=lambda x: x[1], reverse=True)
        popular_songs_ids = list(map(lambda x: x[0], popular_songs[:size_of_playlist_created]))
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
        id_tracks = self.select_songs_from_playlists()
        uri_parameter = ','.join(id_tracks)
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
    test = cria_playlist('Lucas', 'Du')


