# Importing the required modules
import streamlit as st
import pandas as pd
from PIL import Image
import plotly.express as px

# Reading the CSV file
url_data = 'https://github.com/silviaazahro/Netflix-/raw/main/cleaned_data.csv'
df = pd.read_csv(url_data)

# Check for expected columns in the dataset
expected_columns = ['title', 'year', 'genre', 'rating', 'votes']
for col in expected_columns:
    if col not in df.columns:
        st.error(f"Column '{col}' not found in the dataset. Please check the dataset or update the code.")
        st.stop()

# Dashboard title
st.title("Netflix Streaming Dashboard 2024")

# Netflix logo
img = Image.open('Netflix_Logo.png')
st.sidebar.image(img)

# Sidebar for page selection
page = st.sidebar.selectbox("Choose The Page", ["Genre Distribution", "Most Streamed"])

if page == "Genre Distribution":
    # Displaying genre distribution
    st.subheader("Distribution of Genres")
    
    # Counting the occurrences of each genre
    genre_counts = df['genre'].value_counts().reset_index()
    genre_counts.columns = ['Genre', 'Count']
    
    # Visualization of genre distribution
    fig = px.pie(
        genre_counts,
        names='Genre',
        values='Count',
        title='Distribution of Genres on Netflix',
        color_discrete_sequence=px.colors.sequential.Plasma
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Displaying the genre counts table
    st.table(genre_counts)

elif page == "Most Streamed":
    # Most Streamed visualization options
    statistic_option = st.sidebar.selectbox(
        "Choose The Statistics",
        ["Top 10 Most Streamed", "Top 10 Most Popular", "Descriptive Statistics"]
    )

    if statistic_option == "Top 10 Most Streamed":
        # Sort by 'votes' (as a proxy for streaming count) and get the top 10 shows
        top_10_streamed = df.sort_values(by='votes', ascending=False).head(10)

        st.subheader("Top 10 Most 
