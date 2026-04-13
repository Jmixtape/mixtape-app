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
    
    /* Floating Frame Border - Pure White Ridge */
    .stApp::after {{
        content: "";
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        border: 20px ridge #ffffff !important; 
        pointer-events: none;
        z-index: 9999;
    }}
    
    /* THE PREMIUM ULTRA-GLASS CARD */
    .main .block-container {{
        background-color: rgba(255, 255, 255, 0.15) !important; 
        -webkit-backdrop-filter: blur(30px) brightness(1.1) !important;
        backdrop-filter: blur(30px) brightness(1.1) !important;
        
        padding: 50px 60px;
        border-radius: 12px; 
        
        /* White Ridge + Dark Red Outline */
        border: 14px ridge #ffffff !important; 
        outline: 6px solid #8b0000 !important; 
        
        box-shadow: 0px 25px 50px rgba(0,0,0,0.8);
        margin-top: 60px;
        margin-bottom: 60px;
        max-width: 90%; /* Keeps it from hitting borders on desktop */
    }}

    /* Global Typography - MIXED CASE & BOLD */
    .main .block-container h1, 
    .main .block-container h2, 
    .main .block-container h3, 
    .main .block-container p, 
    .main .block-container label, 
    .main .block-container span,
    .stMarkdown {{
        font-family: 'Arial Black', Gadget, sans-serif !important;
        font-weight: 900 !important;
        /* THE FIX: REMOVED UPPERCASE */
        text-transform: none !important; 
        letter-spacing: -0.5px;
        line-height: 1.4;
        text-shadow: 2px 2px 0px #8b0000, 4px 4px 8px rgba(0,0,0,0.7) !important;
        color: #ffffff !important;
    }}

    /* Title Styling */
    .white-text-title h1 {{
        font-size: 42px !important;
        text-align: center;
        margin-bottom: 10px;
        text-shadow: 3px 3px 0px #8b0000, 6px 6px 15px rgba(0,0,0,0.9) !important;
    }}
    
    /* Emoji styling - Subtle glow, no solid block */
    .mixtape-emoji {{
        display: inline-block;
        text-shadow: 0 0 10px #ffffff, 0 0 20px #ffffff;
    }}

    /* Subtitle text */
    .thick-white-text-sub p {{
        text-align: center;
        font-size: 19px !important; 
        margin-bottom: 30px;
        color: #ffffff !important;
    }}

    /* Search Label */
    div[data-testid="stSelectbox"] label p {{
        font-size: 18px !important;
    }}

    /* Search Bar */
    div[data-baseweb="select"] {{
        border: 6px ridge #ffffff !important;
        border-radius: 4px !important;
        background-color: #ffffff !important;
    }}
    
    div[data-baseweb="select"] span {{
        color: #8b0000 !important;
        font-family: 'Arial Black', sans-serif !important;
        text-shadow: none !important;
    }}

    /* Button */
    div.stButton > button:first-child {{
        width: 100% !important;
        height: 70px !important;
        border: 6px ridge #ffffff !important;
        border-radius: 4px !important;
        background-color: #ffffff !important; 
        color: #8b0000 !important; 
        font-family: 'Arial Black', sans-serif !important;
        box-shadow: 0px 8px 15px rgba(0,0,0,0.6);
        transition: all 0.2s;
    }}
    
    div.stButton > button:first-child p {{
        color: #8b0000 !important; 
        font-size: 22px !important;
        text-shadow: none !important; 
    }}
    
    div.stButton > button:hover {{
        background-color: #8b0000 !important;
    }}

    div.stButton > button:hover p {{
        color: #ffffff !important;
    }}

    /* Expander */
    div[data-testid="stExpander"] {{
        border: 4px solid #ffffff !important;
        background-color: rgba(139, 0, 0, 0.4) !important; 
    }}
    
    div[data-testid="stExpander"] summary svg {{
        display: none !important;
    }}

    /* Footer */
    .white-footer {{
        color: rgba(255, 255, 255, 0.3) !important;
        text-align: center;
        margin-top: 40px;
        font-size: 14px;
        text-shadow: none !important;
    }}

    /* MOBILE OPTIMIZATION - THE FIX FOR BORDERS & WIDTH */
    @media (max-width: 480px) {{
        .stApp::after {{
            border-width: 10px ridge #ffffff !important;
        }}
        .main .block-container {{
            /* Shrink width so it doesn't touch the outer white frame */
            width: 85% !important; 
            max-width: 85% !important;
            padding: 25px 15px !important;
            border-width: 8px !important;
            outline-width: 3px !important;
            margin: 30px auto !important; /* Center it */
        }}
        .white-text-title h1 {{
            font-size: 26px !important;
        }}
        .thick-white-text-sub p {{
            font-size: 14px !important;
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
    st.error("KEYS MISSING. Please check your Streamlit secrets!")
    st.stop()

@st.cache_data(ttl=3000)
def get_spotify_token(cid, csec):
    auth_str = f"{cid}:{csec}"
    b64_auth_str = base64.b64encode(auth_str.encode()).decode()
    headers = {
        "Authorization": f"Basic {b64_auth_str}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    response = requests.post("https://accounts.spotify.com/api/token", headers=headers, data=data)
    if response.status_code == 200:
        return response.json().get("access_token")
    return None

def search_spotify_tracks(token, query):
    headers = {"Authorization": f"Bearer {token}"}
    params = {"q": query, "type": "track"} 
    response = requests.get("https://api.spotify.com/v1/search", headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    return None

# --- 4. Load Data ---
@st.cache_data
def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "polyjamorous.csv")
    return pd.read_csv(file_path)

df = load_data()
df['Display Name'] = df['Song'] + " by " + df['Artist']

# --- 5. UI Layout ---
# THE FIX: Emoji with glow but no solid block
st.markdown('<div class="white-text-title"><h1>The Counter-Mixtape <span class="mixtape-emoji">📼</span></h1></div>', unsafe_allow_html=True)

st.markdown('<div class="thick-white-text-sub"><p>Choose your jam and find out what I would recommend <br> Hope this is fun enough but not too distracting you got this Cutie !!!</p></div>', unsafe_allow_html=True)

selected_song = st.selectbox("Search or pick a track", df['Display Name'].tolist())

if st.button("Generate My Perfect Match"):
    song_data = df[df['Display Name'] == selected_song].iloc[0]
    
    with st.spinner("Crunching data..."):
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
                    st.markdown("<h3 style='text-align: center; margin-bottom: 20px;'>Owen would listen to this :)</h3>", unsafe_allow_html=True)
                    embed_url = f"https://open.spotify.com/embed/track/{best_match['id']}?utm_source=generator"
                    components.iframe(embed_url, width=None, height=152) # Width None helps mobile sizing
                    
                    with st.expander("View log data"):
                        st.write(f"Seed: {selected_song}")
                        st.write(f"New Discovery: {best_match['name']} by {best_match['artists'][0]['name']}")
                else:
                    st.error("No new tracks found!")
            else:
                st.error("Artist not found.")

st.markdown("<p class='white-footer'>Hand-coded By Owen :D</p>", unsafe_allow_html=True)

# --- Sparkle Mouse Trail ---
sparkle_js = """
<script>
const parent = window.parent.document;
if (!parent.getElementById("sparkle-style")) {
    const style = parent.createElement("style");
    style.id = "sparkle-style";
    style.innerHTML = `.sparkle-trail { position: fixed; pointer-events: none; width: 8px; height: 8px; background: white; border-radius: 50%; z-index: 999999; box-shadow: 0 0 5px white; animation: fall 0.6s linear forwards; } @keyframes fall { 0% { opacity: 1; transform: scale(1); } 100% { opacity: 0; transform: scale(0.1) translateY(20px); } }`;
    parent.head.appendChild(style);
    parent.addEventListener("mousemove", (e) => {
        if (Math.random() > 0.7) return;
        const spark = parent.createElement("div");
        spark.className = "sparkle-trail";
        spark.style.left = e.clientX + "px"; spark.style.top = e.clientY + "px";
        parent.body.appendChild(spark);
        setTimeout(() => spark.remove(), 600);
    });
}
</script>
"""
components.html(sparkle_js, height=0, width=0)
