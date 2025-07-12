from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
import ast
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import os

app = Flask(__name__)
CORS(app)

# Global variables to store the model and data
movies_df = None
similarity_matrix = None
ps = PorterStemmer()

def convert(obj):
    """Convert JSON string to list of names"""
    L = []
    for i in ast.literal_eval(obj):
        L.append(i['name'])
    return L

def convert2(obj):
    """Convert JSON string to list of top 3 cast names"""
    L = []
    counter = 0
    for i in ast.literal_eval(obj):
        if counter != 3:
            L.append(i['name'])
            counter += 1
        else: 
            break
    return L

def fetch_director(obj):
    """Extract director name from crew JSON"""
    L = []
    for i in ast.literal_eval(obj):
        if i['job'] == 'Director':
            L.append(i['name'])
            break
    return L

def stem(text):
    """Apply stemming to text"""
    y = []
    for i in text.split():
        y.append(ps.stem(i))
    return " ".join(y)

def load_and_prepare_data():
    """Load and prepare the movie data for recommendations"""
    global movies_df, similarity_matrix
    
    # Load the CSV files
    movies = pd.read_csv("tmdb_5000_movies.csv")
    credits = pd.read_csv("tmdb_5000_credits.csv")
    
    # Merge the datasets
    movies = movies.merge(credits, on="title")
    
    # Select relevant columns
    movies = movies[['movie_id','title','overview','genres','keywords','cast','crew']]
    # Ensure movies is a DataFrame
    movies = pd.DataFrame(movies)
    # Drop null values
    movies.dropna(inplace=True)

    # Ensure all columns are pandas Series (not numpy arrays)
    for col in ['genres', 'keywords', 'cast', 'crew', 'overview']:
        if not isinstance(movies[col], pd.Series):
            movies[col] = pd.Series(movies[col])

    # Convert JSON strings to lists
    movies['genres'] = movies['genres'].apply(convert)
    movies['keywords'] = movies['keywords'].apply(convert)
    movies['cast'] = movies['cast'].apply(convert2)
    movies['crew'] = movies['crew'].apply(fetch_director)
    # Convert overview to list of words
    movies['overview'] = movies['overview'].apply(lambda x: x.split())
    # Remove spaces from tags
    movies['genres'] = movies['genres'].apply(lambda x: [i.replace(" ", "") for i in x])
    movies['keywords'] = movies['keywords'].apply(lambda x: [i.replace(" ", "") for i in x])
    movies['cast'] = movies['cast'].apply(lambda x: [i.replace(" ", "") for i in x])
    movies['crew'] = movies['crew'].apply(lambda x: [i.replace(" ", "") for i in x])
    # Combine all tags
    movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']
    # Create new dataframe with only necessary columns
    new_df = movies[['movie_id','title','tags']]
    new_df = pd.DataFrame(new_df)
    # Convert tags to string and lowercase
    new_df['tags'] = new_df['tags'].apply(lambda x: " ".join(x))
    new_df['tags'] = new_df['tags'].apply(lambda x: x.lower())
    # Apply stemming
    new_df['tags'] = new_df['tags'].apply(stem)
    # Ensure new_df is a DataFrame
    new_df = pd.DataFrame(new_df)
    # Create vectors using CountVectorizer
    cv = CountVectorizer(max_features=5000, stop_words='english')
    vectors = cv.fit_transform(new_df['tags']).toarray()
    # Calculate similarity matrix
    similarity_matrix = cosine_similarity(vectors)
    # Store the processed dataframe
    global movies_df
    movies_df = new_df
    return True

@app.route('/api/movies', methods=['GET'])
def get_movies():
    """Get list of all movies for autocomplete"""
    global movies_df
    if movies_df is None or not isinstance(movies_df, pd.DataFrame):
        return jsonify({"error": "Data not loaded"}), 500
    movies_list = movies_df['title'].tolist()
    return jsonify({"movies": movies_list})

@app.route('/api/recommend', methods=['POST'])
def recommend_movies():
    """Get movie recommendations"""
    global movies_df, similarity_matrix
    if movies_df is None or similarity_matrix is None or not isinstance(movies_df, pd.DataFrame):
        return jsonify({"error": "Data not loaded"}), 500
    data = request.get_json()
    movie_title = data.get('movie_title', '').strip()
    if not movie_title:
        return jsonify({"error": "Movie title is required"}), 400
    try:
        # Find movie index
        movie_index = movies_df[movies_df['title'] == movie_title].index[0]
        # Get similarity scores
        distances = similarity_matrix[movie_index]
        # Get top 5 similar movies (excluding the movie itself)
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
        # Get movie details
        recommendations = []
        for i in movies_list:
            movie_info = {
                "title": movies_df.iloc[i[0]]['title'],
                "movie_id": int(movies_df.iloc[i[0]]['movie_id']),
                "similarity_score": float(i[1])
            }
            recommendations.append(movie_info)
        return jsonify({
            "input_movie": movie_title,
            "recommendations": recommendations
        })
    except IndexError:
        return jsonify({"error": f"Movie '{movie_title}' not found in database"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/search', methods=['GET'])
def search_movies():
    """Search movies by title"""
    global movies_df
    if movies_df is None or not isinstance(movies_df, pd.DataFrame):
        return jsonify({"error": "Data not loaded"}), 500
    query = request.args.get('q', '').strip()
    if not query:
        return jsonify({"movies": []})
    # Filter movies that contain the query (case insensitive)
    filtered_movies = movies_df[movies_df['title'].str.contains(query, case=False, na=False)]
    movies_list = filtered_movies['title'].tolist()[:10]  # Limit to 10 results
    return jsonify({"movies": movies_list})

@app.route('/api/health', methods=['GET'])
def health_check():
    global movies_df
    return jsonify({"status": "healthy", "data_loaded": movies_df is not None})

if __name__ == '__main__':
    print("Loading movie data...")
    success = load_and_prepare_data()
    if success and movies_df is not None:
        print("Data loaded successfully!")
        print(f"Loaded {len(movies_df)} movies")
    else:
        print("Failed to load data!")
    app.run(debug=True, host='0.0.0.0', port=5000) 