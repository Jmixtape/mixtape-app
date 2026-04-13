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
        pointer-events: none; /* Lets you click through the border */
        z-index: 9999;
    }}
    
    /* THE PREMIUM ULTRA-GLASS CARD WITH INVERTED RIDGE BORDER */
    .main .block-container {{
        background-color: rgba(255, 255, 255, 0.15) !important; 
        -webkit-backdrop-filter: blur(30px) brightness(1.1) !important;
        backdrop-filter: blur(30px) brightness(1.1) !important;
        
        padding: 50px 60px;
        border-radius: 12px; 
        
        /* INVERTED BORDERS: White Ridge + Dark Red Outline */
        border: 14px ridge #ffffff !important; 
        outline: 6px solid #8b0000 !important; 
        
        box-shadow: 0px 25px 50px rgba(0,0,0,0.8);
        margin-top: 60px; /* Safely pushed down away from the top frame */
        margin-bottom: 60px;
    }}

    /* Global Typography Base - Forcing ALL text to be BOLD with 3D Effects */
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
        /* 3D Red & Black Drop Shadow */
        text-shadow: 2px 2px 0px #8b0000, 4px 4px 8px rgba(0,0,0,0.7) !important;
        color: #ffffff !important;
    }}

    /* Specific Sizing for Titles */
    .white-text-title h1 {{
        font-size: 46px !important;
        text-align: center;
        margin-bottom: 10px;
        text-shadow: 3px 3px 0px #8b0000, 6px 6px 15px rgba(0,0,0,0.9) !important;
    }}
    
    /* Thick White Subtitle */
    .thick-white-text-sub p {{
        text-align: center;
        font-size: 20px !important; 
        font-weight: 900 !important;
        margin-bottom: 30px;
        color: #ffffff !important;
        text-shadow: 2px 2px 0px #8b0000, 4px 4px 8px rgba(0,0,0,0.8) !important;
    }}

    /* FORCING THE SEARCH LABEL TO BE WHITE */
    div[data-testid="stSelectbox"] label p, 
    div[data-testid="stSelectbox"] label {{
        color: #ffffff !important;
        font-size: 18px !important;
        text-shadow: 2px 2px 0px #8b0000, 4px 4px 8px rgba(0,0,0,0.7) !important;
    }}

    /* PREMIUM SEARCH BAR (Selectbox) - INVERTED TO WHITE RIDGE */
    div[data-baseweb="select"] {{
        border: 6px ridge #ffffff !important;
        border-radius: 4px !important;
        background-color: #ffffff !important;
        cursor: text !important;
    }}
    
    /* Force the text inside the search box to be bold and dark red */
    div[data-baseweb="select"] span {{
        color: #8b0000 !important;
        font-family: 'Arial Black', Gadget, sans-serif !important;
        font-weight: 900 !important;
        font-size: 18px !important;
        text-shadow: none !important;
    }}

    /* MASSIVE BUTTON - INVERTED TO WHITE RIDGE */
    div.stButton > button:first-child {{
        width: 100% !important;
        height: 75px !important;
        border: 6px ridge #ffffff !important;
        border-radius: 4px !important;
        background-color: #ffffff !important; 
        color: #8b0000 !important; 
        font-size: 24px !important;
        font-family: 'Arial Black', Gadget, sans-serif !important;
        font-weight: 900 !important;
        text-transform: uppercase !important;
        box-shadow: 0px 8px 15px rgba(0,0,0,0.6);
        transition: all 0.2s ease-in-out;
    }}
    
    div.stButton > button:first-child p {{
        color: #8b0000 !important; 
        font-size: 26px !important;
        font-weight: 900 !important;
        text-shadow: none !important; 
    }}
    
    div.stButton > button:hover {{
        background-color: #8b0000 !important;
        border: 6px ridge #ffffff !important;
    }}

    div.stButton > button:hover p {{
        color: #ffffff !important;
        text-shadow: 2px 2px 5px rgba(0,0,0,0.8) !important;
    }}
    
    div.stButton > button:active {{
        transform: translateY(4px);
        box-shadow: 0px 4px 10px rgba(0,0,0,0.4);
    }}

    /* Absolute Sledgehammer to force the Expander */
    div[data-testid="stExpander"] {{
        border: 4px solid #ffffff !important;
        border-radius: 4px !important;
        background-color: rgba(139, 0, 0, 0.4) !important; 
        margin-top: 15px;
    }}
    
    div[data-testid="stExpander"] * {{
        color: #ffffff !important;
        fill: #ffffff !important;
        stroke: #ffffff !important;
    }}

    div[data-testid="stExpander"] summary:hover *, 
    div[data-testid="stExpander"] summary:focus * {{
        color: #ffffff !important;
        fill: #ffffff !important;
        stroke: #ffffff !important;
        outline: none !important;
    }}
    
    div[data-testid="stExpander"] summary svg, 
    div[data-testid="stExpander"] summary .stIcon,
    div[data-testid="stExpander"] summary span[data-testid="stExpanderIcon"] {{
        display: none !important;
    }}

    /* CUSTOM BARELY VISIBLE WHITE FOOTER */
    .white-footer {{
        color: rgba(255, 255, 255, 0.2) !important; /* 20% Opacity */
        text-align: center;
        font-family: 'Arial Black', Gadget, sans-serif !important;
        margin-top: 40px;
        font-size: 16px;
        letter-spacing: 1px;
        text-shadow: none !important; /* Removed shadow so it hides better */
    }}

    /* MOBILE RESPONSIVENESS FIXES */
    @media (max-width: 768px) {{
        .stApp::after {{
            border-width: 10px ridge #ffffff !important; /* Thinner frame on mobile */
        }}
        .main .block-container {{
            padding: 30px 20px !important; /* Less padding to fit screens */
            border-width: 8px !important;
            outline-width: 4px !important;
            margin-top: 40px !important;
            margin-bottom: 40px !important;
        }}
        .white-text-title h1 {{
            font-size: 32px !important; /* Scale down massive title */
        }}
        .thick-white-text-sub p {{
            font-size: 16px !important; /* Scale down subtitle */
        }}
        div.stButton > button:first-child {{
            height: 60px !important;
        }}
        div.stButton > button:first-child p {{
            font-size: 20px !important;
        }}
        div[data-testid="stSelectbox"] label p {{
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
    else:
        st.error(f"API Error {response.status_code}: {response.text}")
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
# THE FIX: Added white cassette emoji with CSS trick to force pure white color
st.markdown('<div class="white-text-title"><h1>THE COUNTER-MIXTAPE <span style="filter: brightness(0) invert(1);">📼</span></h1></div>', unsafe_allow_html=True)

# Thick White Subtitle text
st.markdown('<div class="thick-white-text-sub"><p>choose your jam and find out what I would recommend <br> Hope this is fun enough but not too distracting you got this Cutie !!!</p></div>', unsafe_allow_html=True)

st.write("") 

selected_song = st.selectbox("SEARCH OR PICK A TRACK", df['Display Name'].tolist())

st.write("")

if st.button("GENERATE MY PERFECT MATCH"):
    song_data = df[df['Display Name'] == selected_song].iloc[0]
    
    with st.spinner("CRUNCHING DATA..."):
        token = get_spotify_token(client_id, client_secret)
        
        if not token:
            st.error("FAILED TO AUTHENTICATE WITH SPOTIFY.")
        else:
            search_query = str(song_data['Artist']).strip()
            search_results = search_spotify_tracks(token, search_query)
            
            if search_results and 'tracks' in search_results and search_results['tracks']['items']:
                
                original_ids = set(df['Spotify Track Id'].dropna().astype(str).tolist())
                clean_ids = {str(uid).split('/')[-1].split('?')[0].split(':')[-1] for uid in original_ids}
                original_names = set(df['Song'].dropna().str.lower().str.strip().tolist())
                
                new_picks = []
                for t in search_results['tracks']['items']:
                    track_name_lower = t['name'].lower().strip()
                    if t['id'] not in clean_ids and track_name_lower not in original_names:
                        new_picks.append(t)
                
                if new_picks:
                    best_match = random.choice(new_picks)
                    
                    st.markdown("<h3 style='text-align: center; margin-bottom: 20px;'>owen would listen to this :)</h3>", unsafe_allow_html=True)
                    
                    embed_url = f"https://open.spotify.com/embed/track/{best_match['id']}?utm_source=generator"
                    components.iframe(embed_url, width=300, height=152)
                    
                    with st.expander("VIEW LOG DATA"):
                        st.write(f"SEED: {selected_song}")
                        st.write(f"NEW DISCOVERY: {best_match['name']} by {best_match['artists'][0]['name']}")
                else:
                    st.error("NO NEW TRACKS FOUND THAT AREN'T ALREADY IN THE MIXTAPE")
            elif search_results:
                st.error("ARTIST NOT FOUND ON SPOTIFY")

# --- Footer in White ---
st.markdown("<br>", unsafe_allow_html=True)
# THE FIX: Faded, barely visible, non-capitalized footer
st.markdown("<p class='white-footer'>Hand-coded By Owen :D</p>", unsafe_allow_html=True)

# --- 6. Custom Magic Sparkle Mouse Trail Script ---
sparkle_js = """
<script>
const parent = window.parent.document;
if (!parent.getElementById("sparkle-style")) {
    const style = parent.createElement("style");
    style.id = "sparkle-style";
    style.innerHTML = `
    .sparkle-trail {
        position: fixed;
        pointer-events: none; /* Ignore mouse clicks */
        width: 10px;
        height: 10px;
        background: radial-gradient(circle, #ffffff 20%, rgba(255,255,255,0) 80%);
        border-radius: 50%;
        z-index: 999999;
        box-shadow: 0px 0px 8px #ffffff;
        animation: fall 0.8s linear forwards;
    }
    @keyframes fall {
        0% { transform: scale(1) translateY(0); opacity: 1; }
        100% { transform: scale(0.2) translateY(30px); opacity: 0; }
    }
    `;
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
