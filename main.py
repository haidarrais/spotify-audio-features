import streamlit as st
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json
import datetime
import requests

st.markdown("# Hi I'am Audio Features Extractor 🎈")

df = None

@st.cache_data
def convert_df(df, state):
    df = pd.DataFrame(state)
    return df.to_csv(index=False).encode('utf-8')

ts = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

def main():
    # Create input fields for the data you want to post to the API
    username = st.text_input("Username", value="21uigsizzf6xs2b3iphqnelci")
    pl_id = st.text_input("Playlist ID", value="1ERuHhasek7qD73MrWRrsx")

    url = "https://spotify-track-streams-playback-count1.p.rapidapi.com/tracks/spotify_track_streams"

    querystring = {"spotify_track_id":"6ho0GyrWZN3mhi9zVRW7xi","isrc":"CA5KR1821202"}

    headers = {
        "X-RapidAPI-Key": "136d06e556mshcf7fb4cd84c3cabp12318ajsn50ff895d015f",
        "X-RapidAPI-Host": "spotify-track-streams-playback-count1.p.rapidapi.com"
    }

    # Create a submit button
    if st.button("Submit", key="submitted"):
        credentials = json.load(open('credentials.json'))
        client_id = credentials['client_id']
        client_secret = credentials['client_secret']

        playlist_uri = "spotify:username" + username + "playlist:" + pl_id 
        client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

        uname= username
        playlist_id = pl_id

        results = sp.user_playlist(uname, playlist_id, 'tracks')

        playlist_tracks_data = results['tracks']
        playlist_tracks_id = []
        playlist_tracks_titles = []
        playlist_tracks_artists = []
        playlist_tracks_first_artists = []
        playlist_tracks_popularity = []
        playlist_tracks_playback_count = []

        for track in playlist_tracks_data['items']:
            playlist_tracks_id.append(track['track']['id'])
            playlist_tracks_titles.append(track['track']['name'])
            playlist_tracks_popularity.append(track['track']['popularity'])
            # adds a list of all artists involved in the song to the list of artists for the playlist
            artist_list = []
            for artist in track['track']['artists']:
                artist_list.append(artist['name'])
            playlist_tracks_artists.append(artist_list)
            playlist_tracks_first_artists.append(artist_list[0])
            querystring['spotify_track_id'] = track['track']['id']
            response = requests.get(url, headers=headers, params=querystring)
            playback = response.json()
            playlist_tracks_playback_count.append(playback['streams'])


        features = sp.audio_features(playlist_tracks_id)

        features_df = pd.DataFrame(data=features, columns=features[0].keys())

        features_df['title'] = playlist_tracks_titles
        features_df['first_artist'] = playlist_tracks_first_artists
        features_df['all_artists'] = playlist_tracks_artists
        features_df['popularity'] = playlist_tracks_popularity
        features_df['streams'] = playlist_tracks_playback_count
        #features_df = features_df.set_index('id')
        features_df = features_df[['id', 'title', 'first_artist', 'all_artists',
                                'danceability', 'energy', 'key', 'popularity', 'streams',
                                'loudness', 'mode', 'acousticness',
                                'instrumentalness', 'liveness', 'valence',
                                'tempo', 'duration_ms', 'time_signature']]
        
        st.dataframe(features_df)
        fdf = convert_df(df, features_df)
        st.download_button(
        "Download as CSV",
        fdf,
        f"{ts}.csv",
        "text/csv",
        key='download-csv-ci'
        )

if __name__ == "__main__":
    main()