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

# --- 2. Professional Flat UI Styling ---
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(img_file):
    bin_str = get_base64(img_file)
    page_bg_img = f'''
    <style>
    /* Main Background with Dark Red Border */
    .stApp {{
        background-image: url("data:image/jpeg;base64,{bin_str}");
        background-size: cover;
        background-attachment: fixed;
        border: 12px solid #8b0000; 
        box-sizing: border-box;
    }}
    
    /* Solid White Professional Card */
    .main .block-container {{
        background-color: #ffffff; 
        padding: 60px;
        border-radius: 2px; 
        border-left: 10px solid #8b0000;
        margin-top: 40px;
        margin-bottom: 40px;
        box-shadow: 20px 20px 0px rgba(139, 0, 0, 0.2);
    }}

    /* Big Bold Typography */
    h1, h2, h3, p, span, label, .stMarkdown {{
        color: #8b0000 !important;
        font-family: 'Arial Black', Gadget, sans-serif !important;
        font-weight: 900 !important;
        text-transform: uppercase;
        letter-spacing: -1px;
    }}

    /* Solid Dark Red Button */
    .stButton>button {{
        width: 100%;
        border: none;
        border-radius: 0px;
        background-color: #8b0000; 
        color: white !important;
        font-size: 20px !important;
        font-weight: 900 !important;
        padding: 18px;
        transition: all 0.2s ease;
        text-transform: uppercase;
    }}
    
    .stButton>button:hover {{
        background-color: #4a0000;
        transform: translateY(-2px);
        box-shadow: 0px 5px 15px rgba(0,0,0,0.1);
    }}

    /* Selectbox Styling */
    div[data-baseweb="select"] {{
        border: 2px solid #8b0000 !important;
        border-radius: 0px !important;
    }}
    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)

# Load background image
try:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    bg_path = os.path.join(current_dir, "background.jpeg")
    set_background(bg_path)
except Exception:
    st.info("🌻 Sunflower background loading...")

# --- 3. Setup Spotify API ---
try:
    client_id = st.secrets["SPOTIPY_CLIENT_ID"]
    client_secret = st.secrets["SPOTIPY_CLIENT_SECRET"]
    auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(auth_manager=auth_manager)
except Exception:
    st.error("API keys missing in Streamlit Secrets.")
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
st.markdown("CHOOSE A TRACK FROM YOUR PLAYLIST. I'LL FIND THE MATHEMATICAL RESPONSE.")

st.markdown("### CHOOSE A TRACK")
selected_song = st.selectbox("", df['Display Name'].tolist(), label_visibility="collapsed")

if st.button("GENERATE MY PERFECT MATCH"):
    song_data = df[df['Display Name'] == selected_song].iloc[0]
    
    with st.spinner("ANALYZING MUSIC DNA..."):
        try:
            # Step 1: Find the artist
            artist_name = song_data['Artist']
            search_results = sp.search(q=f"artist:{artist_name}", type='artist', limit=1)
            
            if search_results['artists']['items']:
                artist_id = search_results['artists']['items'][0]['id']
                
                # Step 2: Get Related Artists
                related = sp.artist_related_artists(artist_id)
                
                if related['artists']:
                    match_artist = random.choice(related['artists'][:5])
                    top_tracks = sp.artist_top_tracks(match_artist['id'])
                    
                    # Step 3: Clean IDs and filter duplicates
                    original_ids = set(df['Spotify Track Id'].dropna().astype(str).tolist())
                    clean_ids = {str(uid).split('/')[-1].split('?')[0].split(':')[-1] for uid in original_ids}
                    
                    new_picks = [t for t in top_tracks['tracks'] if t['id'] not in clean_ids]
                    
                    if new_picks:
                        best_match = random.choice(new_picks[:3])
                        
                        st.success("MATCH FOUND")
                        
                        # --- Spotify Embedded Player ---
                        embed_url = f"https://open.spotify.com/embed/track/{best_match['id']}?utm_source=generator"
                        components.iframe(embed_url, width=300, height=152)
                        
                        # --- Nerd Stats ---
                        with st.expander("VIEW LOG DATA"):
                            st.markdown(f"SEED: {selected_song}")
                            st.markdown(f"VIBE MATCH: {match_artist['name']}")
                            st.markdown("STATUS: API HANDSHAKE SUCCESSFUL")
                    else:
                        st.error("NO NEW TRACKS FOUND")
                else:
                    st.error("NO RELATED VIBES FOUND")
            else:
                st.error("ARTIST NOT FOUND")
                
        except Exception as e:
            st.error(f"SYSTEM ERROR: {e}")

# --- Footer ---
st.markdown("---")
st.markdown("HAND-CODED WITH 🌻")
