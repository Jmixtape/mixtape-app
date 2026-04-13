import streamlit as st
import pandas as pd
import random
import streamlit.components.v1 as components
import os
import base64
import requests

# --- 1. App Configuration ---
st.set_page_config(page_title="The Counter-Mixtape", page_icon="🌻", layout="centered")

# --- 2. Professional High-Contrast Styling with Ultra-Glass & White Text ---
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(img_file):
    bin_str = get_base64(img_file)
    page_bg_img = f'''
    <style>
    /* HIDE STREAMLIT'S TOP MENU AND HEADER ENTIRELY */
    header {{ visibility: hidden !important; display: none !important; }}
    #MainMenu {{ visibility: hidden !important; }}
    [data-testid="stToolbar"] {{ visibility: hidden !important; display: none !important; }}
    
    /* Main Background */
    .stApp {{
        background-image: url("data:image/jpeg;base64,{bin_str}");
        background-size: cover;
        background-attachment: fixed;
    }}
    
    /* THE FIX: Thinner Floating Frame Border */
    .stApp::after {{
        content: "";
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        border: 10px ridge #ffffff !important; 
        pointer-events: none; 
        z-index: 9999;
    }}
    
    /* THE RETRO CASSETTE CARD */
    .main .block-container {{
        background-color: rgba(30, 30, 30, 0.85) !important; 
        -webkit-backdrop-filter: blur(20px) !important;
        backdrop-filter: blur(20px) !important;
        
        padding: 50px 60px;
        border-radius: 30px; /* More rounded like a cassette */
        
        /* RETRO BORDERS: White Ridge + Dark Red Outline */
        border: 8px ridge #ffffff !important; 
        outline: 4px solid #8b0000 !important; 
        
        box-shadow: 0px 30px 60px rgba(0,0,0,0.9);
        margin-top: 60px; 
        margin-bottom: 60px;
        position: relative;
        overflow: hidden;
    }}

    /* Decorative Tape Reels (Visual Only) */
    .main .block-container::before, .main .block-container::after {{
        content: "";
        position: absolute;
        width: 120px;
        height: 120px;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.05);
        border: 2px dashed rgba(255, 255, 255, 0.1);
        z-index: -1;
    }}
    .main .block-container::before {{ top: 40%; left: 10%; }}
    .main .block-container::after {{ top: 40%; right: 10%; }}

    /* Global Typography Base - BOLD 3D Effects */
    .main .block-container h1, 
    .main .block-container h2, 
    .main .block-container h3, 
    .main .block-container p, 
    .main .block-container label, 
    .main .block-container span,
    .stMarkdown {{
        font-family: 'Arial Black', Gadget, sans-serif !important;
        font-weight: 900 !important;
        text-transform: uppercase;
        letter-spacing: -0.5px;
        line-height: 1.4;
        text-shadow: 2px 2px 0px #000000 !important; /* Sharp Retro Shadow */
        color: #ffffff !important;
    }}

    /* Black and White Title Styling */
    .white-text-title h1 {{
        font-size: 42px !important;
        text-align: center;
        margin-bottom: 25px;
        color: #ffffff !important;
        text-shadow: 4px 4px 0px #000000, 0 0 10px rgba(255,255,255,0.3) !important;
    }}
    
    /* Soft Glow Mixtape Emoji */
    .mixtape-emoji {{
        display: inline-block;
        filter: brightness(0) invert(1) drop-shadow(0 0 5px rgba(255, 255, 255, 0.6));
    }}
    
    /* Instructional Text Styling */
    .thick-white-text-sub p {{
        text-align: center;
        font-size: 18px !important; 
        background: #8b0000; /* Stamped Label Effect */
        padding: 5px 15px;
        display: inline-block;
        border-radius: 5px;
        margin-bottom: 20px;
    }}

    /* Personal Message Styling (Under Search) */
    .cutie-text p {{
        text-align: center;
        font-size: 16px !important;
        color: #ffffff !important;
        margin-top: 20px;
        letter-spacing: 1px;
    }}

    /* PREMIUM SEARCH BAR (Selectbox) */
    div[data-baseweb="select"] {{
        border: 4px ridge #ffffff !important;
        background-color: #f0f0f0 !important;
        border-radius: 0px !important; /* Blocky retro look */
    }}
    
    div[data-baseweb="select"] span {{
        color: #000000 !important;
        font-family: 'Arial Black', Gadget, sans-serif !important;
        text-shadow: none !important;
    }}

    /* BUTTON STYLING */
    div.stButton > button:first-child {{
        width: 100% !important;
        height: 70px !important;
        border: 4px ridge #ffffff !important;
        background-color: #ffffff !important; 
        color: #000000 !important; 
        font-size: 22px !important;
        box-shadow: 6px 6px 0px #000000;
        transition: 0.1s;
    }}
    
    div.stButton > button:active {{
        transform: translate(3px, 3px);
        box-shadow: 2px 2px 0px #000000;
    }}

    /* Expander */
    div[data-testid="stExpander"] {{
        border: 2px solid #ffffff !important;
        background-color: rgba(0, 0, 0, 0.5) !important; 
    }}

    /* FOOTER */
    .white-footer {{
        color: #ffffff !important;
        text-align: center;
        font-size: 18px;
        margin-top: 50px;
        opacity: 0.7;
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

# --- 3. Setup Direct Spotify API (Logic kept as is) ---
try:
    client_id = st.secrets["SPOTIPY_CLIENT_ID"]
    client_secret = st.secrets["SPOTIPY_CLIENT_SECRET"]
except Exception:
    st.error("KEYS MISSING")
    st.stop()

@st.cache_data(ttl=3000)
def get_spotify_token(cid, csec):
    auth_str = f"{cid}:{csec}"
    b64_auth_str = base64.b64encode(auth_str.encode()).decode()
    headers = { "Authorization": f"Basic {b64_auth_str}", "Content-Type": "application/x-www-form-urlencoded" }
    data = {"grant_type": "client_credentials"}
    response = requests.post("https://accounts.spotify.com/api/token", headers=headers, data=data)
    return response.json().get("access_token") if response.status_code == 200 else None

def search_spotify_tracks(token, query):
    headers = {"Authorization": f"Bearer {token}"}
    params = {"q": query, "type": "track"} 
    response = requests.get("https://api.spotify.com/v1/search", headers=headers, params=params)
    return response.json() if response.status_code == 200 else None

# --- 4. Load Data (Logic kept as is) ---
@st.cache_data
def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "polyjamorous.csv")
    return pd.read_csv(file_path)

df = load_data()
df['Display Name'] = df['Song'] + " by " + df['Artist']

# --- 5. UI Layout ---
# Black & White Title
st.markdown('<div class="white-text-title"><h1>THE COUNTER MIXTAPE <span class="mixtape-emoji">📼</span></h1></div>', unsafe_allow_html=True)

# Instruction Text (Top)
st.markdown('<div class="thick-white-text-sub"><p>choose your jam and find out what I would recommend</p></div>', unsafe_allow_html=True)

# Search Box
selected_song = st.selectbox("SEARCH OR PICK A TRACK", df['Display Name'].tolist())

# Personal Message (Under Search)
st.markdown('<div class="cutie-text"><p>Hope this is fun enough but not too distracting you got this Cutie !!!</p></div>', unsafe_allow_html=True)

st.write("")

if st.button("GENERATE MY PERFECT MATCH"):
    song_data = df[df['Display Name'] == selected_song].iloc[0]
    
    with st.spinner("CRUNCHING TAPE..."):
        token = get_spotify_token(client_id, client_secret)
        
        if not token:
            st.error("AUTH FAILED")
        else:
            search_query = str(song_data['Artist']).strip()
            search_results = search_spotify_tracks(token, search_query)
            
            if search_results and 'tracks' in search_results and search_results['tracks']['items']:
                original_ids = set(df['Spotify Track Id'].dropna().astype(str).tolist())
                clean_ids = {str(uid).split('/')[-1].split('?')[0].split(':')[-1] for uid in original_ids}
                original_names = set(df['Song'].dropna().str.lower().str.strip().tolist())
                
                new_picks = [t for t in search_results['tracks']['items'] if t['id'] not in clean_ids and t['name'].lower().strip() not in original_names]
                
                if new_picks:
                    best_match = random.choice(new_picks)
                    st.markdown("<h3 style='text-align: center; margin-bottom: 20px;'>owen would listen to this :)</h3>", unsafe_allow_html=True)
                    embed_url = f"https://open.spotify.com/embed/track/{best_match['id']}?utm_source=generator"
                    components.iframe(embed_url, width=300, height=152)
                    
                    with st.expander("VIEW LOG DATA"):
                        st.write(f"SEED: {selected_song}")
                        st.write(f"NEW: {best_match['name']}")
                else:
                    st.error("NO NEW TRACKS")

# Footer
st.markdown("<p class='white-footer'>HAND-CODED BY OWEN</p>", unsafe_allow_html=True)

# --- Sparkle Trail ---
sparkle_js = """
<script>
const parent = window.parent.document;
if (!parent.getElementById("sparkle-style")) {
    const style = parent.createElement("style");
    style.id = "sparkle-style";
    style.innerHTML = `.sparkle-trail { position: fixed; pointer-events: none; width: 10px; height: 10px; background: white; border-radius: 50%; z-index: 999999; animation: fall 0.8s forwards; } @keyframes fall { 0% { opacity: 1; transform: scale(1); } 100% { opacity: 0; transform: translateY(30px); } }`;
    parent.head.appendChild(style);
    parent.addEventListener("mousemove", (e) => {
        if (Math.random() > 0.6) return;
        const spark = parent.createElement("div");
        spark.className = "sparkle-trail";
        spark.style.left = e.clientX + "px"; spark.style.top = e.clientY + "px";
        parent.body.appendChild(spark);
        setTimeout(() => spark.remove(), 800);
    });
}
</script>
"""
components.html(sparkle_js, height=0, width=0)
