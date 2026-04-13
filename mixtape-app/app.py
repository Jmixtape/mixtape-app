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

# --- 2. Bulky High-Contrast Styling with Ultra-Glass & White Text ---
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(img_file):
    bin_str = get_base64(img_file)
    page_bg_img = f'''
    <style>
    /* Main Background with Massive White Border */
    .stApp {{
        background-image: url("data:image/jpeg;base64,{bin_str}");
        background-size: cover;
        background-attachment: fixed;
        border: 25px solid #ffffff; 
        box-sizing: border-box;
    }}
    
    /* THE ULTRA-GLASS CARD */
    .main .block-container {{
        background-color: rgba(255, 255, 255, 0.2) !important; 
        -webkit-backdrop-filter: blur(25px) brightness(1.1) !important;
        backdrop-filter: blur(25px) brightness(1.1) !important;
        
        padding: 60px;
        border-radius: 0px; 
        border: 10px solid #ffffff; 
        outline: 15px solid rgba(255, 255, 255, 0.5); 
        margin-top: 60px;
        margin-bottom: 60px;
        box-shadow: 0px 20px 50px rgba(0,0,0,0.5);
    }}

    /* Global Typography Base */
    h1, h2, h3, p, span, label, .stMarkdown {{
        font-family: 'Arial Black', Gadget, sans-serif !important;
        font-weight: 900 !important;
        text-transform: uppercase;
        letter-spacing: -1px;
        line-height: 1.2;
    }}

    /* Specific White Styling for Title and Subtitle */
    .white-text-title h1, .white-text-sub p {{
        color: #ffffff !important;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.8);
    }}

    /* White Styling for everything inside the card */
    .stMarkdown p, label, .stExpander p, .stMarkdown h3 {{
        color: #ffffff !important;
        text-shadow: 1px 1px 5px rgba(0,0,0,0.5);
    }}

    /* MASSIVE BUTTON - White with dark text for contrast */
    div.stButton > button:first-child {{
        width: 100% !important;
        height: 85px !important;
        border: none !important;
        border-radius: 0px !important;
        background-color: #ffffff !important; 
        color: #000000 !important; 
        font-size: 26px !important;
        font-family: 'Arial Black', Gadget, sans-serif !important;
        font-weight: 900 !important;
        text-transform: uppercase !important;
        box-shadow: 6px 6px 0px #000000;
    }}
    
    div.stButton > button:first-child p {{
        color: #000000 !important; 
        font-size: 26px !important;
        font-weight: 900 !important;
    }}
    
    div.stButton > button:hover {{
        background-color: #000000 !important;
        color: #ffffff !important;
        border: 6px solid #ffffff !important;
    }}

    div.stButton > button:hover p {{
        color: #ffffff !important;
    }}

    /* Dropdown menu styling */
    div[data-baseweb="select"] {{
        border: 5px solid #ffffff !important;
        background-color: white !important;
    }}

    /* CUSTOM WHITE FOOTER */
    .white-footer {{
        color: #ffffff !important;
        text-align: center;
        font-family: 'Arial Black', Gadget, sans-serif !important;
        font-weight: 900 !important;
        text-transform: uppercase;
        margin-top: 50px;
        font-size: 45px;
        text-shadow: 2px 2px 10px rgba(0,0,0,0.5);
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
    st.info("🌻 Finalizing UI...")

# --- 3. Setup Spotify API ---
try:
    client_id = st.secrets["SPOTIPY_CLIENT_ID"]
    client_secret = st.secrets["SPOTIPY_CLIENT_SECRET"]
    auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(auth_manager=auth_manager)
except Exception:
    st.error("KEYS MISSING")
    st.stop()

# --- 4. Load Data ---
@st.cache_data
def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "polyjamorous.csv")
    return pd.read_csv(file_path)

df = load_data()
df['Display Name'] = df['Song'] + " by " + df['Artist']

# --- 5. UI Layout ---
st.markdown('<div class="white-text-title"><h1>THE COUNTER-MIXTAPE</h1></div>', unsafe_allow_html=True)
st.markdown('<div class="white-text-sub"><p>choose your jam and find out what i would recommend Hope this helps you got this Cuitie HAPPY lockdown!!</p></div>', unsafe_allow_html=True)

st.write("") 

selected_song = st.selectbox("PICK A TRACK", df['Display Name'].tolist())

if st.button("GENERATE MY PERFECT MATCH"):
    song_data = df[df['Display Name'] == selected_song].iloc[0]
    
    with st.spinner("CRUNCHING DATA..."):
        try:
            # Clean the string but DROP the strict filter to avoid 400 errors
            search_query = str(song_data['Artist']).strip()
            
            # Execute the search as a broad query (exactly like typing it in the Spotify app)
            search_results = sp.search(q=search_query, type='track', limit=50, market='JO')
            
            if search_results['tracks']['items']:
                
                # 1. Grab all IDs currently in the CSV so we can EXCLUDE them
                original_ids = set(df['Spotify Track Id'].dropna().astype(str).tolist())
                clean_ids = {str(uid).split('/')[-1].split('?')[0].split(':')[-1] for uid in original_ids}
                
                # 2. Keep ONLY the tracks that are NOT already in the mixtape
                new_picks = [t for t in search_results['tracks']['items'] if t['id'] not in clean_ids]
                
                if new_picks:
                    # 3. Randomly pick ONE from the new discoveries
                    best_match = random.choice(new_picks)
                    st.markdown("### MATCH FOUND")
                    
                    embed_url = f"https://open.spotify.com/embed/track/{best_match['id']}?utm_source=generator"
                    components.iframe(embed_url, width=300, height=152)
                    
                    with st.expander("VIEW LOG DATA"):
                        st.write(f"SEED: {selected_song}")
                        st.write(f"NEW DISCOVERY: {best_match['name']} by {best_match['artists'][0]['name']}")
                else:
                    st.error("NO NEW TRACKS FOUND THAT AREN'T ALREADY IN THE MIXTAPE")
            else:
                st.error("ARTIST NOT FOUND ON SPOTIFY")
                
        except spotipy.exceptions.SpotifyException as e:
            st.error(f"SPOTIFY API ERROR: {e.http_status}. Search Query Failed: {search_query}")
        except Exception as e:
            st.error(f"ERROR: {e}")

# --- Footer in White ---
st.markdown("<br><br><br>", unsafe_allow_html=True)
st.markdown("<p class='white-footer'>HAND-CODED BY OWEN</p>", unsafe_allow_html=True)
