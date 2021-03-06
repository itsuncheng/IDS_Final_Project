## File for data loading purposes
## Please load all of the required data files here
import streamlit as st
import numpy as np
import pandas as pd
import pickle

@st.cache(allow_output_mutation=True)
def load_genre_audio():

    global exploded_track_df
    df = pd.read_csv("data/filtered_track_df.csv")
    df["lyric_length"] = [len(item.split(" ")) for item in df.lyrics]
    df['genres'] = df.genres.apply(lambda x: [i[1:-1] for i in str(x)[1:-1].split(", ")])
    exploded_track_df = df.explode("genres")

    genres = ['dance pop', 'electronic', 'electropop', 'hip hop', 'jazz', 'k-pop', 'latin', 'pop', 'pop rap', 'r&b', 'rock']
    audio_feats = ['acousticness', 'danceability', 'duration_ms',
                    'energy', 'instrumentalness', 'liveness',
                    'loudness', 'speechiness', 'tempo', 'valence']

    global genres2audio
    genres2audio = {}
    for genre in genres:
        genres2audio[genre] = exploded_track_df[exploded_track_df["genres"]==genre][audio_feats].to_numpy()

@st.cache(allow_output_mutation=True)
def load_genre():
    global track_with_genre_df
    genres = ['dance pop', 'electronic', 'electropop', 'hip hop', 'jazz', 'k-pop', 'latin', 'pop', 'pop rap', 'r&b', 'rock']
    track_with_genre_df = exploded_track_df[exploded_track_df['genres'].isin(genres)]

@st.cache(allow_output_mutation=True)
def load_track_artist_album():
    global track_artist_album_df
    track_artist_album_df = pd.read_csv("data/trackArtistAlbum.csv")

def load_lyrics_data():
    global lyric_knn #the 10 nearest neighbor of each song using sentence embedding
    global cleaned_lyric #The lyrics of songs in each genre with stopwords removed, used for word clouds
    global lyric_sentiments # The sentiment distribution of each genre and 10 sentence examples for positive and negative each
    global song_sentiments # The sentiment score for each song's each sentence
    lyric_knn = pickle.load(open("data/lyrics_10nn.pkl",'rb'))
    cleaned_lyric = pickle.load(open("data/cleaned_lyrics.pkl",'rb'))
    lyric_sentiments = pickle.load(open("data/lyric_sentiments.pkl", 'rb'))
    song_sentiments = pickle.load(open("data/song_sentiments.pkl",'rb'))



@st.cache(allow_output_mutation=True)
def load_data():
    data_dir = "data/SpotGenTrack/Data Sources/"

    # global albums_data
    global artists_data
    # global tracks_data
    # albums_data = pd.read_csv(data_dir+"spotify_albums.csv")
    artists_data = pd.read_csv(data_dir+"spotify_artists.csv")
    # tracks_data = pd.read_csv(data_dir+"spotify_tracks.csv")

    load_genre_audio()
    load_track_artist_album()
    load_genre()
    load_lyrics_data()
