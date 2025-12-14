"""
Tools for the financial agent
"""
from typing import Dict, Optional
from llama_index.core.tools import FunctionTool
from llama_index.core.llms import LLM
from src.data.alpha_vantage import AlphaVantageClient
from src.rag.retrieval import AdvancedRAGRetriever


def create_financial_report_tool(
    rag_retriever: AdvancedRAGRetriever,
    llm: Optional[LLM] = None
) -> FunctionTool:
    """
    Create a tool for analyzing financial reports using RAG
    
    Args:
        rag_retriever: AdvancedRAGRetriever instance
        llm: Optional LLM for synthesis
        
    Returns:
        FunctionTool instance
    """
    def analyze_10k_report(question: str, section: Optional[str] = None) -> str:
        """
        Use this tool to answer qualitative questions about the company's strategy, 
        risks, and performance based on their annual report (10-K).
        
        Args:
            question: The question to ask about the financial report
            section: Optional section filter (e.g., 'Item 1A' for Risk Factors)
            
        Returns:
            Answer based on the financial report
        """
        metadata_filters = None
        if section:
            metadata_filters = {'section': section}
        
        response = rag_retriever.query(
            query=question,
            metadata_filters=metadata_filters
        )
        return response
    
    return FunctionTool.from_defaults(
        fn=analyze_10k_report,
        name="analyze_10k_report",
        description="""Use this tool to answer qualitative questions about the company's 
        strategy, risks, and performance based on their annual report (10-K). 
        You can optionally filter by section (e.g., 'Item 1A' for Risk Factors)."""
    )


def create_market_data_tool(alpha_vantage_client: AlphaVantageClient) -> FunctionTool:
    """
    Create a tool for retrieving market data
    
    Args:
        alpha_vantage_client: AlphaVantageClient instance
        
    Returns:
        FunctionTool instance
    """
    def get_stock_metrics(symbol: str) -> str:
        """
        Use this tool to get the current stock price, PE ratio, market cap, 
        and other key financial metrics for a company.
        
        Args:
            symbol: Stock ticker symbol (e.g., 'AAPL', 'MSFT')
            
        Returns:
            Formatted string with stock metrics
        """
        try:
            # Get quote
            quote = alpha_vantage_client.get_quote(symbol)
            
            # Get company overview
            overview = alpha_vantage_client.get_company_overview(symbol)
            
            # Format response
            metrics = f"""
Stock Metrics for {symbol}:
- Current Price: ${quote['price']:.2f}
- Change: {quote['change']:.2f} ({quote['change_percent']})
- Volume: {quote['volume']:,}
- Market Cap: ${overview.get('market_cap', 'N/A')}
- PE Ratio: {overview.get('pe_ratio', 'N/A')}
- EPS: ${overview.get('eps', 'N/A')}
- Dividend Yield: {overview.get('dividend_yield', 'N/A')}
- 52 Week High: ${overview.get('52_week_high', 'N/A')}
- 52 Week Low: ${overview.get('52_week_low', 'N/A')}
- Beta: {overview.get('beta', 'N/A')}
- Sector: {overview.get('sector', 'N/A')}
- Industry: {overview.get('industry', 'N/A')}
"""
            return metrics.strip()
            
        except Exception as e:
            return f"Error retrieving market data for {symbol}: {str(e)}"
    
    def get_stock_time_series(symbol: str, days: int = 30) -> str:
        """
        Use this tool to get historical stock price data and technical indicators.
        
        Args:
            symbol: Stock ticker symbol
            days: Number of days of historical data to analyze
            
        Returns:
            Formatted string with time series summary
        """
        try:
            df = alpha_vantage_client.get_time_series_daily(symbol)
            
            # Limit to requested days
            if len(df) > days:
                df = df.tail(days)
            
            # Calculate indicators
            sma_20 = alpha_vantage_client.calculate_sma(df, window=20)
            rsi = alpha_vantage_client.calculate_rsi(df, window=14)
            
            # Get latest values
            latest_price = df['close'].iloc[-1]
            latest_sma = sma_20.iloc[-1] if not sma_20.isna().iloc[-1] else None
            latest_rsi = rsi.iloc[-1] if not rsi.isna().iloc[-1] else None
            
            # Calculate price change
            price_change = latest_price - df['close'].iloc[0]
            price_change_pct = (price_change / df['close'].iloc[0]) * 100
            
            summary = f"""
Time Series Analysis for {symbol} (Last {days} days):
- Latest Price: ${latest_price:.2f}
- Price Change: ${price_change:.2f} ({price_change_pct:+.2f}%)
- 20-Day SMA: ${latest_sma:.2f if latest_sma else 'N/A'}
- RSI (14): {latest_rsi:.2f if latest_rsi else 'N/A'}
- High: ${df['high'].max():.2f}
- Low: ${df['low'].min():.2f}
- Average Volume: {df['volume'].mean():,.0f}
"""
            return summary.strip()
            
        except Exception as e:
            return f"Error retrieving time series for {symbol}: {str(e)}"
    
    # Create tools
    metrics_tool = FunctionTool.from_defaults(
        fn=get_stock_metrics,
        name="get_stock_metrics",
        description="""Use this tool to get the current stock price, PE ratio, market cap, 
        and other key financial metrics for a company. Provide the stock ticker symbol."""
    )
    
    time_series_tool = FunctionTool.from_defaults(
        fn=get_stock_time_series,
        name="get_stock_time_series",
        description="""Use this tool to get historical stock price data and technical indicators 
        (SMA, RSI) for analysis. Provide the stock ticker symbol and optionally the number of days."""
    )
    
    return [metrics_tool, time_series_tool]


def get_all_tools(
    rag_retriever: AdvancedRAGRetriever,
    alpha_vantage_client: AlphaVantageClient,
    llm: Optional[LLM] = None
) -> list:
    """
    Get all available tools for the agent
    
    Args:
        rag_retriever: AdvancedRAGRetriever instance
        alpha_vantage_client: AlphaVantageClient instance
        llm: Optional LLM instance
        
    Returns:
        List of FunctionTool instances
    """
    tools = []
    
    # Add RAG tool
    tools.append(create_financial_report_tool(rag_retriever, llm))
    
    # Add market data tools
    market_tools = create_market_data_tool(alpha_vantage_client)
    tools.extend(market_tools)
    
    return tools






