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
    
    /* Main Background & Centering */
    .stApp {{
        background-image: url("data:image/jpeg;base64,{bin_str}");
        background-size: cover;
        background-attachment: fixed;
        display: flex;
        justify-content: center;
        align-items: center;
    }}
    
    /* THE FIX: Floating Frame Border - Pure White Ridge */
    .stApp::after {{
        content: "";
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        border: 20px ridge #ffffff !important; 
        pointer-events: none; 
        z-index: 9999;
    }}
    
    /* THE PREMIUM ULTRA-GLASS CARD - CENTERED & RESPONSIVE */
    .main .block-container {{
        background-color: rgba(255, 255, 255, 0.15) !important; 
        -webkit-backdrop-filter: blur(30px) brightness(1.1) !important;
        backdrop-filter: blur(30px) brightness(1.1) !important;
        
        padding: 50px 60px;
        border-radius: 12px; 
        border: 14px ridge #ffffff !important; 
        outline: 6px solid #8b0000 !important; 
        
        box-shadow: 0px 25px 50px rgba(0,0,0,0.8);
        margin: auto !important; /* Perfect Center */
        max-width: 800px !important;
        text-align: center;
    }}

    /* Global Typography Base */
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
        text-shadow: 2px 2px 0px #8b0000, 4px 4px 8px rgba(0,0,0,0.7) !important;
        color: #ffffff !important;
    }}

    /* Black and White Title Styling */
    .white-text-title h1 {{
        font-size: 46px !important;
        text-shadow: 3px 3px 0px #000000, 6px 6px 15px rgba(0,0,0,0.8) !important;
    }}
    
    .mixtape-emoji {{
        display: inline-block;
        filter: brightness(0) invert(1);
        filter: drop-shadow(0 0 5px rgba(255, 255, 255, 0.6));
    }}
    
    .thick-white-text-sub p {{
        font-size: 20px !important; 
        text-shadow: 2px 2px 0px #8b0000, 4px 4px 8px rgba(0,0,0,0.8) !important;
    }}

    div[data-baseweb="select"] {{
        border: 6px ridge #ffffff !important;
        background-color: #ffffff !important;
    }}
    
    div[data-baseweb="select"] span {{
        color: #8b0000 !important;
        text-shadow: none !important;
    }}

    /* REACTIVE BUTTON STYLING */
    div.stButton > button:first-child {{
        width: 100% !important;
        height: 75px !important;
        border: 6px ridge #ffffff !important;
        border-radius: 4px !important;
        background-color: #ffffff !important; 
        color: #8b0000 !important; 
        font-size: 24px !important;
        box-shadow: 0px 8px 15px rgba(0,0,0,0.6);
        transition: all 0.1s ease-in-out !important; /* Fast transition for reaction */
    }}
    
    div.stButton > button:hover {{
        background-color: #ffffff !important;
        filter: brightness(1.1);
        transform: translateY(-2px);
    }}

    /* Button Pressing Animation */
    div.stButton > button:active {{
        transform: translateY(4px) scale(0.98) !important;
        box-shadow: 0px 2px 5px rgba(0,0,0,0.8) !important;
    }}
    
    div.stButton > button p {{
        color: #8b0000 !important;
        text-shadow: none !important;
    }}

    /* Spotify Iframe - Forces large scale */
    iframe {{
        border-radius: 12px;
        width: 100% !important;
        min-height: 200px !important; /* Longer/Larger player */
    }}

    div[data-testid="stExpander"] {{
        border: 4px solid #ffffff !important;
        background-color: rgba(139, 0, 0, 0.4) !important; 
    }}

    .white-footer {{
        color: #ffffff !important;
        text-align: center;
        margin-top: 40px;
        font-size: 22px;
        text-shadow: 2px 2px 0px #8b0000, 4px 4px 10px rgba(0,0,0,0.8) !important;
    }}
    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)

try:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    bg_path = os.path.join(current_dir, "background.jpeg")
    set_background(bg_path)
except Exception:
    st.info("🌻 Finalizing Centered Layout...")

# --- 3. Setup Direct Spotify API ---
try:
    client_id = st.secrets["SPOTIPY_CLIENT_ID"]
    client_secret = st.secrets["SPOTIPY_CLIENT_SECRET"]
except Exception:
    st.error("KEYS MISSING.")
    st.stop()

