"""
Tests for Alpha Vantage client
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
import json
import os
from src.data.alpha_vantage import AlphaVantageClient, rate_limited


class TestRateLimiting:
    """Test rate limiting decorator"""
    
    def test_rate_limiting(self):
        """Test that rate limiting works"""
        call_times = []
        
        @rate_limited(max_per_minute=60)  # 1 call per second
        def test_func():
            call_times.append(1)
            return 1
        
        # First call should execute immediately
        result = test_func()
        assert result == 1
        
        # Second call should also execute (but with small delay)
        result = test_func()
        assert result == 1


class TestAlphaVantageClient:
    """Test Alpha Vantage client"""
    
    @pytest.fixture
    def mock_env(self, monkeypatch):
        """Set up mock environment"""
        monkeypatch.setenv("ALPHA_VANTAGE_API_KEY", "test_key")
    
    @pytest.fixture
    def client(self, mock_env):
        """Create client instance"""
        return AlphaVantageClient(api_key="test_key")
    
    def test_init_without_key(self):
        """Test initialization without API key"""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError, match="ALPHA_VANTAGE_API_KEY"):
                AlphaVantageClient()
    
    def test_get_quote_success(self, client):
        """Test successful quote retrieval"""
        mock_response = {
            "Global Quote": {
                "01. symbol": "AAPL",
                "05. price": "150.00",
                "06. volume": "1000000",
                "09. change": "2.50",
                "10. change percent": "1.69%"
            }
        }
        
        with patch('src.data.alpha_vantage.requests.get') as mock_get:
            mock_get.return_value.json.return_value = mock_response
            mock_get.return_value.raise_for_status = Mock()
            
            quote = client.get_quote("AAPL")
            
            assert quote['symbol'] == "AAPL"
            assert quote['price'] == 150.00
            assert quote['volume'] == 1000000
    
    def test_get_quote_api_error(self, client):
        """Test handling of API errors"""
        mock_response = {"Error Message": "Invalid API call"}
        
        with patch('src.data.alpha_vantage.requests.get') as mock_get:
            mock_get.return_value.json.return_value = mock_response
            mock_get.return_value.raise_for_status = Mock()
            
            with pytest.raises(ValueError, match="Alpha Vantage API Error"):
                client.get_quote("INVALID")
    
    def test_get_quote_rate_limit(self, client):
        """Test handling of rate limit errors"""
        mock_response = {"Note": "Thank you for using Alpha Vantage API"}
        
        with patch('src.data.alpha_vantage.requests.get') as mock_get:
            mock_get.return_value.json.return_value = mock_response
            mock_get.return_value.raise_for_status = Mock()
            
            with pytest.raises(ValueError, match="Rate Limit"):
                client.get_quote("AAPL")
    
    def test_calculate_sma(self, client):
        """Test SMA calculation"""
        import pandas as pd
        import numpy as np
        
        dates = pd.date_range('2024-01-01', periods=30, freq='D')
        df = pd.DataFrame({
            'close': np.random.randn(30).cumsum() + 100
        }, index=dates)
        
        sma = client.calculate_sma(df, window=5)
        
        assert len(sma) == 30
        assert not sma.iloc[:4].notna().all()  # First 4 should be NaN
        assert sma.iloc[4:].notna().all()  # Rest should have values
    
    def test_calculate_rsi(self, client):
        """Test RSI calculation"""
        import pandas as pd
        import numpy as np
        
        dates = pd.date_range('2024-01-01', periods=30, freq='D')
        df = pd.DataFrame({
            'close': np.random.randn(30).cumsum() + 100
        }, index=dates)
        
        rsi = client.calculate_rsi(df, window=14)
        
        assert len(rsi) == 30
        # RSI should be between 0 and 100
        assert (rsi.dropna() >= 0).all()
        assert (rsi.dropna() <= 100).all()






