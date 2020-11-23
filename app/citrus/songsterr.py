import requests

base_url = 'http://www.songsterr.com/a/ra/songs.json?pattern='
search_url = 'https://www.songsterr.com/?pattern='
song_url = 'http://www.songsterr.com/a/wa/song?id='
bestmatch_url = 'http://www.songsterr.com/a/wa/bestMatchForQueryString?s={song_title}&a={artist_name}'


def replace_runs_of_whitespace(words):
    return words.replace(' ','%20') 

def searchForSong(key_words):
    pattern = replace_runs_of_whitespace(key_words)
    url = base_url+pattern
    response = requests.get(url)
    content = response.json()
    
    if content:
        return search_url + pattern
    else:
        return False 

def searchForTabLink(artist, song):
    pattern = replace_runs_of_whitespace(artist + " " + song)
    url = base_url+pattern
    response = requests.get(url)
    content = response.json()

    if content:
        song_id = content[0]['id']      # get top most id
        return song_url + str(song_id)
    else:
        return False

def getBestMatchURL(artist, song):
    artist_pattern = replace_runs_of_whitespace(artist)
    song_pattern = replace_runs_of_whitespace(song)
    url = bestmatch_url.format(song_title=song_pattern, artist_name=artist_pattern)
    return url

