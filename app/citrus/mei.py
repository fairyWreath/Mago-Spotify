from . import songsterr
from . import static_items as static
import random
import requests

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

def getUniqueTrackRecommendationUris(artist_names, genre_names, track_names, all_tracks, amount, sp):

    artist_uris = []
    track_uris = []

    not_found_artists = []
    not_found_tracks = []
    ''' first check through saved/top tracks before accessing sp.search '''

    ''' loop through artist names '''
    for artist_name in artist_names:
        for track in all_tracks:
            artists = track['artists']
            found = False
            for artist in artists:
                if artist_name == artist['name']:
                    artist_uris.append(artist['uri'])
                    print(artist['name'])
                    found = True
                    break
            if found is True:
                break
        if found is False:
            not_found_artists.append(artist_name)
    
    ''' loop through track names '''
    for track_name in track_names:
        for track in all_tracks:
            found = False
            if track_name == track['name']:
                print(track['name'])
                track_uris.append(track['id'])
                found = True
                break
        if found is False:
            not_found_tracks.append(track_name)
    
    for artist_name in not_found_artists:
        name = replace_runs_of_whitespace(artist_name)
        searches = sp.search(q=name, type="artist")
        if len(searches['artists']['items']) > 0:
            artist_uris.append(searches['artists']['items'][0]['uri'])

    av_genres = getAvailableGenresOnly(genre_names)
    result_uris = set()

    max_limit = 100
    remaining = amount
    recommend = True 
    
    cycles = 0
    cycles_limit = 25

    while(recommend):
        cycles += 1
        limit = max_limit
        
        try:
            recs = sp.recommendations(seed_tracks=track_uris, seed_genres=av_genres ,seed_artists=artist_uris, limit=limit)
        except:
            return False
            break
        else:
            rec_tracks = recs['tracks']
            for track in rec_tracks:
                track_uri = track['uri']
                print(track['name'],end="->")
                print(track['artists'][0]['name'])

                unique = True
                for track_item in all_tracks:
                    if track_uri == track_item['uri']:
                        unique = False
                        break
                
                if unique is True:
                    result_uris.add(track_uri)
                    if len(result_uris) >= amount:
                        recommend = False
                        break
    
        if cycles >= cycles_limit:
            return False
            break
        print(len(result_uris))

    return result_uris

''' also unique '''
def getUniqueTabTrackRecommendationUris(artist_names, genre_names, track_names, all_tracks, amount, sp):

    artist_uris = []
    track_uris = []

    not_found_artists = []
    not_found_tracks = []
    ''' first check through saved/top tracks before accessing sp.search '''

    ''' loop through artist names '''
    for artist_name in artist_names:
        for track in all_tracks:
            artists = track['artists']
            found = False
            for artist in artists:
                if artist_name == artist['name']:
                    artist_uris.append(artist['uri'])
                    print(artist['name'])
                    found = True
                    break
            if found is True:
                break
        if found is False:
            not_found_artists.append(artist_name)
    
    ''' loop through track names '''
    for track_name in track_names:
        for track in all_tracks:
            found = False
            if track_name == track['name']:
                print(track['name'])
                track_uris.append(track['id'])
                found = True
                break
        if found is False:
            not_found_tracks.append(track_name)
    
    for artist_name in not_found_artists:
        name = replace_runs_of_whitespace(artist_name)
        searches = sp.search(q=name, type="artist")
        if len(searches['artists']['items']) > 0:
            artist_uris.append(searches['artists']['items'][0]['uri'])

    # for track_name in not_found_tracks:
    #     name = replace_runs_of_whitespace(track_name)
    #     searches = sp.search(q=name, type="track")
    #     if len(searches['tracks']['items']) > 0:
    #         track_uris.append(searches['tracks']['items'][0]['uri'])

    
    av_genres = getAvailableGenresOnly(genre_names)
    result_uris = set()
    tabs = {}

    max_limit = 100
    remaining = amount
    recommend = True 
    cycles = 0
    cycles_limit = 15
    
    while(recommend):
        cycles += 1
        limit = max_limit
        
        try:
            recs = sp.recommendations(seed_tracks=track_uris, seed_genres=av_genres ,seed_artists=artist_uris, limit=limit)
        except:
            return False, False
            break
        else:
            rec_tracks = recs['tracks']
            for track in rec_tracks:
                track_uri = track['uri']
                print(track['name'],end="->")
                print(track['artists'][0]['name'])

                unique = True
                for track_item in all_tracks:
                    if track_uri == track_item['uri']:
                        unique = False
                        print('not unique')
                        break
                
                if unique is True:
                    track_tablink = songsterr.searchForTabLink(track['artists'][0]['name'], track['name'])
                    print(track_tablink)
                    if track_tablink != False:
                        output_name = track['name'] + " - " + track['artists'][0]['name']
                        tabs[output_name] = track_tablink
                      
                        print(track_tablink)
                        result_uris.add(track_uri)

                    if len(result_uris) >= amount:
                        recommend = False
                        break
    
        if cycles >= cycles_limit:
            return False, False
        print(len(result_uris)) 
                
    return list(result_uris), tabs


