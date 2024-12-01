
import streamlit as st
import pandas as pd
import pickle
import requests

# Spotify API credentials
client_id = "c578f022bd454623ada8953a4c75184b"
client_secret = "4a9b8a8bfb3540f79f5ae5c6a0b151e5"


def get_spotify_token(client_id, client_secret):
    auth_url = "https://accounts.spotify.com/api/token"
    auth_response = requests.post(auth_url, {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
    })
    auth_data = auth_response.json()
    return auth_data['access_token']


def fetch_song_details(song_name, access_token):
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    search_url = f"https://api.spotify.com/v1/search?q={song_name}&type=track&limit=1"
    response = requests.get(search_url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        tracks = data.get('tracks', {}).get('items', [])
        if tracks:
            track = tracks[0]
            album_image = track['album']['images'][0]['url']  # Get the album image URL
            return album_image
    return none  # Placeholder image if not found

def recommended(musics):
    try:
        if musics not in music['title'].values:
            print(f"'{musics}' not found in dataset.")
            return [], []
        
        music_index = int(music[music['title'] == musics].index[0])
        
        distances = similarity[music_index]
        
        music_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
        
        recommended_music = []
        recommended_posters = []
        
        
        access_token = get_spotify_token(client_id, client_secret)
        
        for i in music_list:
            music_title = music.iloc[i[0]].title
            recommended_music.append(music_title)
            recommended_posters.append(fetch_song_details(music_title, access_token))
        
        return recommended_music, recommended_posters
    except Exception as e:
        print(f"Error in recommendation: {e}")
        return [], []

music_dict = pickle.load(open('musicrec.pkl', 'rb'))
music = pd.DataFrame(music_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title("Music Recommendation System")

selected_music_name = st.selectbox("Select a music you like", music['title'].values)

if st.button('Recommend'):
    names, posters = recommended(selected_music_name)
    
    cols = st.columns(5)
    for idx, col in enumerate(cols):
        if idx < len(names):
            with col:
                st.image(posters[idx], use_container_width=True)  # Updated parameter
                st.text(names[idx])
