import streamlit as st
import pandas as pd
import plotly.express as px
import pickle
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import os

st.set_page_config(
    page_title="Real Estate Analytics",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title('🏠 Real Estate Analytics Dashboard')
st.caption("Explore property trends and market insights through interactive visualizations.")
st.divider()

@st.cache_data()
def load_data():
    base_dir = os.path.dirname(__file__)
    csv_path = os.path.join(base_dir, 'Analysis_datasets', 'data_viz1.csv')
    pkl_path = os.path.join(base_dir, 'Analysis_datasets', 'feature_text.pkl')
    new_df = pd.read_csv(csv_path)
    with open(pkl_path, 'rb') as f:
        feature_text = pickle.load(f)
    return new_df, feature_text

new_df, feature_text = load_data()

# Sidebar filters
with st.sidebar:
    st.header("🔍 Filters")
    price_range = st.slider(
        "Price Range (Cr)",
        min_value=int(new_df['price'].min()),
        max_value=int(new_df['price'].max()),
        value=(int(new_df['price'].min()), int(new_df['price'].max()))
    )
    sectors = st.multiselect(
        "Select Sectors",
        options=new_df['sector'].unique(),
    )

# Apply filters
filtered_df = new_df[
    (new_df['price'].between(price_range[0], price_range[1])) &
    (new_df['sector'].isin(sectors if sectors else new_df['sector'].unique()))
]

# Layout
col1, col2 = st.columns([3, 1])

with col1:
    with st.expander("🌍 Sector Price Distribution Map", expanded=True):
        group_df = filtered_df.groupby('sector').mean(numeric_only=True)[['price', 'price_per_sqft', 'built_up_area', 'latitude', 'longitude']]
        fig_map = px.scatter_mapbox(
            group_df,
            lat="latitude",
            lon="longitude",
            color="price_per_sqft",
            size='built_up_area',
            color_continuous_scale=px.colors.cyclical.IceFire,
            zoom=10,
            mapbox_style="carto-positron",
            width=1200,
            height=600,
            hover_name=group_df.index,
            title="Price per Sqft & Property Size Distribution"
        )
        fig_map.update_layout(margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig_map, use_container_width=True)

    st.subheader("📊 Property Type Insights")
    tab1, tab2, tab3 = st.tabs(["Area vs Price", "Price Distribution", "BHK Analysis"])

    with tab1:
        property_type = st.radio("Select Property Type", ['flat', 'house'], horizontal=True)
        fig_scatter = px.scatter(
            filtered_df[filtered_df['property_type'] == property_type],
            x="built_up_area",
            y="price",
            color="bedRoom",
            size="built_up_area",
            hover_name="sector",
            title=f"{property_type.title()} Pricing Dynamics",
            labels={'built_up_area': 'Built-up Area (sqft)', 'price': 'Price (₹)'}
        )
        fig_scatter.update_traces(marker=dict(opacity=0.7, line=dict(width=1, color='DarkSlateGrey')))
        st.plotly_chart(fig_scatter, use_container_width=True)

    with tab2:
        fig_dist = px.histogram(
            filtered_df,
            x="price",
            color="property_type",
            marginal="box",
            nbins=50,
            title="Price Distribution Comparison"
        )
        st.plotly_chart(fig_dist, use_container_width=True)

    with tab3:
        col_a, col_b = st.columns(2)
        with col_a:
            fig_pie = px.pie(
                filtered_df,
                names='bedRoom',
                hole=0.4,
                title="BHK Distribution"
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        with col_b:
            fig_box = px.box(
                filtered_df[filtered_df['bedRoom'] <= 4],
                x='bedRoom',
                y='price',
                color='property_type',
                title="BHK Price Comparison"
            )
            st.plotly_chart(fig_box, use_container_width=True)

with col2:
    with st.expander("📈 Feature Word Cloud", expanded=True):
        wordcloud = WordCloud(
            width=400,
            height=400,
            background_color='white',
            colormap='Blues',
            stopwords=set(['s'])
        ).generate(feature_text)
        plt.figure(figsize=(6, 6))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        st.pyplot(plt.gcf())

    with st.expander("📌 Key Statistics", expanded=True):
        st.metric("Total Properties", len(filtered_df))
        st.metric("Average Price", f"₹{filtered_df['price'].mean():,.0f}CR")
        st.metric("Avg Price/Sqft", f"₹{filtered_df['price_per_sqft'].mean():,.0f}")
        st.metric("Most Common BHK", filtered_df['bedRoom'].mode()[0])

st.divider()
st.caption("🔍 Hover over charts for tooltips · 🖱️ Click and drag to zoom · 🔄 Double-click to reset")
