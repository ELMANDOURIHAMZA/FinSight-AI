"""
Tests for SEC EDGAR client
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
import os
import json
from src.data.sec_edgar import SecEdgarClient


class TestSecEdgarClient:
    """Test SEC EDGAR client"""
    
    @pytest.fixture
    def client(self):
        """Create client instance"""
        return SecEdgarClient()
    
    def test_get_ticker_to_cik_success(self, client):
        """Test successful ticker to CIK conversion"""
        mock_data = {
            "0": {"cik_str": 320193, "ticker": "AAPL"},
            "1": {"cik_str": 789019, "ticker": "MSFT"}
        }
        
        with patch('src.data.sec_edgar.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = mock_data
            mock_response.raise_for_status = Mock()
            mock_get.return_value = mock_response
            
            cik = client.get_ticker_to_cik("AAPL")
            
            assert cik == "0000320193"  # Padded to 10 digits
    
    def test_get_ticker_to_cik_not_found(self, client):
        """Test ticker not found"""
        mock_data = {
            "0": {"cik_str": 320193, "ticker": "AAPL"}
        }
        
        with patch('src.data.sec_edgar.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = mock_data
            mock_response.raise_for_status = Mock()
            mock_get.return_value = mock_response
            
            cik = client.get_ticker_to_cik("INVALID")
            
            assert cik is None
    
    def test_parse_10k_html(self, client, tmp_path):
        """Test HTML parsing"""
        # Create a mock HTML file
        html_content = """
        <html>
        <body>
            <h1>Item 1. Business</h1>
            <p>This is the business section content.</p>
            <h1>Item 1A. Risk Factors</h1>
            <p>These are the risk factors.</p>
        </body>
        </html>
        """
        
        html_file = tmp_path / "test.html"
        html_file.write_text(html_content)
        
        parsed = client.parse_10k_html(str(html_file))
        
        assert 'sections' in parsed
        assert 'full_text' in parsed
        assert 'metadata' in parsed
        assert len(parsed['full_text']) > 0






