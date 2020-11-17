'''methods to extract data for tracks and genres'''

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import time 
import random

''' get avg track duration from FULL track object (from user saved and top playlist) '''
def getAverageTrackDuration(tracks):
    total = 0
    count = 0
    for track in tracks:
        duration = track['duration_ms']
        count += 1
        total += duration
    result = total / count
    return result

''' get explicit count from FULL track object (from user saved and top playlist) '''
def getExplicitCount(tracks):
    count = 0
    for track in tracks:
        if track['explicit'] is True:
            count += 1
    return count

''' duration ms format to minute and seconds format '''
def getTimeFromMs(ms):
    ms = int(ms)
    seconds, ms = divmod(ms,1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return "{}:{}".format(minutes, seconds)


''' get avg popularity from FULL track object (from user saved and top playlist) '''
def getAveragePopularity(tracks):
    total = 0
    count = 0
    for track in tracks:
        popularity = track['popularity']
        count += 1
        total += popularity
    result = total / count
    return result

def getTrackGenreFromAlbum(track, sp):
    album_id = track['album']['id']
    album = sp.album(album_id)
    genres = album['genres']
    return genres
 
def getTrackGenreFromArtist(track, sp):
    genres = set()
    artists = track['artists']
    for artist in artists:
        artist_id = artist['id']
        artist_object = sp.artist(artist_id)
        artist_genres = artist_object['genres']
        for genre in artist_genres:
            genres.add(genre)
    return genres

def getTrackGenre(track, sp):
    genres = getTrackGenreFromAlbum(track, sp)
    if not genres:
        print('yes')
        genres = getTrackGenreFromArtist(track, sp)
    return genres

''' misc, works for both tracks and genres'''
def getCount(genres):
    counts = {}
    for genre in genres:
        if genre in counts:
            counts[genre] += 1
        else:
            counts[genre] = 1
    return counts

def sortCount(count):      # returns list
    counts = sorted(count.items(), key=lambda x: x[1], reverse=True)
    return counts

def getUserSavedTracksID(sp):
    all_tracks = set()
    still_exists = True
    offset = 0
    while still_exists is True:
        saved_tracks = sp.current_user_saved_tracks(limit=50, offset =offset)
        track_items = saved_tracks['items']
        if track_items:
            for item in track_items:
                track = item['track']['id']
                all_tracks.add(track)
            offset += 50
        else:
            still_exists = False
    return all_tracks

def getUserSavedTracksList(sp):
    all_tracks = []
    still_exists = True
    offset = 0
    while still_exists is True:
        saved_tracks = sp.current_user_saved_tracks(limit=50, offset =offset)
        track_items = saved_tracks['items']
        if track_items:
            for item in track_items:
                track = item['track']
                all_tracks.append(track)
            offset += 50
        else:
            still_exists = False
    return all_tracks


def limitSavedTrakcs(tracks, limit):
    result = random.sample(tracks, limit)
    return result


def getUserTopTracksID(sp, time_range):
    all_tracks = []
    MAX_OFFSET = 50     # max offset is 49
    offset = 0
    while offset < MAX_OFFSET:
        top_tracks = sp.current_user_top_tracks(limit=50, offset=offset, time_range=time_range)
        track_items = top_tracks['items']
        for item in track_items:
            track = item['id']
            all_tracks.add(track)
        offset += 49
    return all_tracks


def getUserTopTracksList(sp, time_range):
    all_tracks = []
    MAX_OFFSET = 50     # max offset is 49
    offset = 0
    limit = 50
    while offset < MAX_OFFSET:
        top_tracks = sp.current_user_top_tracks(limit=limit, offset=offset, time_range=time_range)
        track_items = top_tracks['items']
        all_tracks.extend(track_items)
        offset += 49
        limit -= 1
    return all_tracks


''' get user's top artists in list format '''
def getUserTopArtistsList(sp, time_range):
    all_artists = []
    MAX_OFFSET = 50
    offset = 0
    limit = 50
    while offset < MAX_OFFSET:
        top_artists = sp.current_user_top_artists(limit=limit, offset=offset, time_range=time_range)
        artist_items = top_artists['items']
        all_artists.extend(artist_items)
        offset += 49
        limit -= 1
    return all_artists


''' get list of top genres based on artists '''
def getArtistGenresList(artists):
    all_genres = []
    for artist in artists:
        all_genres.extend(artist['genres'])
    return all_genres


'''  get dict (& list) with track uri as key and genres as value; used to create playlists  '''
def getTrackGenreDict(tracks, sp):
    all_genres = []
    result = {}
    for track in tracks:
        genres = getTrackGenreFromArtist(track, sp)
        result[track['uri']] = genres
        print(track['name'], end="  ")
        print(genres)
        all_genres.extend(genres)
    return result, all_genres



''' for artists '''
''' get dict (& list) with track uri as key and artist(s) as value; used to create playlists '''
def getTrackArtistDict(tracks):
    all_artists = []
    result= {}
    for track in tracks:
        artists = track['artists']
        to_add = []
        for artist in artists:
            artist_name = artist['name']
            to_add.append(artist_name)
        result[track['uri']] = to_add
        all_artists.extend(to_add)
    return result, all_artists


import requests

''' extract all data from playlists '''
# ''' only your owned playlists
def getTracksFromAllPlaylists(sp, token):

    max_limit = 50          # limit for both getting the playlists and getting the tracks in a playlist
    playlists = []
    all_reached = False

    while all_reached is False:
        plays = sp.current_user_playlists(limit=max_limit)
        items = plays['items']
        playlists.extend(items)
        if len(items) < max_limit:
            all_reached = True

    user_id = sp.current_user()['id']
    
    headers = {
        'Authorization': 'Bearer {token}'.format(token=token)
    }
    all_tracks = []
    owned_playlists = []

    for playlist in playlists:
        if playlist['owner']['id'] == user_id:
            # playlist = playlists[37]
            owned_playlists.append(playlist)
            tracks_url = playlist['tracks']['href']
            reached = False         # bool if all tracks in a playlist has been reached 
            offset = 0

            while reached is False:
                params = {
                    'limit': str(max_limit),
                    'offset': str(offset)
                }                        
                response = requests.get(tracks_url, headers=headers, params=params)
                content = response.json()
                items = content['items']
                for item in items:
                    all_tracks.append(item['track'])

                if len(items) < max_limit:
                    reached = True
                
                offset += max_limit

    return all_tracks, owned_playlists


''' doing it from requests instead of spotipy; slower, hence not used '''
def getTrackGenreRequest(track, access_token):
    headers = {
        'Authorization': 'Bearer {token}'.format(token=access_token)
    }
    genres = set()
    artists = track['artists']
    for artist in artists:
        response = requests.get(artist['href'], headers=headers)
        content = response.json()
        artist_genres = content['genres']
        genres.update(artist_genres)

    return genres

def getTrackGenreDictRequest(tracks, token):
    all_genres = []
    result = {}
    for track in tracks:
        genres = getTrackGenreRequest(track, token)
        result[track['uri']] = genres
        all_genres.extend(genres)
    return result, all_genres


