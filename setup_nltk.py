import nltk

def download_nltk_data():
    """Download required NLTK data for the movie recommender"""
    print("Downloading NLTK data...")
    
    try:
        # Download punkt tokenizer (required for text processing)
        nltk.download('punkt')
        print("✓ Successfully downloaded NLTK punkt tokenizer")
        
        # Download stopwords (optional, for better text processing)
        nltk.download('stopwords')
        print("✓ Successfully downloaded NLTK stopwords")
        
        print("\nNLTK data setup complete! You can now run the backend.")
        
    except Exception as e:
        print(f"Error downloading NLTK data: {e}")
        print("Please try running this script again or download manually.")

if __name__ == "__main__":
    download_nltk_data() 