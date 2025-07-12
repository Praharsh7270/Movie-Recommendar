import subprocess
import sys
import os
import time
import webbrowser
from threading import Thread

def run_backend():
    """Run the Flask backend server"""
    print("🚀 Starting Flask backend...")
    try:
        subprocess.run([sys.executable, "backend.py"], check=True)
    except KeyboardInterrupt:
        print("\n⚠️  Backend stopped by user")
    except Exception as e:
        print(f"❌ Error starting backend: {e}")

def run_frontend():
    """Run the React frontend"""
    print("🎨 Starting React frontend...")
    try:
        os.chdir("Frontend")
        subprocess.run(["npm", "run", "dev"], check=True)
    except KeyboardInterrupt:
        print("\n⚠️  Frontend stopped by user")
    except Exception as e:
        print(f"❌ Error starting frontend: {e}")

def main():
    print("🎬 Movie Recommender System")
    print("=" * 40)
    
    # Check if required files exist
    if not os.path.exists("tmdb_5000_movies.csv"):
        print("❌ Error: tmdb_5000_movies.csv not found!")
        print("Please ensure the CSV files are in the project root directory.")
        return
    
    if not os.path.exists("tmdb_5000_credits.csv"):
        print("❌ Error: tmdb_5000_credits.csv not found!")
        print("Please ensure the CSV files are in the project root directory.")
        return
    
    # Check if Frontend directory exists
    if not os.path.exists("Frontend"):
        print("❌ Error: Frontend directory not found!")
        print("Please ensure the React frontend is properly set up.")
        return
    
    print("📋 Prerequisites check passed!")
    print("\n🔧 Setup Instructions:")
    print("1. Install Python dependencies: pip install -r requirements.txt")
    print("2. Install NLTK data: python setup_nltk.py")
    print("3. Install Node.js dependencies: cd Frontend && npm install")
    print("4. Run this script again to start both servers")
    print("\n" + "=" * 40)
    
    # Ask user if they want to start the servers
    response = input("Do you want to start the servers now? (y/n): ").lower().strip()
    
    if response in ['y', 'yes']:
        print("\n🔄 Starting servers...")
        
        # Start backend in a separate thread
        backend_thread = Thread(target=run_backend)
        backend_thread.daemon = True
        backend_thread.start()
        
        # Wait a bit for backend to start
        time.sleep(3)
        
        # Start frontend in a separate thread
        frontend_thread = Thread(target=run_frontend)
        frontend_thread.daemon = True
        frontend_thread.start()
        
        # Wait a bit for frontend to start
        time.sleep(5)
        
        # Open browser
        print("\n🌐 Opening browser...")
        webbrowser.open("http://localhost:5173")
        
        print("\n✅ Both servers are running!")
        print("📱 Frontend: http://localhost:5173")
        print("🔧 Backend: http://localhost:5000")
        print("\nPress Ctrl+C to stop both servers")
        
        try:
            # Keep the main thread alive
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Stopping servers...")
            sys.exit(0)
    
    else:
        print("\n📖 Manual startup instructions:")
        print("1. Start backend: python backend.py")
        print("2. Start frontend: cd Frontend && npm run dev")
        print("3. Open browser to: http://localhost:5173")

if __name__ == "__main__":
    main() 