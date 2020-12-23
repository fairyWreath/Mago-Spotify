''' module for flask sessin parsing methods '''

from flask import session
from app.citrus import nago, mei

''' for user tracks '''
def parseShortTopTracks(sp):
    tracks_list = nago.getUserTopTracksList(sp, 'short_term')
    session['short-top-tracks'] = tracks_list

def parseMediumTopTracks(sp):
    tracks_list = nago.getUserTopTracksList(sp, 'medium_term')
    session['medium-top-tracks'] = tracks_list

def parseLongTopTracks(sp):
    tracks_list = nago.getUserTopTracksList(sp, 'long_term')
    session['long-top-tracks'] = tracks_list

''' for user artists '''
def parseLongTopArtists(sp):
    artists_list = nago.getUserTopArtistsList(sp, 'long_term')
    session['long-top-artists'] = artists_list

def parseMediumTopArtists(sp):
    artists_list = nago.getUserTopArtistsList(sp,'medium_term')
    session['medium-top-artists'] = artists_list

def parseShortTopArtists(sp):
    artists_list = nago.getUserTopArtistsList(sp, 'short_term')
    session['short-top-artists'] = artists_list

''' for top genres  '''
''' saved library '''
def parseSavedLibraryTracks(sp):
    tracks_list = nago.getUserSavedTracksList(sp)
    session['saved-library-tracks'] = tracks_list

def parseTopGenresFromSavedLibrary(sp):
    tracks = session['saved-library-tracks']
    if session.get('saved-library-genres-all') is None:
        session['saved-library-track-genre-dict'], session['saved-library-genres-all'] = nago.getTrackGenreDict(tracks, sp)
    counts = nago.getCount(session['saved-library-genres-all'])
    sorted_counts = nago.sortCount(counts)
    session['top-genres-from-saved-library'] = sorted_counts


''' all playlists '''
def parseAllPlaylistTracks(sp, token):
    tracks_list = nago.getTracksFromAllPlaylists(sp, token)
    session['all-playlist-tracks'] = tracks_list

def parseTopGenresFromAllPlaylists(sp):
    tracks = session['all-playlist-tracks']
    session['all-playlist-track-genre-dict'], session['all-playlist-genres-all'] = nago.getTrackGenreDict(tracks, sp)
    counts = nago.getCount(session['all-playlist-genres-all'])
    sorted_counts = nago.sortCount(counts)
    session['top-genres-from-all-playlist'] = sorted_counts


''' genres from top tracks '''
def parseTopGenresFromLongTop(sp):
    tracks = session['long-top-tracks']
    session['long-top-track-genre-dict'], session['long-top-genres-all'] = nago.getTrackGenreDict(tracks, sp)
    counts = nago.getCount(session['long-top-genres-all'])
    sorted_count = nago.sortCount(counts)
    session['top-genres-from-long-top'] = sorted_count

def parseTopGenresFromMediumTop(sp):
    tracks = session['medium-top-tracks']
    session['medium-top-track-genre-dict'], session['medium-top-genres-all'] = nago.getTrackGenreDict(tracks, sp)
    counts = nago.getCount(session['medium-top-genres-all'])
    sorted_count = nago.sortCount(counts)
    session['top-genres-from-medium-top'] = sorted_count

def parseTopGenresFromShortTop(sp):
    tracks = session['short-top-tracks']
    session['short-top-track-genre-dict'], session['short-top-genres-all'] = nago.getTrackGenreDict(tracks, sp)
    counts = nago.getCount(session['short-top-genres-all'])
    sorted_count = nago.sortCount(counts)
    session['top-genres-from-short-top'] = sorted_count

''' genres from top artists '''
def parseTopGenresFromLongArtist(sp):
    artists = session['long-top-artists']
    session['long-artist-genres-all'] = nago.getArtistGenresList(artists)
    counts = nago.getCount(session['long-artist-genres-all'])
    sorted_count = nago.sortCount(counts)
    session['top-genres-from-long-artist'] = sorted_count

def parseTopGenresFromMediumArtist(sp):
    artists = session['medium-top-artists']
    session['medium-artist-genres-all'] = nago.getArtistGenresList(artists)
    counts = nago.getCount(session['medium-artist-genres-all'])
    sorted_count = nago.sortCount(counts)
    session['top-genres-from-medium-artist'] = sorted_count

def parseTopGenresFromShortArtist(sp):
    artists = session['short-top-artists']
    session['short-artist-genres-all'] = nago.getArtistGenresList(artists)
    counts = nago.getCount(session['short-artist-genres-all'])
    sorted_count = nago.sortCount(counts)
    session['top-genres-from-short-artist'] = sorted_count

''''''
''' for top artists '''
def parseShortTopArtistsName(sp):
    artists_list = nago.getUserTopArtistsNameList(sp, 'short_term')
    session['short-top-artists-name'] = artists_list

