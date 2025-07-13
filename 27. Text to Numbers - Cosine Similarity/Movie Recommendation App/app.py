import streamlit as st
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import utility  # Ensure utility contains the preprocessing function


# Page configuration
st.set_page_config(
    page_title="CineMatch - Movie Recommendation Engine",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    /* Main container styling */
    .main > div {
        padding-top: 2rem;
    }
    
    /* Header styling */
    .main-header {
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 3rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    
    .main-header h1 {
        font-size: 3rem;
        margin-bottom: 0.5rem;
        font-weight: 700;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        font-size: 1.2rem;
        opacity: 0.9;
        margin: 0;
    }
    
    /* Selection container */
    .selection-container {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        margin-bottom: 3rem;
        border: 1px solid #e1e8ed;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 50px;
        font-weight: 600;
        font-size: 1rem;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    /* Selectbox styling */
    .stSelectbox > div > div > div {
        border-radius: 10px;
        border: 2px solid #e1e8ed;
        font-size: 1rem;
    }
    
    /* Results section */
    .results-header {
        text-align: center;
        margin: 3rem 0 2rem 0;
        padding: 1.5rem;
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }
    
    .results-header h2 {
        font-size: 2rem;
        margin: 0;
        font-weight: 600;
    }
    
    /* Movie card container */
    .movie-container {
        margin: 0.5rem;
        position: relative;
    }
    
    /* Hide default streamlit elements */
    .element-container:has(.movie-info) {
        display: none;
    }
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 2rem;
        }
        
        .main-header p {
            font-size: 1rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Load and preprocess data
@st.cache_data
def load_data():
    """Load and preprocess movie data for recommendations"""
    try:
        movie_data = pd.read_csv('imdb_top_1000.csv')
        data = movie_data[['Overview', 'Director', 'Genre', 'Star1', 'Poster_Link']]
        data['combined_info'] = data.apply(lambda x: ' '.join(x.astype(str)), axis=1)
        data['combined_info'] = data['combined_info'].apply(utility.preprocess_text)
        
        tf = TfidfVectorizer(ngram_range=(1,2), max_features=10000, stop_words='english')
        tf_idf_matrix = tf.fit_transform(data['combined_info'])
        doc_sim_df = pd.DataFrame(cosine_similarity(tf_idf_matrix))
        
        return movie_data, doc_sim_df
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None, None

def movie_recommender(movie_title, movie_data, doc_sims, num_movies=10):
    """Generate movie recommendations based on content similarity"""
    try:
        movies = movie_data['Series_Title'].values
        movie_idx = np.where(movies == movie_title)[0][0]
        movie_similarities = doc_sims.iloc[movie_idx].values
        similar_movie_idxs = np.argsort(-movie_similarities)[1:num_movies+1]
        similar_movies = movie_data.iloc[similar_movie_idxs]
        return similar_movies
    except Exception as e:
        st.error(f"Error generating recommendations: {str(e)}")
        return pd.DataFrame()

def display_movie_card(movie, key_suffix=""):
    """Display a movie card using Streamlit components"""
    # Handle missing values
    title = str(movie.get('Series_Title', 'Unknown Title'))
    year = str(movie.get('Released_Year', 'N/A'))
    rating = str(movie.get('IMDB_Rating', 'N/A'))
    director = str(movie.get('Director', 'Unknown Director'))
    genre = str(movie.get('Genre', 'Unknown Genre'))
    overview = str(movie.get('Overview', 'No overview available'))
    runtime = str(movie.get('Runtime', 'N/A'))
    poster_url = str(movie.get('Poster_Link', ''))
    
    # Get stars
    stars = []
    for i in range(1, 5):
        star = movie.get(f'Star{i}', '')
        if star and str(star) != 'nan':
            stars.append(str(star))
    stars_text = ", ".join(stars) if stars else "N/A"
    
    # Truncate overview
    overview_short = overview[:150] + "..." if len(overview) > 150 else overview
    
    # Create container for the movie card
    with st.container():
        # Display poster image with error handling
        try:
            if poster_url and poster_url != 'nan':
                st.image(poster_url, width=200, use_container_width=True)
            else:
                st.image("https://via.placeholder.com/300x450/cccccc/666666?text=No+Image", 
                        width=200, use_container_width=True)
        except:
            st.image("https://via.placeholder.com/300x450/cccccc/666666?text=No+Image", 
                    width=200, use_container_width=True)
        
        # Movie title
        st.markdown(f"**{title}**")
        
        # Create expander for movie details
        with st.expander("📋 Movie Details", expanded=False):
            st.markdown(f"**🗓️ Year:** {year}")
            st.markdown(f"**⭐ Rating:** {rating}/10")
            st.markdown(f"**🎬 Director:** {director}")
            st.markdown(f"**🎭 Genre:** {genre}")
            st.markdown(f"**⏱️ Runtime:** {runtime}")
            st.markdown(f"**🌟 Stars:** {stars_text}")
            st.markdown(f"**📝 Overview:** {overview_short}")
        
        # Quick info below poster
        st.markdown(f"<div style='text-align: center; color: #7f8c8d; font-size: 0.9rem;'>{year} • ⭐ {rating}</div>", 
                   unsafe_allow_html=True)

# Main app
def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🎬 CineMatch</h1>
        <p>Discover your next favorite movie with AI-powered recommendations</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load data
    with st.spinner("Loading movie database..."):
        movie_data, doc_sim_df = load_data()
    
    if movie_data is None:
        st.error("Failed to load movie data. Please check your data file.")
        return
    
    # Movie selection section
    st.markdown('<div class="selection-container">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### 🔍 Select a Movie")
        selected_movie = st.selectbox(
            'Choose a movie you enjoyed:',
            movie_data['Series_Title'].values,
            help="Select a movie to get personalized recommendations based on similar content"
        )
        
        recommend_button = st.button('🎯 Get Recommendations', use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Recommendations section
    if recommend_button:
        with st.spinner("Analyzing movie preferences and generating recommendations..."):
            recommended_movies = movie_recommender(
                selected_movie, 
                movie_data, 
                doc_sims=doc_sim_df, 
                num_movies=10
            )
        
        if not recommended_movies.empty:
            st.markdown(f"""
            <div class="results-header">
                <h2>🎬 Movies Similar to "{selected_movie}"</h2>
            </div>
            """, unsafe_allow_html=True)
            
            # Display movies in rows of 5
            for i in range(0, min(10, len(recommended_movies)), 5):
                cols = st.columns(5)
                
                for j, col in enumerate(cols):
                    movie_idx = i + j
                    if movie_idx < len(recommended_movies):
                        with col:
                            movie = recommended_movies.iloc[movie_idx]
                            display_movie_card(movie, key_suffix=f"_{movie_idx}")
            
            # Additional information
            st.markdown("---")
            st.markdown("""
            <div style="text-align: center; color: #7f8c8d; font-style: italic; margin-top: 2rem;">
                💡 Click on "📋 Movie Details" under each poster to see comprehensive information including cast, director, genre, and plot overview
            </div>
            """, unsafe_allow_html=True)
            
            # Show similarity scores
            st.markdown("### 📊 Recommendation Scores")
            similarity_data = []
            movies = movie_data['Series_Title'].values
            selected_idx = np.where(movies == selected_movie)[0][0]
            similarities = doc_sim_df.iloc[selected_idx].values
            
            for idx in range(len(recommended_movies)):
                movie_title = recommended_movies.iloc[idx]['Series_Title']
                movie_idx = np.where(movies == movie_title)[0][0]
                similarity_score = similarities[movie_idx]
                similarity_data.append({
                    'Movie': movie_title,
                    'Similarity Score': f"{similarity_score:.3f}",
                    'Match Percentage': f"{similarity_score * 100:.1f}%"
                })
            
            similarity_df = pd.DataFrame(similarity_data)
            st.dataframe(similarity_df, use_container_width=True)
            
        else:
            st.error("No recommendations could be generated. Please try selecting a different movie.")

if __name__ == "__main__":
    main()