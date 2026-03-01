import streamlit as st
import pickle
import pandas as pd
import numpy as np
import os
import gdown

st.set_page_config(
    page_title="Property Price Predictor",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load DataFrame
base_dir = os.path.dirname(os.path.abspath(__file__))
df_path = os.path.join(base_dir, 'df.pkl')
with open(df_path, 'rb') as file:
    df = pickle.load(file)

# Download pipeline from Google Drive
@st.cache_data
def download_from_gdrive(file_id, destination):
    url = f"https://drive.google.com/uc?id={file_id}"
    gdown.download(url, destination, quiet=False)
    return destination

file_id = "1alSmJrC2k5kbGg1-tfeqF_eLQ8yQ0_C7"
pipeline_path = download_from_gdrive(file_id, "pipeline.pkl")

with open(pipeline_path, "rb") as file:
    pipeline = pickle.load(file)

# Header
st.title("🏠 Property Price Predictor")
st.caption("Get an instant price estimate based on property details.")
st.divider()

# Sidebar
with st.sidebar:
    st.header("ℹ️ How to use")
    st.write("""
    Fill in the property details and click **Predict** to get an estimated price range.

    Inputs used:
    - Location & Sector
    - Size & Room count
    - Property Age
    - Amenities & Category
    """)

# Input form
with st.form("prediction_form"):
    col1, col2 = st.columns(2)
    with col1:
        property_type = st.selectbox('🏠 Property Type', ['flat', 'house'])
        bedrooms = float(st.selectbox('🛏️ Bedrooms', sorted(df['bedRoom'].unique())))
        balcony = st.selectbox('🌿 Balconies', sorted(df['balcony'].unique()))
        servant_room = float(st.selectbox('🧹 Servant Room', [0.0, 1.0]))
        furnishing_type = st.selectbox('🛋️ Furnishing Type', sorted(df['furnishing_type'].unique()))
        built_up_area = st.slider('📐 Built Up Area (sqft)', 100.0, 5000.0, 1000.0, step=50.0)
    with col2:
        sector = st.selectbox('📍 Sector', sorted(df['sector'].unique()))
        bathroom = float(st.selectbox('🚿 Bathrooms', sorted(df['bathroom'].unique())))
        property_age = st.selectbox('📆 Property Age', sorted(df['agePossession'].unique()))
        store_room = float(st.selectbox('📦 Store Room', [0.0, 1.0]))
        luxury_category = st.selectbox('💎 Luxury Category', sorted(df['luxury_category'].unique()))
        floor_category = st.selectbox('🏢 Floor Category', sorted(df['floor_category'].unique()))

    colA, colB = st.columns(2)
    with colA:
        predict = st.form_submit_button("🔮 Predict Price", use_container_width=True)
    with colB:
        show_summary = st.form_submit_button("📝 Show Summary", use_container_width=True)

# Summary
if show_summary:
    st.subheader("Your Inputs")
    summary_data = {
        "Field": ["Type", "Sector", "Bedrooms", "Bathrooms", "Balconies",
                  "Built-up Area", "Servant Room", "Store Room",
                  "Furnishing", "Luxury", "Floor", "Age"],
        "Value": [property_type, sector, bedrooms, bathroom, balcony,
                  f"{built_up_area} sqft", servant_room, store_room,
                  furnishing_type, luxury_category, floor_category, property_age]
    }
    st.table(pd.DataFrame(summary_data))

# Prediction
if predict:
    with st.spinner("Calculating price..."):
        data = [[property_type, sector, bedrooms, bathroom, balcony, property_age,
                 built_up_area, servant_room, store_room,
                 furnishing_type, luxury_category, floor_category]]
        columns = ['property_type', 'sector', 'bedRoom', 'bathroom', 'balcony',
                   'agePossession', 'built_up_area', 'servant room', 'store room',
                   'furnishing_type', 'luxury_category', 'floor_category']
        one_df = pd.DataFrame(data, columns=columns)
        base_price = np.expm1(pipeline.predict(one_df))[0]
        low = base_price - 0.22
        high = base_price + 0.22
        st.success(f"### 🏷️ Estimated Price: ₹{round(low, 2)} Cr – ₹{round(high, 2)} Cr")
