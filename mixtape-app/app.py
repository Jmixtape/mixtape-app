import streamlit as st
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random
import streamlit.components.v1 as components
import os
import base64

# --- Custom Styling Logic ---
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = f'''
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{bin_str}");
        background-size: cover;
        background-attachment: fixed;
    }}
    
    /* Making the text more readable against the drawing */
    h1, h2, h3, p, span, label {{
        color: #3d2b1f !important; /* A dark sunflower-seed brown */
        font-family: 'Courier New', Courier, monospace; /* Geeky typewriter font */
        font-weight: bold;
    }}
    
    /* Styling the buttons to look more "hand-drawn" */
    .stButton>button {{
        border: 2px solid #3d2b1f;
        border-radius: 20px;
        background-color: #ffda03; /* Sunflower yellow */
        color: #3d2b1f;
    }}
    
    /* Make the selectbox container slightly transparent white */
    div[data-baseweb="select"] {{
        background-color: rgba(255, 255, 255, 0.7);
        border-radius: 10px;
    }}
    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)

# Run the background function
# Make sure "background.jpg" matches the name of your file on GitHub!
try:
    set_background('background.jpg')
except Exception:
    st.warning("Sunflower background not found. Upload 'background.jpg' to GitHub!")
# --- App Configuration ---
st.set_page_config(page_title="The Counter-Mixtape", page_icon="🎧")

st.title("🎧 The Perfect Counter-Mixtape")
st.markdown(
    "Pick a song from the playlist you sent me, and my algorithm will analyze "
    "its musical DNA to find you a brand new song with the exact same vibe!"
)

# --- Setup Spotify API ---
try:
    client_id = st.secrets["SPOTIPY_CLIENT_ID"]
    client_secret = st.secrets["SPOTIPY_CLIENT_SECRET"]
    auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(auth_manager=auth_manager)
except Exception:  # Fixed F841: Removed unused 'as e'
    st.error("Spotify API keys are missing! Check Streamlit Secrets.")
    st.stop()

# --- Load Her Playlist Data ---
@st.cache_data
def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "polyjamorous.csv")
    return pd.read_csv(file_path)

df = load_data()
df['Display Name'] = df['Song'] + " by " + df['Artist']

# --- The Interactive UI ---
st.markdown("### Step 1: Pick a track from your playlist")
selected_song = st.selectbox("Choose a song:", df['Display Name'].tolist())

if st.button("Generate My Perfect Match 🚀"):
    song_data = df[df['Display Name'] == selected_song].iloc[0]
    
    with st.spinner("Hacking the Spotify mainframe to find a match..."):
        try:
            # 1. Get the artist of the selected song
            artist_name = song_data['Artist']
            
            # 2. Search Spotify for that exact artist
            artist_results = sp.search(q=f"artist:{artist_name}", type='artist', limit=1)
            
            if not artist_results['artists']['items']:
                st.error(f"Couldn't find the artist {artist_name} on Spotify!")
                st.stop()
                
            artist_id = artist_results['artists']['items'][0]['id']
            
            # 3. Get 'Related Artists' (Bands with the exact same vibe)
            related_artists = sp.artist_related_artists(artist_id)
            
            if related_artists['artists']:
                # Pick a random related artist
                random_artist = random.choice(related_artists['artists'][:5])
                
                # 4. Get that related artist's Top Tracks
                top_tracks = sp.artist_top_tracks(random_artist['id'])
                
                # 5. Filter out any tracks already in her CSV
                original_playlist_ids = set(df['Spotify Track Id'].dropna().astype(str).tolist())
                clean_original_ids = {str(uid).split('/')[-1].split('?')[0].split(':')[-1] for uid in original_playlist_ids}
                
                valid_recommendations = [t for t in top_tracks['tracks'] if t['id'] not in clean_original_ids]
                
                if valid_recommendations:
                    best_match = random.choice(valid_recommendations[:5])
                    
                    st.success("Mathematical perfection achieved! Here is your counter-pick:")
                    
                    # --- The Playable Spotify Widget ---
                    new_track_id = best_match['id']
                    # FIXED: The actual official Spotify Embed URL structure
                    embed_url = f"https://open.spotify.com/embed/track/{new_track_id}?utm_source=generator"
                    components.iframe(embed_url, width=300, height=152)
                    
                    # --- Nerd Stats ---
                    with st.expander("🤓 View the Nerd Stats"):
                        st.markdown(f"**Seed Track:** {selected_song}")
                        st.markdown(f"**Target Vibe:** {random_artist['name']} (Matched to {artist_name})")
                        st.markdown("Algorithm successfully bypassed previously known playlist vectors.")
                else:
                    st.error("The algorithm was too strict! Try picking a different song.")
            else:
                st.error("This artist is too underground! No related bands found.")
                
        except Exception as e:
            # THIS IS THE X-RAY: It will print the exact error!
            st.error(f"CRASH REPORT: {e}")
                
        except Exception:
            st.error("The Spotify API rejected our request. Try another song!")
