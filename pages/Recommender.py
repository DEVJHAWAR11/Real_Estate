import streamlit as st
import pickle
import pandas as pd
import numpy as np
import os

st.set_page_config(
    page_title="Smart Property Advisor",
    page_icon="🏘️",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data()
def load_data():
    base_dir = os.path.dirname(__file__)
    recommender_dir = os.path.join(base_dir, 'Recommender_System')
    location_df = pd.read_pickle(os.path.join(recommender_dir, 'location_distance.pkl'))
    cosine_sim1 = pd.read_pickle(os.path.join(recommender_dir, 'cosine_sim1.pkl'))
    cosine_sim2 = pd.read_pickle(os.path.join(recommender_dir, 'cosine_sim2.pkl'))
    cosine_sim3 = pd.read_pickle(os.path.join(recommender_dir, 'cosine_sim3.pkl'))
    return location_df, cosine_sim1, cosine_sim2, cosine_sim3

location_df, cosine_sim1, cosine_sim2, cosine_sim3 = load_data()

def recommend_properties(property_name, top_n=5):
    try:
        cosine_sim_matrix = 0.5 * cosine_sim1 + 0.8 * cosine_sim2 + 1.0 * cosine_sim3
        sim_scores = list(enumerate(cosine_sim_matrix[location_df.index.get_loc(property_name)]))
        sorted_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:top_n + 1]

        recommendations = pd.DataFrame({
            'PropertyName': location_df.index[[i[0] for i in sorted_scores]],
            'Match Score': [f"{i[1]:.0%}" for i in sorted_scores],
            'Distance (km)': [location_df.iloc[i[0]][selected_location] / 1000 if selected_location in location_df.columns else np.nan for i in sorted_scores]
        })
        return recommendations
    except Exception as e:
        st.error(f"Error generating recommendations: {str(e)}")
        return pd.DataFrame()

# Header
st.title("🏘️ Smart Property Advisor")
st.caption("Discover your perfect home with AI-powered recommendations.")
st.divider()

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("📍 Location Finder")
    selected_location = st.selectbox(
        'Neighborhood',
        sorted(location_df.columns.to_list()),
        help="Choose your preferred area"
    )
    radius = st.slider('Max Distance (km)', min_value=1, max_value=20, value=5, step=1)

    if st.button('🔍 Search Properties', use_container_width=True):
        results = location_df[location_df[selected_location] < radius * 1000][selected_location].sort_values()
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

# Results
if 'search_results' in st.session_state:
    st.divider()
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
    st.divider()
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

# Sidebar
with st.sidebar:
    st.header("ℹ️ How It Works")
    st.markdown("""
    Recommendations use a **weighted cosine similarity** ensemble:
    - **Location features** — weight: 0.5
    - **Price features** — weight: 0.8
    - **Amenities & property features** — weight: 1.0
    """)
    st.divider()
    st.subheader("📊 Quick Stats")
    st.metric("Total Properties", len(location_df))
    st.metric("Recommendations per Query", "Top 5")
    st.divider()
    st.caption("💡 Tip: Use Location Finder first, then Smart Recommendations to find similar properties.")