def parseMediumTopArtistsName(sp):
    artists_list = nago.getUserTopArtistsNameList(sp, 'medium_term')
    session['medium-top-artists-name'] = artists_list

def parseLongTopArtistsName(sp):
    artists_list = nago.getUserTopArtistsNameList(sp, 'long_term')
    session['long-top-artists-name'] = artists_list

def parseTopArtistsFromSavedLibrary(sp):
    tracks = session['saved-library-tracks']
    # tracks = nago.limitSavedTracks(tracks, 100)
    session['library-artists-track-artist-dict'], session['library-artists-all'] = nago.getTrackArtistDict(tracks)
    counts = nago.getCount(session['library-artists-all']) 
    session['top-artists-from-library'] = nago.sortCount(counts)


def parseTopArtistFromPlaylist(sp):
    tracks = session['all-playlist-tracks']
    # tracks = nago.limitSavedTracks(tracks, 100)
    session['playlist-artists-track-artist-dict'], session['playlist-artists-all'] = nago.getTrackArtistDict(tracks)
    counts = nago.getCount(session['playlist-artists-all']) 
    session['top-artists-from-playlist'] = nago.sortCount(counts)

def parseTopGenresFromCombined():
    counts = nago.getCount(session['combined-genres-all'])
    session['top-genres-from-combined'] = nago.sortCount(counts)

def parseTopArtistsFromCombined():
    counts = nago.getCount(session['combined-artists-all'])
    session['top-artists-from-combined'] = nago.sortCount(counts)

''' parse dicts to create playlists '''
def parseLibraryTrackGenreDict(sp):
    tracks = session['saved-library-tracks']
    session['saved-library-track-genre-dict'], session['saved-library-genres-all'] = nago.getTrackGenreDict(tracks, sp)

def parseLibraryTrackArtistDict():
    tracks = session['saved-library-tracks']
    session['library-artists-track-artist-dict'], session['library-artists-all'] = nago.getTrackArtistDict(tracks)

def parseCombinedTrackGenreDict(sp):
    tracks = session['combined-library-playlist-tracks']
    if session.get('saved-library-track-genre-dict') is not None:       # use help of saved-library dict if available
        session['combined-track-genre-dict'], session['combined-genres-all'] = nago.getTrackGenreDictWithOther(tracks, session['saved-library-track-genre-dict'], sp)
    else:    
        session['combined-track-genre-dict'], session['combined-genres-all'] = nago.getTrackGenreDict(tracks, sp)

def parseCombinedTrackArtistDict():
    tracks = session['combined-library-playlist-tracks']
    session['combined-track-artist-dict'], session['combined-artists-all'] = nago.getTrackArtistDict(tracks)


''' parse playlist+library tracks '''
def parseCombinedTracks(sp, token):
    if session.get('saved-library-tracks') is None:
        parseSavedLibraryTracks(sp)
    if session.get('all-playlist-tracks') is None:
        parseAllPlaylistTracks(sp, token)
    track_lists = [session['saved-library-tracks'], session['all-playlist-tracks']]
    session['combined-library-playlist-tracks'] = nago.combineTrackLists(track_lists)
 
def parseCombinedTrackGenreDictNew(sp, token):
    if session.get('saved-library-tracks') is None:
        parseSavedLibraryTracks(sp)
    if session.get('saved-library-track-genre-dict') is None:
        parseTopGenresFromSavedLibrary(sp)

    if session.get('all-playlist-tracks') is None:
        parseAllPlaylistTracks(sp, token)
    if session.get('all-playlist-track-genre-dict') is None:
        parseTopGenresFromAllPlaylists(sp)
    
    session['combined-track-genre-dict'] = {**session['saved-library-track-genre-dict'], **session['all-playlist-track-genre-dict']}
    

def parseCombinedTrackArtistDictNew(sp, token):
    if session.get('saved-library-tracks') is None:
        parseSavedLibraryTracks(sp)
    if session.get('library-artists-track-artist-dict') is None:
        parseTopArtistsFromSavedLibrary(sp)

    if session.get('all-playlist-tracks') is None:
        parseAllPlaylistTracks(sp, token)
    if session.get('playlist-artists-track-artist-dict') is None:
        parseTopArtistFromPlaylist(sp)

    session['combined-track-artist-dict'] = {**session['library-artists-track-artist-dict'], **session['playlist-artists-track-artist-dict']}


''' for user profile '''
def getTopFive(dict_items):
    dict_items = dict_items[:5]
    result = []
    for item in dict_items:
        result.append(item['name'])
    result_string = ", ".join(result)
    return result_string

# from artist genres
def getTopFiveGenres(counts):
    counts = counts[:5]
    result = []
    for count in counts:
        result.append(count[0])
    result_string = ", ".join(result)
    return result_string