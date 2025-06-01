import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Real Estate AI Suite",
    page_icon="🏘️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for smooth animations and modern look

st.markdown("""
<style>
/* Sidebar background and border */
[data-testid="stSidebar"] {
    background: linear-gradient(135deg, #232526 0%, #2c5364 100%);
    color: #f8fafc;
    border-top-right-radius: 20px;
    border-bottom-right-radius: 20px;
    box-shadow: 2px 0 12px rgba(0,0,0,0.2);
}

/* Sidebar navigation links */
[data-testid="stSidebarNav"] > ul {
    margin-top: 2rem;
}
[data-testid="stSidebarNav"] ul li {
    margin-bottom: 1.2rem;
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

/* Sidebar title/logo */
[data-testid="stSidebar"] .css-1v3fvcr {
    margin-top: 1rem;
    margin-bottom: 2rem;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
    /* Main background */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #232526 0%, #414345 100%);
        background-attachment: fixed;
    }
    /* Card styling */
    .card {
        background: rgba(30,41,59,0.98);
        border-radius: 16px;
        box-shadow: 0 8px 32px 0 rgba(31,38,135,0.37);
        padding: 2rem;
        margin-bottom: 2rem;
        color: #fff;
        transition: all 0.3s ease;
        border: 1px solid rgba(255,255,255,0.18);
    }
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px 0 rgba(31,38,135,0.5);
    }
    /* Button styling */
    .stButton>button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.8rem 1.8rem;
        font-size: 1.1rem;
        font-weight: bold;
        transition: all 0.3s;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #764ba2 0%, #667eea 100%);
        transform: scale(1.05);
    }
    /* Header styling */
    .header {
        background: #2b6cb0;
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    /* Responsive columns */
    @media (max-width: 768px) {
        .column {width: 100% !important;}
    }
</style>
""", unsafe_allow_html=True)

# Hero Section (replaces colored_header)
st.markdown("""
<div class="header">
    <h1 style="color: white; margin: 0;">🏘️ Real Estate AI Suite</h1>
    <p style="margin: 0; opacity: 0.9;">Empowering your property journey with smart analytics, price predictions, and personalized recommendations.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="text-align: center; margin-bottom: 3rem;">
    <p style="font-size: 1.2rem; color: #cbd5e0;">
        Explore, predict, and discover your perfect property with cutting-edge AI.
    </p>
</div>
""", unsafe_allow_html=True)

# App Cards (no extra containers, just columns)
col1, col2, col3 = st.columns(3)

with col1:
    # st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("""
    <h2 style="color: #a3bffa;">📊 Analytics Dashboard</h2>
    <p style="color: #cbd5e0;">
        Visualize property trends, market insights, and sector-wise price distributions with interactive charts and maps.
    </p>
    """, unsafe_allow_html=True)
    if st.button("Explore Analytics", key="analytics"):
        st.switch_page("pages/Analysis_App.py")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    # st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("""
    <h2 style="color: #a3bffa;">🔮 Price Predictor</h2>
    <p style="color: #cbd5e0;">
        Get instant price estimates for any property based on location, size, amenities, and more.
    </p>
    """, unsafe_allow_html=True)
    if st.button("Predict Prices", key="predictor"):
        st.switch_page("pages/Price_Predictor.py")
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    # st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("""
    <h2 style="color: #a3bffa;">🤖 Recommender System</h2>
    <p style="color: #cbd5e0;">
        Discover properties similar to your favorites with our AI-powered recommendation engine.
    </p>
    """, unsafe_allow_html=True)
    if st.button("Find Recommendations", key="recommender"):
        st.switch_page("pages/Recommender.py")
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #cbd5e0; font-size: 0.9rem;">
    <p>Built with ❤️ by Dev | Powered by Streamlit</p>
</div>
""", unsafe_allow_html=True)
