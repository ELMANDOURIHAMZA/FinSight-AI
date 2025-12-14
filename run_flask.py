"""
Script de démarrage pour l'application Flask
"""
import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from app import app

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('data/raw', exist_ok=True)
    os.makedirs('data/vector_db', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    os.makedirs('flask_session', exist_ok=True)
    
    print("=" * 50)
    print("FinSight AI - Agent Financier Autonome")
    print("Application Flask démarrée")
    print("=" * 50)
    print("\nAccédez à l'application sur: http://localhost:5000")
    print("Appuyez sur Ctrl+C pour arrêter\n")
    
    # Run Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)

