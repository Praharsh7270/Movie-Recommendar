import { useState, useEffect } from 'react'
import './App.css'

function App() {
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedMovie, setSelectedMovie] = useState('')
  const [recommendations, setRecommendations] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [suggestions, setSuggestions] = useState([])
  const [showSuggestions, setShowSuggestions] = useState(false)

  const API_BASE_URL = 'http://localhost:5000/api'

  // Fetch movie suggestions as user types
  useEffect(() => {
    const fetchSuggestions = async () => {
      if (searchQuery.length < 2) {
        setSuggestions([])
        setShowSuggestions(false)
        return
      }

      try {
        const response = await fetch(`${API_BASE_URL}/search?q=${encodeURIComponent(searchQuery)}`)
        const data = await response.json()
        setSuggestions(data.movies || [])
        setShowSuggestions(true)
      } catch (err) {
        console.error('Error fetching suggestions:', err)
      }
    }

    const timeoutId = setTimeout(fetchSuggestions, 300)
    return () => clearTimeout(timeoutId)
  }, [searchQuery])

  const handleMovieSelect = (movie) => {
    setSelectedMovie(movie)
    setSearchQuery(movie)
    setShowSuggestions(false)
  }

  const handleRecommendations = async () => {
    if (!selectedMovie.trim()) {
      setError('Please select a movie first')
      return
    }

    setLoading(true)
    setError('')
    setRecommendations([])

    try {
      const response = await fetch(`${API_BASE_URL}/recommend`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ movie_title: selectedMovie }),
      })

      const data = await response.json()

      if (response.ok) {
        setRecommendations(data.recommendations || [])
      } else {
        setError(data.error || 'Failed to get recommendations')
      }
    } catch (err) {
      setError('Failed to connect to the recommendation service')
      console.error('Error:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleRecommendations()
    }
  }

  return (
    <div className="app">
      <div className="container">
        <header className="header">
          <h1 className="title">🎬 Movie Recommender</h1>
          <p className="subtitle">Discover your next favorite movie</p>
        </header>

        <div className="search-section">
          <div className="search-container">
            <input
              type="text"
              placeholder="Enter a movie title..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              onKeyPress={handleKeyPress}
              className="search-input"
            />
            <button 
              onClick={handleRecommendations}
              disabled={loading || !selectedMovie.trim()}
              className="search-button"
            >
              {loading ? 'Finding...' : 'Get Recommendations'}
            </button>
          </div>

          {showSuggestions && suggestions.length > 0 && (
            <div className="suggestions">
              {suggestions.map((movie, index) => (
                <div
                  key={index}
                  className="suggestion-item"
                  onClick={() => handleMovieSelect(movie)}
                >
                  {movie}
                </div>
              ))}
            </div>
          )}
        </div>

        {error && (
          <div className="error-message">
            {error}
          </div>
        )}

        {selectedMovie && (
          <div className="selected-movie">
            <h3>Selected Movie:</h3>
            <p className="movie-title">{selectedMovie}</p>
          </div>
        )}

        {recommendations.length > 0 && (
          <div className="recommendations-section">
            <h2>Recommended Movies</h2>
            <div className="recommendations-grid">
              {recommendations.map((movie, index) => (
                <div key={movie.movie_id} className="movie-card">
                  <div className="movie-number">{index + 1}</div>
                  <h3 className="movie-title">{movie.title}</h3>
                  <div className="similarity-score">
                    Similarity: {(movie.similarity_score * 100).toFixed(1)}%
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {loading && (
          <div className="loading">
            <div className="spinner"></div>
            <p>Finding similar movies...</p>
          </div>
        )}
      </div>
    </div>
  )
}

export default App
