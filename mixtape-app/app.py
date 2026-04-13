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

# --- 2. Premium Minimalist Styling ---
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(img_file):
    bin_str = get_base64(img_file)
    page_bg_img = f'''
    <style>
    /* Background with a subtle dark overlay to make the card pop */
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.15), rgba(0,0,0,0.15)), 
                    url("data:image/jpeg;base64,{bin_str}");
        background-size: cover;
        background-attachment: fixed;
    }}
    
    /* Elegant floating card */
    .main .block-container {{
        background-color: #ffffff; 
        padding: 50px 60px;
        border-radius: 8px; 
        border-top: 8px solid #8b0000; /* Subtle top accent instead of a full border */
        margin-top: 60px;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.2), 0 10px 10px -5px rgba(0, 0, 0, 0.1);
        max-width: 700px;
    }}

    /* Modern Clean Typography */
    h1 {{
        color: #1a1a1a !important;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif !important;
        font-weight: 800 !important;
        letter-spacing: -0.02em;
        margin-bottom: 0.5rem;
    }}
    
    p, span, label, .stMarkdown {{
        color: #444444 !important;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif !important;
        font-weight: 400 !important;
        line-height: 1.6;
    }}

    /* Bold Red Highlights */
    .highlight {{
        color: #8b0000;
        font-weight: 700;
    }}

    /* Designer Button - Solid Dark Red, No Glow */
    .stButton>button {{
        width: 100%;
        border: none;
        border-radius: 4px;
        background-color: #8b0000; 
        color: #ffffff !important;
        font-size: 16px !important;
        font-weight: 600 !important;
        padding: 14px;
        transition: background-color 0.2s ease;
        margin-top: 20px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }}
    
    .stButton>button:hover {{
        background-color: #5a0000;
        color: #ffffff !important;
    }}

    /* Custom Input Styling */
    div[data-baseweb="select"] {{
        border: 1px solid #e0e0e0 !important;
        border-radius: 4px !important;
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
    st.info("🌻 Finalizing UI...")

# --- 3. Setup Spotify API ---
try:
    client_id = st.secrets["SPOTIPY_CLIENT_ID"]
    client_secret = st.secrets["SPOTIPY_CLIENT_SECRET"]
    auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(auth_manager=auth_manager)
except Exception:
    st.error("Missing API Keys.")
    st.stop()

# --- 4. Load Data ---
@st.cache_data
def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "polyjamorous.csv")
    return pd.read_csv(file_path)

df = load_data()
df['Display Name'] = df['Song'] + " by " + df['Artist']

# --- 5. The UI ---
st.title("The Counter-Mixtape")
st.markdown("Choose a track from your playlist. I'll use the Spotify API to find a <span class='highlight'>mathematical response</span> with the same vibe.", unsafe_allow_html=True)

st.write("") # Spacer

selected_song = st.selectbox("CHOOSE A TRACK", df['Display Name'].tolist())

if st.button("Generate My Match"):
    song_data = df[df['Display Name'] == selected_song].iloc[0]
    
    with st.spinner("Analyzing music data..."):
        try:
            artist_name = song_data['Artist']
            search = sp.search(q=f"artist:{artist_name}", type='artist', limit=1)
            
            if search['artists']['items']:
                artist_id = search['artists']['items'][0]['id']
                related = sp.artist_related_artists(artist_id)
                
                if related['artists']:
                    match_artist = random.choice(related['artists'][:5])
                    top_tracks = sp.artist_top_tracks(match_artist['id'])
                    
                    original_ids = set(df['Spotify Track Id'].dropna().astype(str).tolist())
                    clean_ids = {str(uid).split('/')[-1].split('?')[0].split(':')[-1] for uid in original_ids}
                    
                    new_picks = [t for t in top_tracks['tracks'] if t['id'] not in clean_ids]
                    
                    if new_picks:
                        best_match = random.choice(new_picks[:3])
                        st.markdown("### <span class='highlight'>Perfect Match Found</span>", unsafe_allow_html=True)
                        
                        embed_url = f"https://open.spotify.com/embed/track/{best_match['id']}?utm_source=generator"
                        components.iframe(embed_url, width=300, height=152)
                        
                        with st.expander("Technical Log Data"):
                            st.markdown(f"**Seed:** {selected_song}")
                            st.markdown(f"**Vibe Match:** {match_artist['name']}")
                    else:
                        st.error("Try a different song.")
                else:
                    st.error("No related vibes found.")
            else:
                st.error("Artist not found.")
        except Exception as e:
            st.error(f"Error: {e}")

# --- Footer ---
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 12px; opacity: 0.6;'>HAND-CODED BY OWEN</p>", unsafe_allow_html=True)