''' not unique '''
def getTrackRecommendationUris(artist_names, genre_names, track_names, all_tracks, amount, sp):
    artist_uris = []
    track_uris = []
    not_found_artists = []
    not_found_tracks = []

    for artist_name in artist_names:
        for track in all_tracks:
            artists = track['artists']
            found = False
            for artist in artists:
                if artist_name == artist['name']:
                    artist_uris.append(artist['uri'])
                    print(artist['name'])
                    found = True
                    break
            if found is True:
                break
        if found is False:
            not_found_artists.append(artist_name)
    
    for track_name in track_names:
        for track in all_tracks:
            found = False
            if track_name == track['name']:
                print(track['name'])
                track_uris.append(track['id'])
                found = True
                break
        if found is False:
            not_found_tracks.append(track_name)
    
    for artist_name in not_found_artists:
        name = replace_runs_of_whitespace(artist_name)
        searches = sp.search(q=name, type="artist")
        if len(searches['artists']['items']) > 0:
            artist_uris.append(searches['artists']['items'][0]['uri'])


    av_genres = getAvailableGenresOnly(genre_names)
    result_uris = set()
    max_limit = 100
    remaining = amount
    recommend = True 
    
    while(recommend):
        limit = max_limit
        try:
            recs = sp.recommendations(seed_tracks=track_uris, seed_genres=av_genres ,seed_artists=artist_uris, limit=limit)
        except:
            return False
            break
        else:
            rec_tracks = recs['tracks']
            for track in rec_tracks:
                track_uri = track['uri']
                print(track['name'],end="->")
                print(track['artists'][0]['name'])
                result_uris.add(track_uri)
                if len(result_uris) >= amount:
                    recommend = False
                    break
        print(len(result_uris))
        
    return result_uris


def getTabTrackRecommendationUris(artist_names, genre_names, track_names, all_tracks, amount, sp):

    artist_uris = []
    track_uris = []

    not_found_artists = []
    not_found_tracks = []
    ''' first check through saved/top tracks before accessing sp.search '''

    ''' loop through artist names '''
    for artist_name in artist_names:
        for track in all_tracks:
            artists = track['artists']
            found = False
            for artist in artists:
                if artist_name == artist['name']:
                    artist_uris.append(artist['uri'])
                    print(artist['name'])
                    found = True
                    break
            if found is True:
                break
        if found is False:
            not_found_artists.append(artist_name)
    
    ''' loop through track names '''
    for track_name in track_names:
        for track in all_tracks:
            found = False
            if track_name == track['name']:
                print(track['name'])
                track_uris.append(track['id'])
                found = True
                break
        if found is False:
            not_found_tracks.append(track_name)
    
    for artist_name in not_found_artists:
        name = replace_runs_of_whitespace(artist_name)
        searches = sp.search(q=name, type="artist")
        if len(searches['artists']['items']) > 0:
            artist_uris.append(searches['artists']['items'][0]['uri'])

    # for track_name in not_found_tracks:
    #     name = replace_runs_of_whitespace(track_name)
    #     searches = sp.search(q=name, type="track")
    #     if len(searches['tracks']['items']) > 0:
    #         track_uris.append(searches['tracks']['items'][0]['uri'])

    
    av_genres = getAvailableGenresOnly(genre_names)
    result_uris = set()
    tabs = {}

    max_limit = 100
    remaining = amount
    recommend = True 
    
    while(recommend):
        limit = max_limit
        
        try:
            recs = sp.recommendations(seed_tracks=track_uris, seed_genres=av_genres ,seed_artists=artist_uris, limit=limit)
        except:
            return False, False
            break
        else:
            rec_tracks = recs['tracks']
            for track in rec_tracks:
                track_uri = track['uri']
                print(track['name'],end="->")
                print(track['artists'][0]['name'])

                track_tablink = songsterr.searchForTabLink(track['artists'][0]['name'], track['name'])
                print(track_tablink)
                if track_tablink != False:
                    output_name = track['name'] + " - " + track['artists'][0]['name']
                    tabs[output_name] = track_tablink
                    
                    print(track_tablink)
                    result_uris.add(track_uri)

                if len(result_uris) >= amount:
                    recommend = False
                    break
    
        print(len(result_uris)) 
                
    return list(result_uris), tabs