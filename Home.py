import streamlit as st

st.set_page_config(
    page_title="Real Estate AI Suite",
    page_icon="🏘️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🏘️ Real Estate AI Suite")
st.caption("Empowering your property journey with smart analytics, price predictions, and personalized recommendations.")
st.divider()

col1, col2, col3 = st.columns(3, gap="large")

with col1:
    st.subheader("📊 Analytics Dashboard")
    st.write("Visualize property trends, market insights, and sector-wise price distributions with interactive charts and maps.")
    if st.button("Explore Analytics →", use_container_width=True, key="analytics"):
        st.switch_page("pages/Analysis_App.py")

with col2:
    st.subheader("🔮 Price Predictor")
    st.write("Get instant price estimates for any property based on location, size, amenities, and more.")
    if st.button("Predict Prices →", use_container_width=True, key="predictor"):
        st.switch_page("pages/Price_Predictor.py")

with col3:
    st.subheader("🤖 Recommender System")
    st.write("Discover properties similar to your favorites with our AI-powered recommendation engine.")
    if st.button("Find Recommendations →", use_container_width=True, key="recommender"):
        st.switch_page("pages/Recommender.py")

st.divider()
st.caption("Built with ❤️ by Dev | Powered by Streamlit")
