import streamlit as st
import pandas as pd
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


# --- 3. Load Data ---
# Spotify API blocks bypassed. Relying entirely on curated CSV.
@st.cache_data
def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "polyjamorous.csv")
    return pd.read_csv(file_path)

df = load_data()
df['Display Name'] = df['Song'] + " by " + df['Artist']

# --- 4. UI Layout ---
st.markdown('<div class="white-text-title"><h1>THE COUNTER-MIXTAPE</h1></div>', unsafe_allow_html=True)
st.markdown('<div class="white-text-sub"><p>choose your jam and find out what i would recommend Hope this helps you got this Cuitie HAPPY lockdown!!</p></div>', unsafe_allow_html=True)

st.write("") 

selected_song = st.selectbox("PICK A TRACK", df['Display Name'].tolist())

if st.button("GENERATE MY PERFECT MATCH"):
    with st.spinner("CRUNCHING DATA..."):
        try:
            # THE FIX: Bypass Spotify's blocked API and use your CSV data directly
            potential_matches = df[df['Display Name'] != selected_song]
            
            if not potential_matches.empty:
                # Pick a random track from the remaining pool
                best_match = potential_matches.sample(1).iloc[0]
                
                # Extract and clean the ID (Handles raw IDs, full URLs, or URIs)
                raw_id = str(best_match['Spotify Track Id'])
                clean_id = raw_id.split('/')[-1].split('?')[0].split(':')[-1]
                
                st.markdown("### MATCH FOUND")
                
                # Render the standard Spotify iframe using the cleaned ID
                embed_url = f"https://open.spotify.com/embed/track/{clean_id}?utm_source=generator"
                components.iframe(embed_url, width=300, height=152)
                
                with st.expander("VIEW LOG DATA"):
                    st.write(f"SEED: {selected_song}")
                    st.write(f"MATCH: {best_match['Display Name']}")
            else:
                st.error("NOT ENOUGH DATA IN CSV TO FIND A MATCH")
                
        except Exception as e:
            st.error(f"ERROR: {e}")

# --- Footer in White ---
st.markdown("<br><br><br>", unsafe_allow_html=True)
st.markdown("<p class='white-footer'>HAND-CODED BY OWEN</p>", unsafe_allow_html=True)
