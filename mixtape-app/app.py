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
    
    /* THE FIX: Floating Frame Border - Pure White Ridge using Relative Sizes */
    .stApp::after {{
        content: "";
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        border: 4vw ridge #ffffff !important; 
        pointer-events: none; 
        z-index: 9999;
    }}
    
    /* THE PREMIUM ULTRA-GLASS CARD WITH INVERTED RIDGE BORDER */
    .main .block-container {{
        background-color: rgba(255, 255, 255, 0.15) !important; 
        -webkit-backdrop-filter: blur(30px) brightness(1.1) !important;
        backdrop-filter: blur(30px) brightness(1.1) !important;
        
        padding: 5vh 5vw;
        border-radius: 12px; 
        
        /* INVERTED BORDERS: White Ridge + Dark Red Outline */
        border: 1.5vw ridge #ffffff !important; 
        outline: 0.8vw solid #8b0000 !important; 
        
        box-shadow: 0px 25px 50px rgba(0,0,0,0.8);
        margin: 10vh auto !important;
        width: 80vw !important;
        max-width: 700px;
    }}

    /* Global Typography Base - Forcing ALL text to be BOLD ALL CAPS with 3D Effects */
    .main .block-container h1, 
    .main .block-container h2, 
    .main .block-container h3, 
    .main .block-container p, 
    .main .block-container label, 
    .main .block-container span,
    .stMarkdown {{
        font-family: 'Arial Black', Gadget, sans-serif !important;
        font-weight: 900 !important;
        text-transform: uppercase !important; 
        letter-spacing: -1px;
        line-height: 1.2;
        /* 3D Red & Black Drop Shadow */
        text-shadow: 2px 2px 0px #8b0000, 4px 4px 8px rgba(0,0,0,0.7) !important;
        color: #ffffff !important;
    }}

    /* Specific Sizing for Titles */
    .white-text-title h1 {{
        font-size: clamp(24px, 6vw, 48px) !important;
        text-align: center;
        margin-bottom: 10px;
        text-shadow: 3px 3px 0px #8b0000, 6px 6px 15px rgba(0,0,0,0.9) !important;
    }}
    
    /* Cassette Emoji with white glow */
    .mixtape-emoji {{
        display: inline-block;
        filter: brightness(0) invert(1);
        text-shadow: 0 0 15px #ffffff;
    }}

    /* Thick White Subtitle */
    .thick-white-text-sub p {{
        text-align: center;
        font-size: clamp(14px, 3.5vw, 20px) !important; 
        font-weight: 900 !important;
        margin-top: 20px;
        margin-bottom: 30px;
        color: #ffffff !important;
        text-shadow: 2px 2px 0px #8b0000, 4px 4px 8px rgba(0,0,0,0.8) !important;
    }}

    /* SEARCH LABEL */
    div[data-testid="stSelectbox"] label p, 
    div[data-testid="stSelectbox"] label {{
        color: #ffffff !important;
        font-size: clamp(12px, 3vw, 18px) !important;
        text-shadow: 2px 2px 0px #8b0000, 4px 4px 8px rgba(0,0,0,0.7) !important;
    }}

    /* PREMIUM SEARCH BAR (Selectbox) - WHITE RIDGE */
    div[data-baseweb="select"] {{
        border: 0.8vw ridge #ffffff !important;
        border-radius: 4px !important;
        background-color: #ffffff !important;
        cursor: text !important;
    }}
    
    div[data-baseweb="select"] span {{
        color: #8b0000 !important;
        font-family: 'Arial Black', Gadget, sans-serif !important;
        font-weight: 900 !important;
        font-size: clamp(12px, 3vw, 18px) !important;
        text-shadow: none !important;
    }}

    /* MASSIVE BUTTON - WHITE RIDGE */
    div.stButton > button:first-child {{
        width: 100% !important;
        height: 10vh !important;
        min-height: 60px;
        border: 0.8vw ridge #ffffff !important;
        border-radius: 4px !important;
        background-color: #ffffff !important; 
        color: #8b0000 !important; 
        font-family: 'Arial Black', Gadget, sans-serif !important;
        font-weight: 900 !important;
        box-shadow: 0px 8px 15px rgba(0,0,0,0.6);
        transition: all 0.2s ease-in-out;
    }}
    
    div.stButton > button:first-child p {{
        color: #8b0000 !important; 
        font-size: clamp(16px, 4vw, 24px) !important;
        font-weight: 900 !important;
        text-shadow: none !important; 
    }}
    
    div.stButton > button:hover {{
        background-color: #8b0000 !important;
        border: 0.8vw ridge #ffffff !important;
    }}

    div.stButton > button:hover p {{
        color: #ffffff !important;
    }}

    /* Expander */
    div[data-testid="stExpander"] {{
        border: 0.5vw solid #ffffff !important;
        border-radius: 4px !important;
        background-color: rgba(139, 0, 0, 0.4) !important; 
        margin-top: 15px;
    }}
    
    div[data-testid="stExpander"] * {{
        color: #ffffff !important;
        fill: #ffffff !important;
        stroke: #ffffff !important;
    }}

    div[data-testid="stExpander"] summary svg {{
        display: none !important;
    }}

    /* CUSTOM BARELY VISIBLE WHITE FOOTER */
    .white-footer {{
        color: rgba(255, 255, 255, 0.2) !important; 
        text-align: center;
        font-family: 'Arial Black', Gadget, sans-serif !important;
        margin-top: 40px;
        font-size: 14px;
        letter-spacing: 1px;
        text-shadow: none !important;
        text-transform: none !important; /* Allow mixed case for footer */
        margin-bottom: 50px;
    }}

    /* MOBILE SPECIFIC OVERRIDES */
    @media (max-width: 480px) {{
        .stApp::after {{
            border-width: 6vw ridge #ffffff !important;
        }}
        .main .block-container {{
            width: 85vw !important;
            padding: 20px !important;
            margin: 8vh auto !important;
        }}
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

# --- 3. Setup Direct Spotify API ---
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

# --- 4. Load Data ---
@st.cache_data
def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "polyjamorous.csv")
    return pd.read_csv(file_path)

df = load_data()
df['Display Name'] = df['Song'] + " by " + df['Artist']

# --- 5. UI Layout ---
st.markdown('<div class="white-text-title"><h1>THE COUNTER-MIXTAPE <span class="mixtape-emoji">📼</span></h1></div>', unsafe_allow_html=True)

st.markdown('<div class="thick-white-text-sub"><p>CHOOSE YOUR JAM AND FIND OUT WHAT I WOULD RECOMMEND <br> HOPE THIS IS FUN ENOUGH BUT NOT TOO DISTRACTING YOU GOT THIS CUTIE !!!</p></div>', unsafe_allow_html=True)

st.write("") 

selected_song = st.selectbox("SEARCH OR PICK A TRACK", df['Display Name'].tolist())

st.write("")

if st.button("GENERATE MY PERFECT MATCH"):
    song_data = df[df['Display Name'] == selected_song].iloc[0]
    
    with st.spinner("CRUNCHING DATA..."):
        token = get_spotify_token(client_id, client_secret)
        
        if not token:
            st.error("FAILED TO AUTHENTICATE")
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
                    st.markdown("<h3 style='text-align: center; margin-bottom: 20px;'>OWEN WOULD LISTEN TO THIS :)</h3>", unsafe_allow_html=True)
                    embed_url = f"https://open.spotify.com/embed/track/{best_match['id']}?utm_source=generator"
                    components.iframe(embed_url, height=152)
                    
                    with st.expander("VIEW LOG DATA"):
                        st.write(f"SEED: {selected_song}")
                        st.write(f"NEW DISCOVERY: {best_match['name']} by {best_match['artists'][0]['name']}")
                else:
                    st.error("NO NEW TRACKS FOUND")

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<p class='white-footer'>Hand-coded By Owen :D</p>", unsafe_allow_html=True)

# --- Sparkle Mouse Trail ---
sparkle_js = """
<script>
const parent = window.parent.document;
if (!parent.getElementById("sparkle-style")) {
    const style = parent.createElement("style");
    style.id = "sparkle-style";
    style.innerHTML = `.sparkle-trail { position: fixed; pointer-events: none; width: 10px; height: 10px; background: white; border-radius: 50%; z-index: 999999; box-shadow: 0 0 8px white; animation: fall 0.8s linear forwards; } @keyframes fall { 0% { transform: scale(1); opacity: 1; } 100% { transform: scale(0.2) translateY(30px); opacity: 0; } }`;
    parent.head.appendChild(style);
    parent.addEventListener("mousemove", (e) => {
        if (Math.random() > 0.6) return;
        const spark = parent.createElement("div");
        spark.className = "sparkle-trail";
        spark.style.left = (e.clientX - 5) + "px"; spark.style.top = (e.clientY - 5) + "px";
        parent.body.appendChild(spark);
        setTimeout(() => spark.remove(), 800);
    });
}
</script>
"""
components.html(sparkle_js, height=0, width=0)