@st.cache_data(ttl=3000)
def get_spotify_token(cid, csec):
    auth_str = f"{cid}:{csec}"
    b64_auth_str = base64.b64encode(auth_str.encode()).decode()
    headers = {"Authorization": f"Basic {b64_auth_str}", "Content-Type": "application/x-www-form-urlencoded"}
    data = {"grant_type": "client_credentials"}
    response = requests.post("https://accounts.spotify.com/api/token", headers=headers, data=data)
    return response.json().get("access_token") if response.status_code == 200 else None

def search_spotify_tracks(token, query):
    headers = {"Authorization": f"Bearer {token}"}
    params = {"q": query, "type": "track"} 
    response = requests.get("https://api.spotify.com/v1/search", headers=headers, params=params)
    return response.json() if response.status_code == 200 else None

# --- 4. Load Data ---
@st.cache_data
def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "polyjamorous.csv")
    return pd.read_csv(file_path)

df = load_data()
df['Display Name'] = df['Song'] + " by " + df['Artist']

# --- 5. UI Layout ---
st.markdown('<div class="white-text-title"><h1>THE COUNTER MIXTAPE <span class="mixtape-emoji">📼</span></h1></div>', unsafe_allow_html=True)

st.markdown('<div class="thick-white-text-sub"><p style="margin-bottom: 5px;">choose your jam and find out what I would recommend</p></div>', unsafe_allow_html=True)

selected_song = st.selectbox("SEARCH OR PICK A TRACK", df['Display Name'].tolist())

st.markdown('<div class="thick-white-text-sub"><p style="margin-top: 15px; margin-bottom: 25px;">Hope this is fun enough but not too distracting you got this Cutie !!!</p></div>', unsafe_allow_html=True)

if st.button("GENERATE MY PERFECT MATCH"):
    song_data = df[df['Display Name'] == selected_song].iloc[0]
    
    with st.spinner("CRUNCHING DATA..."):
        token = get_spotify_token(client_id, client_secret)
        if token:
            search_query = str(song_data['Artist']).strip()
            search_results = search_spotify_tracks(token, search_query)
            
            if search_results and 'tracks' in search_results and search_results['tracks']['items']:
                original_ids = set(df['Spotify Track Id'].dropna().astype(str).tolist())
                clean_ids = {str(uid).split('/')[-1].split('?')[0].split(':')[-1] for uid in original_ids}
                original_names = set(df['Song'].dropna().str.lower().str.strip().tolist())
                
                new_picks = [t for t in search_results['tracks']['items'] if t['id'] not in clean_ids and t['name'].lower().strip() not in original_names]
                
                if new_picks:
                    best_match = random.choice(new_picks)
                    st.markdown("<h3 style='margin-bottom: 20px;'>owen would listen to this :)</h3>", unsafe_allow_html=True)
                    
                    # LARGE SPOTIFY PLAYER
                    embed_url = f"https://open.spotify.com/embed/track/{best_match['id']}?utm_source=generator"
                    components.iframe(embed_url, height=220) # Increased height for 'Large/Long' look
                    
                    with st.expander("VIEW LOG DATA"):
                        st.write(f"SEED: {selected_song}")
                        st.write(f"NEW DISCOVERY: {best_match['name']} by {best_match['artists'][0]['name']}")
                else:
                    st.error("NO NEW TRACKS FOUND.")

st.markdown("<p class='white-footer'>HAND-CODED BY OWEN</p>", unsafe_allow_html=True)

# --- 6. Sparkle Script ---
sparkle_js = """
<script>
const parent = window.parent.document;
if (!parent.getElementById("sparkle-style")) {
    const style = parent.createElement("style");
    style.id = "sparkle-style";
    style.innerHTML = `.sparkle-trail { position: fixed; pointer-events: none; width: 10px; height: 10px; background: radial-gradient(circle, #ffffff 20%, rgba(255,255,255,0) 80%); border-radius: 50%; z-index: 999999; animation: fall 0.8s linear forwards; } @keyframes fall { 0% { transform: scale(1); opacity: 1; } 100% { transform: scale(0.2) translateY(30px); opacity: 0; } }`;
    parent.head.appendChild(style);
    parent.addEventListener("mousemove", (e) => {
        if (Math.random() > 0.6) return;
        const spark = parent.createElement("div");
        spark.className = "sparkle-trail";
        spark.style.left = (e.clientX - 5) + "px";
        spark.style.top = (e.clientY - 5) + "px";
        parent.body.appendChild(spark);
        setTimeout(() => { spark.remove(); }, 800);
    });
}
</script>
"""
components.html(sparkle_js, height=0, width=0)
