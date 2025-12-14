"""
Flask Application for FinSight AI - Agent Financier Autonome
"""
import os
import sys
from pathlib import Path
from flask import Flask, render_template, request, jsonify, session, send_from_directory
from flask_session import Session
from dotenv import load_dotenv
import json

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Load environment variables from project root .env explicitly so loading
# works even when Python is started from a different current working directory.
project_root = Path(__file__).parent
dotenv_path = project_root / '.env'
load_dotenv(dotenv_path=dotenv_path)

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
Session(app)

# Import routes
try:
    from src.web.routes import dashboard, api, chat
    
    # Register blueprints
    app.register_blueprint(dashboard.bp)
    app.register_blueprint(api.bp)
    app.register_blueprint(chat.bp)
except ImportError as e:
    print(f"Warning: Could not import routes: {e}")
    print("Routes will be registered when modules are available")

@app.route('/')
def index():
    """Redirect to dashboard"""
    from flask import redirect, url_for
    return redirect(url_for('dashboard.dashboard'))

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('data/raw', exist_ok=True)
    os.makedirs('data/vector_db', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    
    # Run Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)

