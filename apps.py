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

        st.subheader("Top 10 Most Streamed Netflix Shows 2024")
        
        # Visualization of the top 10 streamed shows
        fig = px.bar(
            top_10_streamed,
            x='votes',
            y='title',
            color='votes',
            color_continuous_scale='reds',
            title='Top 10 Most Streamed Netflix Shows 2024',
            labels={'votes': 'Votes', 'title': 'Show Title'},
            text='votes'
        )
        fig.update_layout(
            yaxis_title='Show Title',
            xaxis_title='Votes',
            yaxis=dict(
                tickmode='array',
                tickvals=top_10_streamed['title'],
                ticktext=[t if len(t) <= 50 else t[:47] + '...' for t in top_10_streamed['title']],
                autorange='reversed'
            ),
            xaxis=dict(tickformat=',')
        )
    
        # Adjusting y-axis to rotate labels
        fig.update_yaxes(tickangle=-45)
    
        st.plotly_chart(fig, use_container_width=True)
        
        # Displaying the top 10 shows table
        st.table(top_10_streamed[['title', 'genre', 'year', 'votes']].reset_index(drop=True))

    elif statistic_option == "Top 10 Most Popular":
        # Sort by 'rating' and get the top 10 shows
        top_10_popular = df.sort_values(by='rating', ascending=False).head(10)

        st.subheader("Top 10 Most Popular Netflix Shows 2024")
    
        # Visualization of the top 10 popular shows
        fig = px.bar(
            top_10_popular,
            x='rating',
            y='title',
            color='rating',
            color_continuous_scale='greens',
            title='Top 10 Most Popular Netflix Shows 2024',
            labels={'rating': 'Rating', 'title': 'Show Title'},
            text='rating'
        )
        fig.update_layout(
            xaxis_title='Rating',
            yaxis_title='Show Title',
            yaxis=dict(autorange='reversed')  # Reversing the y-axis to maintain order
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Displaying the top 10 shows table
        st.table(top_10_popular[['title', 'genre', 'year', 'rating']].reset_index(drop=True))

    elif statistic_option == "Descriptive Statistics":
        st.subheader("Descriptive Statistics")

        # Calculating descriptive statistics
        descriptive_stats = df[['rating', 'votes']].describe().transpose()
    
        # Displaying descriptive statistics
        st.write(descriptive_stats)

        # Displaying histogram distribution of 'votes' and 'rating'
        st.subheader("Distribution of Votes")
        fig_votes = px.histogram(df, x='votes', nbins=30, title='Distribution of Votes')
        st.plotly_chart(fig_votes, use_container_width=True)

        st.subheader("Distribution of Ratings")
        fig_ratings = px.histogram(df, x='rating', nbins=30, title='Distribution of Ratings')
        st.plotly_chart(fig_ratings, use_container_width=True)
