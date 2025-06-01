import streamlit as st
import pickle
import pandas as pd
import numpy as np

# Configure page settings first
st.set_page_config(
    page_title="Smart Property Advisor",
    page_icon="🏘️",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data
def load_data():
    location_df = pd.read_pickle('C:/Users/KIIT0001/Desktop/Campusx_Project/Real_Estate/pages/Recommender_System/location_distance.pkl')
    cosine_sim1 = pd.read_pickle('C:/Users/KIIT0001/Desktop/Campusx_Project/Real_Estate/pages/Recommender_System/cosine_sim1.pkl')
    cosine_sim2 = pd.read_pickle('C:/Users/KIIT0001/Desktop/Campusx_Project/Real_Estate/pages/Recommender_System/cosine_sim2.pkl')
    cosine_sim3 = pd.read_pickle('C:/Users/KIIT0001/Desktop/Campusx_Project/Real_Estate/pages/Recommender_System/cosine_sim3.pkl')
    return location_df, cosine_sim1, cosine_sim2, cosine_sim3

location_df, cosine_sim1, cosine_sim2, cosine_sim3 = load_data()

# Custom CSS for better styling
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
    
    .highlight {
        padding: 12px;
        border-radius: 8px;
        background: #ffffff;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 12px 0;
    }
    .stProgress > div > div > div > div {
        background-color: #4a90e2;
    }
</style>
""", unsafe_allow_html=True)

def recommend_properties(property_name, top_n=5):
    try:
        cosine_sim_matrix = 0.5 * cosine_sim1 + 0.8 * cosine_sim2 + 1 * cosine_sim3
        sim_scores = list(enumerate(cosine_sim_matrix[location_df.index.get_loc(property_name)]))
        sorted_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:top_n + 1]
        
        recommendations = pd.DataFrame({
            'PropertyName': location_df.index[[i[0] for i in sorted_scores]],
            'Match Score': [f"{i[1]:.0%}" for i in sorted_scores],
            'Distance (km)': [location_df.iloc[i[0]][selected_location]/1000 if selected_location in location_df.columns else np.nan for i in sorted_scores]
        })
        
        return recommendations
    except Exception as e:
        st.error(f"Error generating recommendations: {str(e)}")
        return pd.DataFrame()

# Main Content
st.title("🏘️ Smart Property Advisor")
st.markdown("Discover your perfect home with AI-powered recommendations")
st.markdown("---")

# Split into two main columns
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("📍 Location Finder")
    with st.container():
        selected_location = st.selectbox(
            'Select Neighborhood',
            sorted(location_df.columns.to_list()),
            help="Choose your preferred area"
        )
        
        radius = st.slider(
            'Maximum Commute Distance (km)',
            min_value=1,
            max_value=20,
            value=5,
            step=1,
            format="%d km"
        )
        
        if st.button('🔍 Search Properties', use_container_width=True):
            results = location_df[location_df[selected_location] < radius*1000][selected_location].sort_values()
            st.session_state.search_results = results.reset_index(name='Distance') \
                .rename(columns={'index': 'Property', 'Distance': 'Distance (meters)'})

with col2:
    st.subheader("🤖 Smart Recommendations")
    selected_property = st.selectbox(
        'Select a Property',
        sorted(location_df.index.to_list()),
        help="Choose a property to find similar options"
    )
    
    if st.button('✨ Generate Recommendations', use_container_width=True):
        st.session_state.recommendations = recommend_properties(selected_property)

# Display Results
if 'search_results' in st.session_state:
    st.subheader(f"📌 Properties within {radius} km of {selected_location}")
    results = st.session_state.search_results.copy()
    results['Distance (km)'] = results['Distance (meters)'] / 1000
    
    st.dataframe(
        results[['PropertyName', 'Distance (km)']],
        use_container_width=True,
        column_config={
            "PropertyName": st.column_config.TextColumn(width="large"),
            "Distance (km)": st.column_config.ProgressColumn(
                format="%.2f km",
                min_value=0,
                max_value=radius
            )
        },
        hide_index=True
    )

if 'recommendations' in st.session_state:
    st.subheader("🎯 Recommended Matches")
    if not st.session_state.recommendations.empty:
        st.dataframe(
            st.session_state.recommendations,
            use_container_width=True,
            column_config={
                "Match Score": st.column_config.ProgressColumn(
                    format="%s",
                    min_value=0,
                    max_value=1,
                    help="Similarity score combining location, price, and amenities"
                )
            },
            hide_index=True
        )
    else:
        st.warning("No similar properties found. Try adjusting your search criteria.")

# Sidebar with additional info
with st.sidebar:
    st.header("ℹ️ How It Works")
    st.markdown("""
    Our AI-powered recommender considers:
    - **Location Proximity** (50% weight)
    - **Price Similarity** (80% weight)
    - **Amenities Match** (100% weight)
    
    Recommendations are sorted by overall match score.
    """)
    
    st.markdown("---")
    st.subheader("📊 Quick Stats")
    st.metric("Total Properties", len(location_df))
    st.metric("Average Recommendations", "5-10 options")
    
    st.markdown("---")
    st.markdown("💡 **Tip:** Use the filters to narrow down properties based on your daily commute needs and preferred amenities.")
