# Mago - Spotify

Mago - A simple webapp to view, analyze and organize your spotify tracks and playlists

Deployed on Heroku -http://mago-spotify.herokuapp.com/

Features:
  - View your top tracks, artists and genres
  - Different methods exist to calculate your top tracks and artists:
    -> using Spotify's API
    -> based on your owned playlists combined
    -> based on your saved library
  - Top genres are gathered from your top tracks and genres, based on Spotify's own API and based on
    your library and playlists
  - Create playlists based on a single track or genre from your saved library and owned playlists. This can
    help you organize your library
  - Create playlists of recommendations based on given tracks, artists or genres, using Spotify's recommendation API. 
    You can choose to create unique recommendations(tracks that are not yet in your library or playlists)
  - For guitarists: you can create recommendations that has tabs available up on songsterr.com, using the songsterr API
  
Dependencies:
- flask
- flask-wtf
- flask-bootstrap
- flask-session
- spotipy

You also need a working spotify client id, client secret and redirect uri which you can get from the spotify dev website.
Place them inside app/client.py
