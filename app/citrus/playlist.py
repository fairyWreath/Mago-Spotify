import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import pandas 
import time 
import json
import datetime
from mago import *
from yuzu import *
from mei import *
import requests

client_id =  '2ae3de12e0964343a71cc1eaf4b8a6f3'
client_secret = '0fcc3f6cdf784105baee8186d0bd8333'
redirect_uri = 'http://127.0.0.1:8080/'

scope = 'user-top-read user-library-read user-read-recently-played playlist-read-private'
auth_manager = spotipy.oauth2.SpotifyOAuth(client_id, client_secret, redirect_uri, scope=scope)
sp = spotipy.Spotify(auth_manager=auth_manager)


token = auth_manager.get_access_token(as_dict=False)
print(token)
dicts = getPlaylistTracksDict(sp, token)
for key in dicts:
    print(key, end="")
    print(dicts[key])

tracks = getTracksFromPlaylist(dicts['Everything'], token)
for track in tracks:
    print(track['name'])
print(len(tracks))

'''
plays = sp.current_user_playlists(limit=50)
plays = plays['items']
for p in plays:
    print(p['name'])
url = plays[0]['tracks']['href']


token = auth_manager.get_cached_token()['access_token']
print(token)

headers = {
    'Authorization': 'Bearer {token}'.format(token=token)
}

response = requests.get(url, headers=headers, params={'limit': '10'})
content = response.json()
items = content['items']
print(len(items))
'''



'''
token = auth_manager.get_cached_token()['access_token']
tracks, ps = getTracksFromAllPlaylists(sp, token)
print(len(ps))
print(len(tracks))
# trs = tracks[:100]


start = datetime.datetime.now()
# result, gendict = getTrackGenreDictRequest(trs, token)
result, gendict = getTrackGenreDict(tracks, sp)
end = datetime.datetime.now()

result = getCount(result)
result = sortCount(result)
for r in result:
    print(r[0])
    print(r[1])

print(start)
print(end)
print(result)

'''


# token = auth_manager.get_cached_token()['access_token']


# g = getTrackGenreRequest(tracks[0], sp, token)
# print(g)
# artref = tracks[0]['artists'][0]['href']

# for t in tracks:
    # print(t['name'])
# for p in ps:
#     print(p['name'],end="->")
#     print(p['owner']['display_name'])
    # '''


