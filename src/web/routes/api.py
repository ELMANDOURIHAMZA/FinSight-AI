"""
API routes for Flask application
"""
from flask import Blueprint, request, jsonify, session
import os
import sys
from pathlib import Path
import pandas as pd
import json

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from src.data.alpha_vantage import AlphaVantageClient
from src.data.sec_edgar import SecEdgarClient
from src.rag.ingestion import DocumentIngester
from src.rag.retrieval import AdvancedRAGRetriever
from src.agents.finance_agent import FinanceAgent
from llama_index.llms.gemini import Gemini
from llama_index.core.llms import LLM

bp = Blueprint('api', __name__, url_prefix='/api')

def initialize_llm(model_name: str = "gemini-2.0-flash-exp"):
    """Initialize LLM"""
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            return None
        
        # Ensure model name has 'models/' prefix
        if not model_name.startswith('models/'):
            model_name = f'models/{model_name}'
        
        llm = Gemini(api_key=api_key, model=model_name)
        return llm
    except Exception as e:
        print(f"Error initializing LLM: {e}")
        return None

@bp.route('/quote/<ticker>')
def get_quote(ticker):
    """Get stock quote"""
    try:
        client = AlphaVantageClient()
        quote = client.get_quote(ticker.upper())
        return jsonify(quote)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/overview/<ticker>')
def get_overview(ticker):
    """Get company overview"""
    try:
        client = AlphaVantageClient()
        overview = client.get_company_overview(ticker.upper())
        return jsonify(overview)
    except ValueError as e:
        return jsonify({'error': str(e), 'message': 'Vérifiez que votre clé Alpha Vantage API est configurée'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/timeseries/<ticker>')
def get_timeseries(ticker):
    """Get time series data"""
    try:
        client = AlphaVantageClient()
        df = client.get_time_series_daily(ticker.upper(), outputsize="compact")
        df = df.tail(100)  # Last 100 days
        
        # Convert to JSON (handle NaN values)
        data = {
            'dates': df.index.strftime('%Y-%m-%d').tolist(),
            'open': df['open'].fillna(0).tolist(),
            'high': df['high'].fillna(0).tolist(),
            'low': df['low'].fillna(0).tolist(),
            'close': df['close'].fillna(0).tolist(),
            'volume': df['volume'].fillna(0).tolist()
        }
        return jsonify(data)
    except ValueError as e:
        return jsonify({'error': str(e), 'message': 'Vérifiez que votre clé Alpha Vantage API est configurée'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/chart/price/<ticker>')
def get_price_chart(ticker):
    """Get price chart data"""
    try:
        client = AlphaVantageClient()
        df = client.get_time_series_daily(ticker.upper(), outputsize="compact")
        df = df.tail(100)
        
        # Calculate SMAs
        sma_20 = df['close'].rolling(window=20).mean()
        sma_50 = df['close'].rolling(window=50).mean()
        
        data = {
            'dates': df.index.strftime('%Y-%m-%d').tolist(),
            'close': df['close'].fillna(0).tolist(),
            'sma_20': sma_20.fillna(0).tolist(),
            'sma_50': sma_50.fillna(0).tolist()
        }
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/chart/rsi/<ticker>')
def get_rsi_chart(ticker):
    """Get RSI chart data"""
    try:
        client = AlphaVantageClient()
        df = client.get_time_series_daily(ticker.upper(), outputsize="compact")
        df = df.tail(100)
        
        # Calculate RSI
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        
        data = {
            'dates': df.index.strftime('%Y-%m-%d').tolist(),
            'rsi': rsi.fillna(50).tolist()
        }
        return jsonify(data)
    except ValueError as e:
        return jsonify({'error': str(e), 'message': 'Vérifiez que votre clé Alpha Vantage API est configurée'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/set-ticker', methods=['POST'])
def set_ticker():
    """Set ticker in session and optionally initialize RAG"""
    data = request.get_json()
    ticker = data.get('ticker', '').upper()
    initialize_rag = data.get('initialize_rag', False)
    
    session['ticker'] = ticker
    
    # Optionally initialize RAG system
    if initialize_rag and ticker:
        try:
            from src.web.routes.chat import initialize_rag_system, initialize_llm
            from src.agents.finance_agent import FinanceAgent
            
            # Initialize RAG
            retriever, _ = initialize_rag_system(ticker)
            
            # Initialize LLM
            llm = initialize_llm()
            if llm:
                # Create agent
                agent = FinanceAgent(
                    rag_retriever=retriever,
                    alpha_vantage_client=AlphaVantageClient(),
                    llm=llm,
                    verbose=False
                )
                
                # Cache agent
                from src.web.routes.chat import _agents_cache
                _agents_cache[ticker] = agent
                
                return jsonify({
                    'success': True, 
                    'ticker': ticker,
                    'rag_initialized': True
                })
        except Exception as e:
            # Continue even if RAG initialization fails
            return jsonify({
                'success': True, 
                'ticker': ticker,
                'rag_initialized': False,
                'warning': f'RAG initialization failed: {str(e)}'
            })
    
    return jsonify({'success': True, 'ticker': ticker})

@bp.route('/config', methods=['GET', 'POST'])
def config():
    """Get or update configuration"""
    if request.method == 'POST':
        data = request.get_json()
        # Store API keys in session (in production, use secure storage)
        if 'gemini_key' in data:
            session['gemini_key'] = data['gemini_key']
            os.environ['GEMINI_API_KEY'] = data['gemini_key']
        if 'alpha_key' in data:
            session['alpha_key'] = data['alpha_key']
            os.environ['ALPHA_VANTAGE_API_KEY'] = data['alpha_key']
        return jsonify({'success': True})
    else:
        return jsonify({
            'gemini_key': os.getenv('GEMINI_API_KEY', ''),
            'alpha_key': os.getenv('ALPHA_VANTAGE_API_KEY', ''),
            'ticker': session.get('ticker', '')
        })

