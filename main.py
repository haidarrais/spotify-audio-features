import streamlit as st
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json
import datetime

st.markdown("# Hi I'am Audio Features Extractor 🎈")

df = None

@st.cache_data
def convert_df(df, state):
    df = pd.DataFrame(state)
    return df.to_csv(index=False).encode('utf-8')

ts = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

def main():
    # Create input fields for the data you want to post to the API
    username = st.text_input("Username", value="simon.th7")
    pl_id = st.text_input("Playlist ID", value="5NH8uTSrEdvFg6zGyjfdUh")
    like = st.text_input("Like?", value="true")

    # Create a submit button
    if st.button("Submit", key="submitted"):
        credentials = json.load(open('credentials.json'))
        client_id = credentials['client_id']
        client_secret = credentials['client_secret']

        playlist_uri = "spotify:username" + username + "playlist:" + pl_id 
        like = like
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

        for track in playlist_tracks_data['items']:
            playlist_tracks_id.append(track['track']['id'])
            playlist_tracks_titles.append(track['track']['name'])
            # adds a list of all artists involved in the song to the list of artists for the playlist
            artist_list = []
            for artist in track['track']['artists']:
                artist_list.append(artist['name'])
            playlist_tracks_artists.append(artist_list)
            playlist_tracks_first_artists.append(artist_list[0])

        features = sp.audio_features(playlist_tracks_id)

        features_df = pd.DataFrame(data=features, columns=features[0].keys())

        features_df['title'] = playlist_tracks_titles
        features_df['first_artist'] = playlist_tracks_first_artists
        features_df['all_artists'] = playlist_tracks_artists
        #features_df = features_df.set_index('id')
        features_df = features_df[['id', 'title', 'first_artist', 'all_artists',
                                'danceability', 'energy', 'key', 'loudness',
                                'mode', 'acousticness', 'instrumentalness',
                                'liveness', 'valence', 'tempo',
                                'duration_ms', 'time_signature']]
        
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