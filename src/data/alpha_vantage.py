"""
Alpha Vantage API Client with rate limiting and caching
"""
import time
import json
import os
from functools import wraps
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import requests
import pandas as pd


def rate_limited(max_per_minute: int = 5):
    """
    Decorator to limit API calls per minute
    """
    min_interval = 60.0 / max_per_minute
    last_called = [0.0]

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            if elapsed < min_interval:
                time.sleep(min_interval - elapsed)
            ret = func(*args, **kwargs)
            last_called[0] = time.time()
            return ret
        return wrapper
    return decorator


class AlphaVantageClient:
    """
    Client for Alpha Vantage API with rate limiting and caching
    """
    
    BASE_URL = "https://www.alphavantage.co/query"
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("ALPHA_VANTAGE_API_KEY")
        if not self.api_key:
            raise ValueError("ALPHA_VANTAGE_API_KEY must be set")
        self.cache_dir = "data/raw"
        os.makedirs(self.cache_dir, exist_ok=True)
    
    def _get_cache_path(self, symbol: str, function: str) -> str:
        """Generate cache file path"""
        today = datetime.now().strftime("%Y-%m-%d")
        return os.path.join(self.cache_dir, f"{symbol}_{function}_{today}.json")
    
    def _load_from_cache(self, cache_path: str) -> Optional[Dict]:
        """Load data from cache if it exists and is from today"""
        if os.path.exists(cache_path):
            try:
                with open(cache_path, 'r') as f:
                    return json.load(f)
            except Exception:
                return None
        return None
    
    def _save_to_cache(self, cache_path: str, data: Dict):
        """Save data to cache"""
        try:
            with open(cache_path, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save cache: {e}")
    
    @rate_limited(max_per_minute=5)
    def _make_request(self, params: Dict) -> Dict:
        """Make API request with rate limiting"""
        params['apikey'] = self.api_key
        try:
            response = requests.get(self.BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Check for API errors
            if "Error Message" in data:
                raise ValueError(f"Alpha Vantage API Error: {data['Error Message']}")
            if "Note" in data:
                raise ValueError(f"Alpha Vantage API Rate Limit: {data['Note']}")
            
            return data
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Failed to connect to Alpha Vantage: {e}")
    
    def get_quote(self, symbol: str) -> Dict:
        """
        Get real-time quote for a symbol
        Returns: {symbol, price, volume, timestamp}
        """
        cache_path = self._get_cache_path(symbol, "quote")
        cached = self._load_from_cache(cache_path)
        if cached:
            return cached
        
        params = {
            'function': 'GLOBAL_QUOTE',
            'symbol': symbol.upper()
        }
        
        data = self._make_request(params)
        
        if 'Global Quote' not in data:
            raise ValueError(f"No quote data found for {symbol}")
        
        quote = data['Global Quote']
        result = {
            'symbol': quote.get('01. symbol'),
            'price': float(quote.get('05. price', 0)),
            'volume': int(quote.get('06. volume', 0)),
            'change': float(quote.get('09. change', 0)),
            'change_percent': quote.get('10. change percent', '0%'),
            'timestamp': datetime.now().isoformat()
        }
        
        self._save_to_cache(cache_path, result)
        return result
    
    def get_time_series_daily(self, symbol: str, outputsize: str = "compact") -> pd.DataFrame:
        """
        Get daily time series data
        Returns: DataFrame with columns [date, open, high, low, close, volume]
        """
        cache_path = self._get_cache_path(symbol, "timeseries")
        cached = self._load_from_cache(cache_path)
        if cached and 'Time Series (Daily)' in cached:
            # Convert cached data to DataFrame
            time_series = cached['Time Series (Daily)']
            df = pd.DataFrame.from_dict(time_series, orient='index')
            df.index = pd.to_datetime(df.index)
            df.columns = ['open', 'high', 'low', 'close', 'volume']
            df = df.astype(float)
            df = df.sort_index()
            return df
        
        params = {
            'function': 'TIME_SERIES_DAILY',
            'symbol': symbol.upper(),
            'outputsize': outputsize
        }
        
        data = self._make_request(params)
        
        if 'Time Series (Daily)' not in data:
            raise ValueError(f"No time series data found for {symbol}")
        
        time_series = data['Time Series (Daily)']
        df = pd.DataFrame.from_dict(time_series, orient='index')
        df.index = pd.to_datetime(df.index)
        df.columns = ['open', 'high', 'low', 'close', 'volume']
        df = df.astype(float)
        df = df.sort_index()
        
        # Save to cache
        self._save_to_cache(cache_path, data)
        return df
    
    def get_company_overview(self, symbol: str) -> Dict:
        """
        Get company overview (fundamentals)
        Returns: Company information including PE ratio, market cap, etc.
        """
        cache_path = self._get_cache_path(symbol, "overview")
        cached = self._load_from_cache(cache_path)
        if cached:
            return cached
        
        params = {
            'function': 'OVERVIEW',
            'symbol': symbol.upper()
        }
        
        data = self._make_request(params)
        
        if not data or 'Symbol' not in data:
            raise ValueError(f"No overview data found for {symbol}")
        
        # Extract key metrics
        result = {
            'symbol': data.get('Symbol'),
            'name': data.get('Name'),
            'sector': data.get('Sector'),
            'industry': data.get('Industry'),
            'market_cap': data.get('MarketCapitalization'),
            'pe_ratio': data.get('PERatio'),
            'eps': data.get('EPS'),
            'dividend_yield': data.get('DividendYield'),
            '52_week_high': data.get('52WeekHigh'),
            '52_week_low': data.get('52WeekLow'),
            'beta': data.get('Beta'),
            'description': data.get('Description', '')
        }
        
        self._save_to_cache(cache_path, result)
        return result
    
    def calculate_sma(self, df: pd.DataFrame, window: int = 20) -> pd.Series:
        """Calculate Simple Moving Average"""
        return df['close'].rolling(window=window).mean()
    
    def calculate_rsi(self, df: pd.DataFrame, window: int = 14) -> pd.Series:
        """Calculate Relative Strength Index"""
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi






