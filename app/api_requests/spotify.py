'''methods to extract data for tracks and genres'''
import requests
import spotipy
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
        # for user defined local files, skip them as they have no artist id
        if artist['id'] is None:
            continue

        artist_id = artist['id']
        artist_object = sp.artist(artist_id)
        artist_genres = artist_object['genres']
        for genre in artist_genres:
            genres.add(genre)
    return genres

def getTrackGenre(track, sp):
    genres = getTrackGenreFromAlbum(track, sp)
    if not genres:
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


def limitSavedTracks(tracks, limit):
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

def getUserTopArtistsNameList(sp, time_range):
    all_artists = []
    MAX_OFFSET = 50
    offset = 0
    limit = 50
    while offset < MAX_OFFSET:
        top_artists = sp.current_user_top_artists(limit=limit, offset=offset, time_range=time_range)
        artist_items = top_artists['items']
        for item in artist_items:
            all_artists.append(item['name'])
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
        all_genres.extend(genres)
    return result, all_genres

''' get a genre dict, but first finds it in another dict, if not found then make an API call '''
def getTrackGenreDictWithOther(tracks, genre_dict, sp):
    all_genres = []
    result = {}
    for track in tracks:
        if track['uri'] in genre_dict:          #uri is the key
            result[track['uri']] = genre_dict[track['uri']]
            all_genres.extend(genre_dict[track['uri']])
        else:
            genres = getTrackGenreFromArtist(track, sp)
            result[track['uri']] = genres
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




''' extract all data from playlists '''
# ''' only your owned playlists
def getTracksFromAllPlaylists(sp, token):
    max_limit = 50          # limit for both getting the playlists and getting the tracks in a playlist
    playlist_offset = 0
    playlists = []
    all_reached = False

    while all_reached is False:
        plays = sp.current_user_playlists(limit=max_limit, offset=playlist_offset)
        items = plays['items']
        playlists.extend(items)
        if len(items) < max_limit:      #less than 50 means all playlists has been grabbed
            all_reached = True
        else:
            playlist_offset = playlist_offset + max_limit

    user_id = sp.current_user()['id']
    
    headers = {
        'Authorization': 'Bearer {token}'.format(token=token)
    }

    all_tracks_dict = {}                # temporary dict
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
                    if item['track']['id'] not in all_tracks_dict:
                        all_tracks_dict[item['track']['id']] = item['track']

                if len(items) < max_limit:
                    reached = True
                
                offset += max_limit

    all_tracks = list(all_tracks_dict.values())
    return all_tracks


''' gets a dict for playlist name and tracks url link(user owned playlist) '''
def getPlaylistTracksDict(sp, token):
    max_limit = 50          
    playlists = []
    all_reached = False

    while all_reached is False:
        plays = sp.current_user_playlists(limit=max_limit)
        items = plays['items']
        playlists.extend(items)
        if len(items) < max_limit:
            all_reached = True

    user_id = sp.current_user()['id']
    result = {}

    for playlist in playlists:
        if playlist['owner']['id'] == user_id:
            result[playlist['name']] = playlist['tracks']['href']
    
    return result

''' gets all tracks from a single playlist 'tracks' object '''
def getTracksFromPlaylist(url, token):
    reached = False         
    max_limit = 50
    offset = 0
    all_tracks = []

    headers = {
        'Authorization': 'Bearer {token}'.format(token=token)
    }

    while reached is False:
        params = {
            'limit': str(max_limit),
            'offset': str(offset)
        }                        
        response = requests.get(url, headers=headers, params=params)
        content = response.json()
        items = content['items']
        for item in items:
            all_tracks.append(item['track'])

        if len(items) < max_limit:
            reached = True
        
        offset += max_limit
    
    return all_tracks

def combineTrackLists(track_lists):
    result_dict = {}
    for track_list in track_lists:
        for track in track_list:
            if track['id'] not in result_dict:
                result_dict[track['id']] = track

    result = list(result_dict.values())
    return result


''' methods for recommendations and updating the user's library and playlists '''

''' create's a playlist from user's saved library based on a given genre keyword 
    parameters - (trackgenre dict, dictkeyword)
    return - uri list '''
def getUrisFromSaved(track_dict, keyword):
    uris = []
    for uri in track_dict:               
        keywords = track_dict[uri]
        if keyword in keywords:
            uris.append(uri)
    return uris


''' creates playlist from a list of uris '''   
def createPlaylistFromUris(uris, sp, play_name):
   
    playlist_name = play_name
    user_id = sp.current_user()['id']
    playlist_id = sp.user_playlist_create(user_id, playlist_name)['id']

    num_of_tracks = len(uris)
    max_num = 100              
    remaining = len(uris)

    start_index = 0
    end_index = 100

    while(remaining > 100):
        sp.user_playlist_add_tracks(user_id, playlist_id, uris[start_index:end_index])
        remaining -= max_num
        start_index += max_num
        end_index += max_num
    sp.user_playlist_add_tracks(user_id, playlist_id, uris[start_index:end_index])
    
    return playlist_id


''' misc ''' 
def replace_runs_of_whitespace_with_hyphen(words):
    return words.replace(' ','-') 

''' RECOMMENDATIONS '''

''' filter user requested genres, limitting to max 5 only '''
def getAvailableGenresOnly(genres):
    result = set()
    for genre in genres:
        genre = genre.lower()           # lowercase string
        if genre in static.AVAILABLE_GENRES_LIST:
            result.add(genre)
        genre = replace_runs_of_whitespace_with_hyphen(genre)   
        if genre in static.AVAILABLE_GENRES_LIST:
            result.add(genre)
    if len(result) > 5:
        result = random.sample(result, 5)
    return result


''' get recommendations based on genres(all, not only from seeds), artists and tracks 
    user inputs artist/track names as keywords
'''

def replace_runs_of_whitespace(words):
    return words.replace(' ','+') 

''' search artist uris from a given track list '''
def searchArtistUrisFromList(artist_names, all_tracks):
    artist_uris = []
    not_found_artists = []

    for artist_name in artist_names:
        found = False
        for track in all_tracks:
            for artist in track['artists']:
                if artist_name == artist['name']:
                     artist_uris.append(artist['uri'])
                     found = True
                     break
            if found is True:
                break
        if found is False:
            not_found_artists.append(artist_name)
    
    return artist_uris, not_found_artists

''' search track uris from a given track list '''
def searchTrackUrisFromList(track_names, all_tracks):
    track_uris = []
    not_found_tracks = []

    for track_name in track_names:
        found = False
        for track in all_tracks:
            if track_name == track['name']:
                track_uris.append(track['id'])
                found = True
                break
        if found is False:
            not_found_tracks.append(track_name)

    return track_uris, not_found_tracks

''' search for artists using the api'''
def searchArtistUris(artist_names, sp):
    artist_uris = []
    for artist_name in artist_names:
        name = replace_runs_of_whitespace(artist_name)
        if name == '':              # handle .split ''
            continue
        searches = sp.search(q=name, type="artist")
        if len(searches['artists']['items']) > 0:
            artist_uris.append(searches['artists']['items'][0]['uri'])
    return artist_uris

''' search for tracks using the api '''
def searchTrackUris(track_names, sp):
    track_uris = []
    for track_name in track_names:
        name = replace_runs_of_whitespace(track_name)
        if name == '':              # handle .split ''
            continue
        searches = sp.search(q=name, type="track")
        if len(searches['tracks']['items']) > 0:
            track_uris.append(searches['tracks']['items'][0]['uri'])
    return track_uris

def checkUniqueFromList(track_uri, all_tracks):
    for track_item in all_tracks:
        if track_uri == track_item['uri']:
            return False
    return True

def getRecommendationUris(artist_names, genre_names, track_names, all_tracks, amount, sp, unique_state=False, tab_state=False):
    artist_uris = []
    track_uris = []
    not_found_artists = []
    not_found_tracks = []

    artist_uris, not_found_artists = searchArtistUrisFromList(artist_names, all_tracks)
    track_uris, not_found_tracks = searchTrackUrisFromList(track_names, all_tracks)

    if len(not_found_artists) > 0:
        artist_uris = artist_uris + searchArtistUris(artist_names, sp)
    
    if len(not_found_tracks) > 0:
        tracks_uris = track_uris + searchTrackUris(track_names, sp)

    av_genres = getAvailableGenresOnly(genre_names)
    result_uris = set()
    tabs = {}

    max_limit = 100
    remaining = amount
    recommend = True 
    
    cycles = 0
    cycles_limit = 25

    while(recommend):
        cycles += 1    
        try:
            recs = sp.recommendations(seed_tracks=track_uris, seed_genres=av_genres ,seed_artists=artist_uris, limit=max_limit)
        except:
            return False
        
        rec_tracks = recs['tracks']
        for track in rec_tracks:
            track_uri = track['uri']
            if tab_state is True:
                track_tablink = songsterr.searchForTabLink(track['artists'][0]['name'], track['name'])
                if track_tablink != False:
                    output_name = track['name'] + " - " + track['artists'][0]['name']
                    tabs[output_name] = track_tablink
                else:
                    continue        # skip adding if tab could not be found

            if unique_state is True:
                unique = checkUniqueFromList(track_uri, all_tracks)
                if unique is True:
                    result_uris.add(track_uri)
            else:
                result_uris.add(track_uri)

            if len(result_uris) >= amount:
                recommend = False
                break

        if cycles >= cycles_limit:
            return False
            break

    if not tab_state:
        return result_uris
    else:
        return list(result_uris), tabs



