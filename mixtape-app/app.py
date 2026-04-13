import streamlit as st
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random
import streamlit.components.v1 as components
import os

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
                # (This also cleans the IDs so they match perfectly)
                original_playlist_ids = set(df['Spotify Track Id'].dropna().astype(str).tolist())
                clean_original_ids = {str(uid).split('/')[-1].split('?')[0].split(':')[-1] for uid in original_playlist_ids}
                
                valid_recommendations = [t for t in top_tracks['tracks'] if t['id'] not in clean_original_ids]
                
                if valid_recommendations:
                    best_match = random.choice(valid_recommendations[:5])
                    
                    st.success("Mathematical perfection achieved! Here is your counter-pick:")
                    
                    # --- The Playable Spotify Widget ---
                    new_track_id = best_match['id']
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
                
        except Exception:
            st.error("The Spotify API rejected our request. Try another song!")
