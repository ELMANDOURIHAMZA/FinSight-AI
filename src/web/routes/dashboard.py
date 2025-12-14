"""
Dashboard routes for Flask application
"""
from flask import Blueprint, render_template, request, session, jsonify
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from src.data.alpha_vantage import AlphaVantageClient
from src.data.sec_edgar import SecEdgarClient

bp = Blueprint('dashboard', __name__)

@bp.route('/dashboard')
def dashboard():
    """Main dashboard page"""
    # Get ticker from session or default
    ticker = session.get('ticker', 'AAPL')
    
    # Initialize clients
    try:
        alpha_client = AlphaVantageClient()
        has_alpha_key = True
    except:
        alpha_client = None
        has_alpha_key = False
    
    return render_template(
        'dashboard.html',
        ticker=ticker,
        has_alpha_key=has_alpha_key
    )


@bp.route('/documents')
def documents():
    """Document explorer page"""
    ticker = session.get('ticker', '')
    return render_template('documents.html', ticker=ticker)

