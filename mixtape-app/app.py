import streamlit as st
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random
import streamlit.components.v1 as components
import os
import base64

# --- 1. App Configuration ---
st.set_page_config(page_title="The Counter-Mixtape", page_icon="🌻")

# --- 2. Bulky High-Contrast Styling with Ultra-Glass Fix ---
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(img_file):
    bin_str = get_base64(img_file)
    page_bg_img = f'''
    <style>
    /* Main Background with Massive Red Border */
    .stApp {{
        background-image: url("data:image/jpeg;base64,{bin_str}");
        background-size: cover;
        background-attachment: fixed;
        border: 25px solid #8b0000; 
        box-sizing: border-box;
    }}
    
    /* THE ULTRA-GLASS CARD: Fixed for Safari and Chrome */
    .main .block-container {{
        background-color: rgba(255, 255, 255, 0.8) !important; 
        
        /* The Blur Magic - High Strength & Brightness for Readability */
        -webkit-backdrop-filter: blur(25px) brightness(1.1) !important;
        backdrop-filter: blur(25px) brightness(1.1) !important;
        
        padding: 60px;
        border-radius: 0px; 
        border: 10px solid #8b0000; 
        outline: 15px solid white; 
        margin-top: 60px;
        margin-bottom: 60px;
        box-shadow: 0px 20px 50px rgba(0,0,0,0.5);
    }}

    /* Big Bulky Red Typography */
    h1, h2, h3, p, span, label, .stMarkdown {{
        color: #8b0000 !important;
        font-family: 'Arial Black', Gadget, sans-serif !important;
        font-weight: 900 !important;
        text-transform: uppercase;
        letter-spacing: -1px;
        line-height: 1.2;
    }}

    /* MASSIVE RED BUTTON WITH GUARANTEED WHITE TEXT */
    div.stButton > button:first-child {{
        width: 100% !important;
        height: 85px !important;
        border: none !important;
        border-radius: 0px !important;
        background-color: #8b0000 !important; 
        color: #ffffff !important; 
        font-size: 26px !important;
        font-family: 'Arial Black', Gadget, sans-serif !important;
        font-weight: 900 !important;
        text-transform: uppercase !important;
        box-shadow: 6px 6px 0px #000000;
        transition: 0.2s ease;
    }}
    
    div.stButton > button:first-child p {{
        color: #ffffff !important; 
        font-size: 26px !important;
        font-weight: 900 !important;
    }}
    
    div.stButton > button:hover {{
        background-color: #ffffff !important;
        color: #8b0000 !important;
        border: 6px solid #8b0000 !important;
        transform: translate(-2px, -2px);
    }}

    div.stButton > button:hover p {{
        color: #8b0000 !important;
    }}

    /* Dropdown menu styling */
    div[data-baseweb="select"] {{
        border: 5px solid #8b0000 !important;
        background-color: white !important;
    }}
    
    div[data-baseweb="select"] div {{
        color: #8b0000 !important;
        font-weight: 900 !important;
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
    st.info("🌻 Loading lockdown mixtape vibes...")

# --- 3. Setup Spotify API ---
try:
    client_id = st.secrets["SPOTIPY_CLIENT_ID"]
    client_secret = st.secrets["SPOTIPY_CLIENT_SECRET"]
    auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(auth_manager=auth_manager)
except Exception:
    st.error("KEYS MISSING IN SECRETS")
    st.stop()

# --- 4. Load & Prepare Data ---
@st.cache_data
def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "polyjamorous.csv")
    return pd.read_csv(file_path)

df = load_data()
df['Display Name'] = df['Song'] + " by " + df['Artist']

# --- 5. The Interactive UI ---
st.title("THE COUNTER-MIXTAPE")
st.markdown("choose your jam and find out what i would recommend Hope this helps you got this Cuitie HAPPY lockdown!!")

st.write("") 

selected_song = st.selectbox("PICK A TRACK", df['Display Name'].tolist())

if st.button("GENERATE MY PERFECT MATCH"):
    song_data = df[df['Display Name'] == selected_song].iloc[0]
    
    with st.spinner("CRUNCHING DATA..."):
        try:
            # Algorithm Logic
            artist_name = song_data['Artist']
            search_results = sp.search(q=f"artist:{artist_name}", type='artist', limit=1)
            
            if search_results['artists']['items']:
                artist_id = search_results['artists']['items'][0]['id']
                related = sp.artist_related_artists(artist_id)
                
                if related['artists']:
                    match_artist = random.choice(related['artists'][:5])
                    top_tracks = sp.artist_top_tracks(match_artist['id'])
                    
                    original_ids = set(df['Spotify Track Id'].dropna().astype(str).tolist())
                    clean_ids = {str(uid).split('/')[-1].split('?')[0].split(':')[-1] for uid in original_ids}
                    
                    new_picks = [t for t in top_tracks['tracks'] if t['id'] not in clean_ids]
                    
                    if new_picks:
                        best_match = random.choice(new_picks[:3])
                        st.markdown("### MATCH FOUND")
                        
                        embed_url = f"https://open.spotify.com/embed/track/{best_match['id']}?utm_source=generator"
                        components.iframe(embed_url, width=300, height=152)
                        
                        with st.expander("VIEW LOG DATA"):
                            st.write(f"SEED: {selected_song}")
                            st.write(f"MATCH: {match_artist['name']}")
                    else:
                        st.error("NO NEW TRACKS")
                else:
                    st.error("NO RELATED VIBES")
            else:
                st.error("ARTIST NOT FOUND")
                
        except Exception as e:
            st.error(f"SYSTEM ERROR: {e}")

# --- Footer ---
st.markdown("<br><br><br>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center;'>HAND-CODED BY OWEN</h1>", unsafe_allow_html=True)
