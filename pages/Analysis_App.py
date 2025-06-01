import streamlit as st
import pandas as pd
import plotly.express as px
import pickle
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns

# Configuration
st.set_page_config(
    page_title="Real Estate Analytics Dashboard",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

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

# Custom CSS
st.markdown("""
    <style>
        .main {background-color: #f5f5f5;}
        .stSelectbox:first-child {width: 300px;}
        .stPlotlyChart {border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);}
        .css-1vq4p4l {padding: 2rem;}
        [data-testid="stHeader"] {background-color: #003366;}
    </style>
""", unsafe_allow_html=True)

# Title and description
st.title('🏠 Real Estate Analytics Dashboard')
st.markdown("Explore property trends and market insights through interactive visualizations.")

# Cache data loading
@st.cache_data
def load_data():
    new_df = pd.read_csv('C:/Users/KIIT0001/Desktop/Campusx_Project/Real_Estate/pages/Analysis_datasets/data_viz1.csv')
    feature_text = pickle.load(open('C:/Users/KIIT0001/Desktop/Campusx_Project/Real_Estate/pages/Analysis_datasets/feature_text.pkl','rb'))
    return new_df, feature_text

new_df, feature_text = load_data()

# Sidebar filters
with st.sidebar:
    st.header("🔍 Filters")
    price_range = st.slider(
        "Select Price Range (Cr)",
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

# Main columns layout
col1, col2 = st.columns([3, 1])

with col1:
    # Interactive Map
    with st.expander("🌍 Sector Price Distribution Map", expanded=True):
        group_df = filtered_df.groupby('sector').mean(numeric_only=True)[['price','price_per_sqft','built_up_area','latitude','longitude']]
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
            title="<b>Price per Sqft & Property Size Distribution</b>"
        )
        fig_map.update_layout(margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig_map, use_container_width=True)

    # Property Type Analysis
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
            title=f"<b>{property_type.title()} Pricing Dynamics</b>",
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
            title="<b>Price Distribution Comparison</b>"
        )
        st.plotly_chart(fig_dist, use_container_width=True)

    with tab3:
        col_a, col_b = st.columns(2)
        with col_a:
            fig_pie = px.pie(
                filtered_df,
                names='bedRoom',
                hole=0.4,
                title="<b>BHK Distribution</b>"
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        with col_b:
            fig_box = px.box(
                filtered_df[filtered_df['bedRoom'] <= 4],
                x='bedRoom',
                y='price',
                color='property_type',
                title="<b>BHK Price Comparison</b>"
            )
            st.plotly_chart(fig_box, use_container_width=True)

with col2:
    # Word Cloud
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

    # Quick Stats
    with st.expander("📌 Key Statistics", expanded=True):
        st.metric("Total Properties", len(filtered_df))
        st.metric("Average Price", f"₹{filtered_df['price'].mean():,.0f}CR")
        st.metric("Avg Price/Sqft", f"₹{filtered_df['price_per_sqft'].mean():,.0f}")
        st.metric("Most Common BHK", filtered_df['bedRoom'].mode()[0])

# Footer
st.markdown("---")
st.markdown("🔍 *Hover over charts for detailed tooltips* | 🖱️ *Click and drag to zoom* | 🔄 *Double-click to reset view*")





