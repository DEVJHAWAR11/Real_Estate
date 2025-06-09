import streamlit as st
import pickle
import pandas as pd
import numpy as np

# Page configuration
st.set_page_config(
    page_title="🏡 Property Price Predictor",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for cards, buttons, and animations

st.markdown("""
<style>
[data-testid="stSidebar"] {
    background: linear-gradient(135deg, #232526 0%, #2c5364 100%);
    color: #f8fafc;
    border-top-right-radius: 20px;
    border-bottom-right-radius: 20px;
    box-shadow: 2px 0 12px rgba(0,0,0,0.2);
}
[data-testid="stSidebarNav"] ul li a {
    color: #f8fafc !important;
    font-size: 1.1rem;
    font-weight: 500;
    border-radius: 10px;
    padding: 0.5rem 1.2rem;
    transition: background 0.2s, color 0.2s;
}
[data-testid="stSidebarNav"] ul li a:hover {
    background: #3a3f4b;
    color: #60a5fa !important;
}
[data-testid="stSidebarNav"] ul li a.active {
    background: #4f8cff;
    color: #fff !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
    .stApp {
        background: #111827 !important;
        background-attachment: fixed;
    }
    .card {
        background: rgba(30,41,59,0.95);
        border-radius: 20px;
        box-shadow: 0 8px 32px 0 rgba(31,38,135,0.37);
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        border: 1px solid rgba(255,255,255,0.18);
        padding: 2rem;
        margin-bottom: 2rem;
        transition: transform 0.2s;
    }
    .card:hover {
        transform: scale(1.02) rotateY(2deg);
        box-shadow: 0 16px 40px 0 rgba(31,38,135,0.37);
    }
    .floating {
        animation: float 3s ease-in-out infinite;
    }
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }
    .stButton button {
        background-color: #10B981 !important;
        color: white !important;
        font-weight: bold;
        border-radius: 10px;
        border: none;
        padding: 0.7rem 1.5rem;
        font-size: 1.1rem;
        box-shadow: 0 2px 8px rgba(16,185,129,0.2);
        transition: background 0.3s, transform 0.2s;
    }
    .stButton button:hover {
        background-color: #059669 !important;
        transform: scale(1.05);
    }
    .stSlider > div[data-baseweb="slider"] {
background: linear-gradient(90deg, #D8B5FF 0%, #1EAE98 100%);
        border-radius: 10px;
        padding: 5px;
    }
    </style>
    """, unsafe_allow_html=True)


# Load DataFrame and pipeline
# try:
#     with open('df.pkl', 'rb') as file:
#         df = pickle.load(file)
#         # df=pd.read_pickle('df.pkl')
#     with open('pipeline.pkl', 'rb') as file:
#         pipeline = pickle.load(file)
# except FileNotFoundError:
#     st.error("Could not load df.pkl or pipeline.pkl. Please make sure they exist.")
#     st.stop()

import os
import requests

base_dir = os.path.dirname(os.path.abspath(__file__))
df_path = os.path.join(base_dir, 'df.pkl')
with open(df_path, 'rb') as file:
    df = pickle.load(file)

import gdown




@st.cache_data
def download_from_gdrive(file_id, destination):
    url = f"https://drive.google.com/uc?id={file_id}"
    gdown.download(url, destination, quiet=False)
    return destination

file_id = "1alSmJrC2k5kbGg1-tfeqF_eLQ8yQ0_C7"
pipeline_path = download_from_gdrive(file_id, "pipeline.pkl")

with open(pipeline_path, "rb") as file:
    pipeline = pickle.load(file)

    





# Visual header (emoji)
st.markdown("<h1 style='text-align: center; font-size: 3em;'>🏠</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='margin-bottom:0; text-align: center; color: #10B981;'>🏙️ Property Price Prediction App</h2>", unsafe_allow_html=True)

# Sidebar Info
with st.sidebar:
    st.title("ℹ️ About")
    with st.expander("How to use"):
        st.write("""
            Predict property prices using:
            - **Location**
            - **Size & Rooms**
            - **Property Age**
            - **Amenities & Category**
            ---
            Built with 💡 by a Data Science Enthusiast.
        """)

# Main content card
st.markdown('<div class="card">', unsafe_allow_html=True)

# Input form
with st.form("prediction_form"):
    st.header("Enter your inputs")
    col1, col2 = st.columns(2)
    with col1:
        property_type = st.selectbox('🏠 Property Type', ['flat', 'house'])
        bedrooms = float(st.selectbox('🛏️ Number of Bedrooms', sorted(df['bedRoom'].unique())))
        balcony = st.selectbox('🌿 Number of Balconies', sorted(df['balcony'].unique()))
        servant_room = float(st.selectbox('🧹 Servant Room', [0.0, 1.0]))
        furnishing_type = st.selectbox('🛋️ Furnishing Type', sorted(df['furnishing_type'].unique()))
        built_up_area = st.slider('📐 Built Up Area (sqft)', 100.0, 5000.0, 1000.0, step=50.0)
    with col2:
        sector = st.selectbox('📍 Sector', sorted(df['sector'].unique()))
        bathroom = float(st.selectbox('🚿 Number of Bathrooms', sorted(df['bathroom'].unique())))
        property_age = st.selectbox('📆 Property Age', sorted(df['agePossession'].unique()))
        store_room = float(st.selectbox('📦 Store Room', [0.0, 1.0]))
        luxury_category = st.selectbox('💎 Luxury Category', sorted(df['luxury_category'].unique()))
        floor_category = st.selectbox('🏢 Floor Category', sorted(df['floor_category'].unique()))
    colA, colB = st.columns(2)
    with colA:
        predict = st.form_submit_button("🔮 Predict")
    with colB:
        show_summary = st.form_submit_button("📝 Show Summary")

st.markdown('</div>', unsafe_allow_html=True)

# Handle prediction and summary
if show_summary:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Your Inputs:")
    st.markdown(f"""
    - **Type:** {property_type}
    - **Sector:** {sector}
    - **Bedrooms:** {bedrooms}
    - **Bathrooms:** {bathroom}
    - **Balconies:** {balcony}
    - **Built-up Area:** {built_up_area} sqft
    - **Servant Room:** {servant_room}
    - **Store Room:** {store_room}
    - **Furnishing:** {furnishing_type}
    - **Luxury:** {luxury_category}
    - **Floor:** {floor_category}
    - **Age:** {property_age}
    """)
    st.markdown('</div>', unsafe_allow_html=True)

if predict:
    with st.spinner("Calculating Price..."):
        # Create DataFrame for prediction
        data = [[property_type, sector, bedrooms, bathroom, balcony, property_age,
                built_up_area, servant_room, store_room,
                furnishing_type, luxury_category, floor_category]]
        columns = ['property_type', 'sector', 'bedRoom', 'bathroom', 'balcony',
                'agePossession', 'built_up_area', 'servant room', 'store room',
                'furnishing_type', 'luxury_category', 'floor_category']
        one_df = pd.DataFrame(data, columns=columns)
        # Predict
        base_price = np.expm1(pipeline.predict(one_df))[0]
        low = base_price - 0.22
        high = base_price + 0.22
        # Display result in a floating, card-like container
        st.markdown(f"""
        <div class="card floating">
            <h3 style="color: #10B981; margin-top: 0;">🏷️ Estimated Price</h3>
            <p style="font-size: 2rem; font-weight: bold; margin-bottom: 0;">₹{round(low, 2)} Cr – ₹{round(high, 2)} Cr</p>
        </div>
        """, unsafe_allow_html=True)
