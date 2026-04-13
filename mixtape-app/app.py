import streamlit as st
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random
import streamlit.components.v1 as components
import os
import base64

# --- App Configuration ---
st.set_page_config(page_title="The Counter-Mixtape", page_icon="🌻")

# --- Custom Styling Logic ---
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(img_file):
    bin_str = get_base64(img_file)
    page_bg_img = f'''
    <style>
    /* Main Background */
    .stApp {{
        background-image: url("data:image/jpeg;base64,{bin_str}");
        background-size: cover;
        background-attachment: fixed;
        border: 15px solid #8b0000; /* Dark Red Border around the whole page */
        box-sizing: border-box;
    }}
    
    /* Creating a heavy frosted glass container */
    .main .block-container {{
        background-color: rgba(255, 255, 255, 0.85); /* Whiter background for readability */
        padding: 50px;
        border-radius: 20px;
        border: 4px solid #8b0000;
        margin-top: 30px;
        margin-bottom: 30px;
    }}

    /* Big Bold Typography */
    h1, h2, h3, p, span, label, .stMarkdown {{
        color: #8b0000 !important; /* Consistent Dark Red Text */
        font-family: 'Arial Black', Gadget, sans-serif !important; /* Big Bold Font */
        font-weight: 900 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }}

    /* Dark Red Button Styling */
    .stButton>button {{
        width: 100%;
        border: None;
        border-radius: 5px;
        background-color: #8b0000; /* Dark Red Box */
        color: white !important; /* White text for contrast */
        font-size: 20px !important;
        font-weight: bold;
        padding: 15px;
        transition: 0.3s;
    }}
    
    .stButton>button:hover {{
        background-color: #5f0000;
        color: #ffffff !important;
    }}

    /* Selectbox Text Fix */
    div[data-baseweb="select"] div {{
        color: #8b0000 !important;
        font-weight: bold !important;
    }}
    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)

# Try to load the background
try:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    bg_path = os.path.join(current_dir, "background.jpeg")
    set_background(bg_path)
except Exception:
    st.info("🌻 Loading background...")

# --- Setup Spotify API ---
try:
    client_id = st.secrets["SPOTIPY_CLIENT_ID"]
    client_secret = st.secrets["SPOTIPY_CLIENT_SECRET"]
    auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(auth_manager=auth_manager)
except Exception:
    st.error("API keys missing.")
    st.stop()

# --- Load Data ---
@st.cache_data
def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "polyjamorous.csv")
    return pd.read_csv(file_path)

df = load_data()
df['Display Name'] = df['Song'] + " by " + df['Artist']

# --- UI ---
st.title("THE COUNTER-MIXTAPE")
st.markdown("CHOOSE A SONG FROM YOUR PLAYLIST. THE ALGORITHM WILL FIND THE PERFECT RESPONSE.")

st.markdown("### CHOOSE A TRACK")
selected_song = st.selectbox("", df['Display Name'].tolist(), label_visibility="collapsed")

# Removed the rocket emoji from the button text
if st.button("GENERATE MY PERFECT MATCH"):
    song_data = df[df['Display Name'] == selected_song].iloc[0]
    
    with st.spinner("ANALYZING DATA..."):
        try:
            artist_name = song_data['Artist']
            artist_results = sp.search(q=f"artist:{artist_name}", type='artist', limit=1)
            
            if not artist_results['artists']['items']:
                st.error("ARTIST NOT FOUND")
                st.stop()
                
            artist_id = artist_results['artists']['items'][0]['id']
            related_artists = sp.artist_related_artists(artist_id)
            
            if related_artists['artists']:
                random_artist = random.choice(related_artists['artists'][:5])
                top_tracks = sp.artist_top_tracks(random_artist['id'])
                
                original_playlist_ids = set(df['Spotify Track Id'].dropna().astype(str).tolist())
                clean_original_ids = {str(uid).split('/')[-1].split('?')[0].split(':')[-1] for uid in original_playlist_ids}
                
                valid_recommendations = [t for t in top_tracks['tracks'] if t['id'] not in clean_original_ids]
                
                if valid_recommendations:
                    best_match = random.choice(valid_recommendations[:5])
                    st.success("MATCH FOUND")
                    
                    new_track_id = best_match['id']
                    embed_url = f"https://open.spotify.com/embed/track/{new_track_id}?utm_source=generator"
                    components.iframe(embed_url, width=300, height=152)
                    
                    with st.expander("VIEW NERD STATS"):
                        st.markdown(f"SEED: {selected_song}")
                        st.markdown(f"MATCHED VIBE: {random_artist['name']}")
                else:
                    st.error("TRY A DIFFERENT SONG")
            else:
                st.error("NO RELATED VIBES FOUND")
                
        except Exception as e:
            st.error(f"ERROR: {e}")
