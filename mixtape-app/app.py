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
        border: 20px solid #8b0000; /* Thicker Dark Red Border */
        box-sizing: border-box;
    }}
    
    /* Heavy Cardstock Container */
    .main .block-container {{
        background-color: rgba(255, 255, 255, 0.95); /* Nearly solid white */
        padding: 50px;
        border-radius: 15px;
        border: 5px solid #8b0000;
        margin-top: 30px;
        margin-bottom: 30px;
        box-shadow: 0px 10px 30px rgba(0,0,0,0.5); /* Shadow to lift it off the drawing */
    }}

    /* Big Bold Dark Red Typography with White Glow */
    h1, h2, h3, p, span, label, .stMarkdown {{
        color: #8b0000 !important;
        font-family: 'Arial Black', Gadget, sans-serif !important;
        font-weight: 900 !important;
        text-transform: uppercase;
        text-shadow: 2px 2px 4px rgba(255, 255, 255, 1), -2px -2px 4px rgba(255, 255, 255, 1); /* White text glow */
    }}

    /* The Button: Dark Red with a White Outer Glow */
    .stButton>button {{
        width: 100%;
        border: 3px solid #ffffff; /* White border around the button */
        border-radius: 10px;
        background-color: #8b0000; 
        color: white !important;
        font-size: 22px !important;
        font-weight: 900 !important;
        padding: 20px;
        box-shadow: 0px 0px 15px rgba(255, 255, 255, 0.8); /* White glowing effect */
        transition: 0.3s;
    }}
    
    .stButton>button:hover {{
        background-color: #5f0000;
        box-shadow: 0px 0px 25px rgba(255, 255, 255, 1);
    }}

    /* Dropdown menu fix */
    div[data-baseweb="select"] {{
        border: 2px solid #8b0000 !important;
        background-color: white !important;
    }}
    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)

# Load background
try:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    bg_path = os.path.join(current_dir, "background.jpeg")
    set_background(bg_path)
except Exception:
    st.info("🌻 Loading...")

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

if st.button("GENERATE MY PERFECT MATCH"):
    song_data = df[df['Display Name'] == selected_song].iloc[0]
    
    with st.spinner("ANALYZING DATA..."):
        try:
            artist_name = song_data['Artist']
            artist_results = sp.search(q=f"artist:{artist_name}", type='artist', limit=1)
            
            if artist_results['artists']['items']:
                artist_id = artist_results['artists']['items'][0]['id']
                related = sp.artist_related_artists(artist_id)
                
                if related['artists']:
                    match_artist = random.choice(related['artists'][:5])
                    top_tracks = sp.artist_top_tracks(match_artist['id'])
                    
                    original_ids = set(df['Spotify Track Id'].dropna().astype(str).tolist())
                    clean_ids = {str(uid).split('/')[-1].split('?')[0].split(':')[-1] for uid in original_ids}
                    
                    new_picks = [t for t in top_tracks['tracks'] if t['id'] not in clean_ids]
                    
                    if new_picks:
                        best_match = random.choice(new_picks[:3])
                        st.success("MATCH FOUND")
                        
                        embed_url = f"https://open.spotify.com/embed/track/{best_match['id']}?utm_source=generator"
                        components.iframe(embed_url, width=300, height=152)
                        
                        with st.expander("VIEW NERD STATS"):
                            st.markdown(f"SEED: {selected_song}")
                            st.markdown(f"MATCH: {match_artist['name']}")
                    else:
                        st.error("NO NEW MATCHES")
                else:
                    st.error("NO RELATED VIBES")
            else:
                st.error("ARTIST NOT FOUND")
        except Exception as e:
            st.error(f"ERROR: {e}")
