# 🎬 Movie Recommender System

A beautiful, **professional-grade** web application that recommends movies based on your favorite films using content-based filtering and cosine similarity.

---

## ✨ Features

- **Smart Search**: Autocomplete suggestions as you type movie titles
- **Content-Based Recommendations**: Uses movie overview, genres, keywords, cast, and crew
- **Modern, Responsive UI**: Professional design, smooth animations, and touch-friendly layout
- **Accessibility**: Keyboard navigation, focus outlines, and readable font sizes
- **Similarity Scores**: See how similar each recommendation is to your chosen movie
- **Real-time Results**: Get top 5 similar movies instantly

---

## 📸 Screenshots

> ![Screenshot Example](./screenshot.png)

- **Header with Icon**: Modern, branded look
- **Beautiful Cards**: Soft shadows, rounded corners, and smooth hover
- **Mobile-First**: Looks great on all devices

---

## 🗂️ Project Structure

```
Movie Recommendar/
├── backend.py              # Flask API server
├── requirements.txt        # Python dependencies
├── tmdb_5000_movies.csv   # Movie dataset
├── tmdb_5000_credits.csv  # Credits dataset
├── movieRecommendar.ipynb # Original Jupyter notebook
├── setup_nltk.py          # NLTK data downloader
├── start_app.py           # Easy startup script
└── Frontend/              # React frontend
    ├── src/
    │   ├── App.jsx        # Main React component
    │   └── App.css        # Styling (professional, responsive)
    └── package.json       # Node.js dependencies
```

---

## 🚀 Setup Instructions

### Prerequisites
- Python 3.8 or higher
- Node.js 16 or higher
- npm or yarn

### Backend Setup
1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Download NLTK data (required for text processing):**
   ```bash
   python setup_nltk.py
   ```
3. **Start the Flask backend:**
   ```bash
   python backend.py
   ```
   The backend will start on `http://localhost:5000`

### Frontend Setup
1. **Navigate to the Frontend directory:**
   ```bash
   cd Frontend
   ```
2. **Install Node.js dependencies:**
   ```bash
   npm install
   ```
3. **Start the React development server:**
   ```bash
   npm run dev
   ```
   The frontend will start on `http://localhost:5173`

### One-Click Startup (Recommended)
You can use the helper script to start both backend and frontend:
```bash
python start_app.py
```

---

## 🧑‍💻 How to Use

1. **Open your browser** and go to `http://localhost:5173`
2. **Search for a movie:**
   - Start typing a movie title in the search box
   - Select from the autocomplete suggestions
   - Or type the full movie name
3. **Get recommendations:**
   - Click "Get Recommendations" or press Enter
   - View the top 5 similar movies with similarity scores
4. **Explore recommendations:**
   - Each card shows the movie title and similarity percentage
   - Hover over cards for interactive effects

---

## 🖌️ Design & UX

- **Font:** Uses [Inter](https://fonts.google.com/specimen/Inter) for a modern, readable look
- **Header Icon:** 🎬 for instant recognition and branding
- **Professional Card Design:** Soft shadows, rounded corners, and smooth transitions
- **Mobile-First:** Fully responsive, touch-friendly, and easy to use on any device
- **Accessibility:**
  - Keyboard navigation and focus outlines
  - Good color contrast and readable font sizes
  - Touch targets are large and easy to use
- **Micro-interactions:** Smooth hover, focus, and click effects

---

## 🛠️ Technologies Used

### Backend
- **Flask**: Web framework for API
- **Pandas**: Data manipulation
- **Scikit-learn**: Machine learning (CountVectorizer, cosine_similarity)
- **NLTK**: Natural language processing (PorterStemmer)

### Frontend
- **React**: User interface framework
- **CSS3**: Modern styling with gradients, animations, and responsive design
- **Inter Font**: Clean, modern typography
- **Fetch API**: HTTP requests to backend

---

## 📊 Dataset

The system uses the TMDB 5000 Movies dataset:
- **tmdb_5000_movies.csv**: Movie metadata (4803 movies)
- **tmdb_5000_credits.csv**: Cast and crew information

---

## 🧩 API Endpoints
- `GET /api/movies` - Get all movies for autocomplete
- `GET /api/search?q=<query>` - Search movies by title
- `POST /api/recommend` - Get movie recommendations
- `GET /api/health` - Health check endpoint

---

## ⚙️ How It Works

### Content-Based Filtering
1. **Feature Extraction**: Combines movie overview, genres, keywords, cast, and crew
2. **Text Processing**: Applies stemming and removes stop words
3. **Vectorization**: Converts text to TF-IDF vectors using CountVectorizer
4. **Similarity Calculation**: Uses cosine similarity to find similar movies
5. **Ranking**: Returns top 5 most similar movies

### Data Processing
- **Genres**: Extracted from JSON format
- **Keywords**: Movie-specific tags and themes
- **Cast**: Top 3 actors from each movie
- **Crew**: Director information
- **Overview**: Movie plot description

---

## 🧑‍🤝‍🧑 Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

## 🪪 License
This project is open source and available under the MIT License. 