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
    # This automatically finds the exact folder where app.py is located
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # This joins that folder path with the CSV name
    file_path = os.path.join(current_dir, "polyjamorous.csv")
    
    return pd.read_csv(file_path)
# --- The Interactive UI ---
st.write(df.columns)
st.markdown("### Step 1: Pick a track from your playlist")
selected_song = st.selectbox("Choose a song:", df['Display Name'].tolist())

if st.button("Generate My Perfect Match 🚀"):
    song_data = df[df['Display Name'] == selected_song].iloc[0]
    original_track_id = song_data['Spotify Track Id']

    # Extract the musical DNA safely
    try:
        target_energy = float(song_data['Energy']) / 100
        target_valence = float(song_data['Valence']) / 100
        target_dance = float(song_data['Dance']) / 100
    except Exception:  # Fixed E722: No bare excepts allowed
        target_energy, target_valence, target_dance = 0.5, 0.5, 0.5

    with st.spinner("Crunching the musical data..."):
        # Ask Spotify for recommendations
        results = sp.recommendations(
            seed_tracks=[original_track_id],
            target_energy=target_energy,
            target_valence=target_valence,
            target_danceability=target_dance,
            limit=20
        )

        # Filter out any songs already in her CSV
        original_playlist_ids = set(df['Spotify Track Id'].dropna().tolist())
        valid_recommendations = [t for t in results['tracks'] if t['id'] not in original_playlist_ids]

        if valid_recommendations:
            best_match = random.choice(valid_recommendations[:5])

            st.success("Mathematical perfection achieved! Here is your counter-pick:")

            # --- The Playable Spotify Widget ---
            new_track_id = best_match['id']
            embed_url = f"https://open.spotify.com/embed/track/{new_track_id}?utm_source=generator"

            # Inject the Spotify player into the website
            components.iframe(embed_url, width=300, height=152)

            # --- Nerd Stats ---
            with st.expander("🤓 View the Nerd Stats"):
                st.markdown(f"**Seed Track:** {selected_song}")
                st.markdown(f"**Target Energy:** {target_energy}")
                st.markdown(f"**Target Valence (Mood):** {target_valence}")
                st.markdown("Algorithm successfully bypassed previously known playlist vectors.")
        else:
            st.error("The algorithm was too strict! Try picking a different song.")
