"""
Main Streamlit dashboard for FinSight AI
"""
import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dotenv import load_dotenv
from datetime import datetime

from llama_index.llms.gemini import Gemini
from llama_index.core.llms import LLM

from src.data.alpha_vantage import AlphaVantageClient
from src.data.sec_edgar import SecEdgarClient
from src.rag.ingestion import DocumentIngester
from src.rag.retrieval import AdvancedRAGRetriever
from src.agents.finance_agent import FinanceAgent
from src.ui.components import (
    show_welcome_screen, show_quick_start_guide, show_api_key_help,
    show_example_questions, show_error_with_solution, show_success_message,
    show_info_card
)

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="FinSight AI - Agent Financier Autonome",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Analytics Dashboard Style (Figma Template Inspired)
st.markdown("""
    <style>
    /* Import Google Fonts for Analytics Dashboard */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Global Styles - Exact Figma Template Background */
    .main {
        background-color: #F5F7FA !important;
    }
    
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 2rem;
        padding-right: 2rem;
        max-width: 1600px;
    }
    
    /* Page Header - Figma Template Style */
    .page-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 2rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid #E2E8F0;
    }
    
    .page-header h1 {
        font-family: 'Inter', sans-serif;
        font-size: 1.875rem;
        font-weight: 700;
        color: #1A202C;
        margin: 0;
        letter-spacing: -0.02em;
    }
    
    .page-header-actions {
        display: flex;
        gap: 1rem;
        align-items: center;
    }
    
    /* Filters Section - Figma Style */
    .filters-section {
        display: flex;
        gap: 1rem;
        margin-bottom: 1.5rem;
        flex-wrap: wrap;
    }
    
    .filter-dropdown {
        min-width: 150px;
    }
    
    /* Metric Cards - Exact Figma Template Style */
    [data-testid="stMetricContainer"] {
        background: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 8px !important;
        padding: 1.5rem !important;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05) !important;
        transition: all 0.2s ease !important;
        font-family: 'Inter', sans-serif !important;
        height: 100%;
    }
    
    [data-testid="stMetricContainer"]:hover {
        box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.08) !important;
    }
    
    [data-testid="stMetricValue"] {
        font-family: 'Inter', sans-serif !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
        color: #1A202C !important;
        line-height: 1.2 !important;
        margin-bottom: 0.5rem !important;
    }
    
    [data-testid="stMetricLabel"] {
        font-family: 'Inter', sans-serif !important;
        font-size: 0.8125rem !important;
        font-weight: 500 !important;
        color: #718096 !important;
        text-transform: none;
        letter-spacing: 0;
        margin-top: 0.25rem !important;
    }
    
    [data-testid="stMetricDelta"] {
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.875rem !important;
    }
    
    /* Metric Card with Icon */
    .metric-card-with-icon {
        display: flex;
        align-items: flex-start;
        gap: 0.75rem;
    }
    
    .metric-icon {
        width: 2rem;
        height: 2rem;
        border-radius: 6px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1rem;
        flex-shrink: 0;
    }
    
    /* Analytics Card Styling */
    .analytics-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05);
        margin-bottom: 1.5rem;
    }
    
    /* Sidebar Styling - Exact Figma Template Style */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E2E8F0 !important;
        padding: 1.5rem 1rem !important;
    }
    
    /* Sidebar Logo/Brand */
    .sidebar-brand {
        font-family: 'Inter', sans-serif;
        font-size: 1.5rem;
        font-weight: 700;
        color: #E53E3E;
        margin-bottom: 2rem;
        padding-bottom: 1.5rem;
        border-bottom: 1px solid #E2E8F0;
    }
    
    /* Sidebar Navigation Items */
    .sidebar-nav-item {
        display: flex;
        align-items: center;
        padding: 0.75rem 1rem;
        margin: 0.25rem 0;
        border-radius: 8px;
        font-family: 'Inter', sans-serif;
        font-size: 0.875rem;
        font-weight: 500;
        color: #4A5568;
        transition: all 0.2s;
        cursor: pointer;
    }
    
    .sidebar-nav-item:hover {
        background-color: #F7FAFC;
        color: #1A202C;
    }
    
    .sidebar-nav-item.active {
        background-color: #EBF8FF;
        color: #3182CE;
        font-weight: 600;
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
        color: #1A202C !important;
    }
    
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {
        color: #1A202C !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    [data-testid="stSidebar"] .stTextInput > div > div > input {
        background-color: #F7FAFC !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 8px !important;
        color: #1A202C !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    [data-testid="stSidebar"] .stSelectbox > div > div {
        background-color: #F7FAFC !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 8px !important;
    }
    
    /* Sidebar Support Section */
    .sidebar-support {
        margin-top: 2rem;
        padding-top: 1.5rem;
        border-top: 1px solid #E2E8F0;
    }
    
    /* Tab Styling - Analytics Dashboard */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background-color: transparent;
        padding: 0;
        border-bottom: 2px solid #E2E8F0;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border-radius: 0;
        padding: 12px 20px;
        font-weight: 500;
        font-family: 'Inter', sans-serif;
        color: #718096;
        transition: all 0.2s;
        border-bottom: 2px solid transparent;
        margin-bottom: -2px;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        color: #2D3748;
        background-color: #F7FAFC;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: transparent !important;
        color: #3182CE !important;
        border-bottom-color: #3182CE !important;
        font-weight: 600 !important;
    }
    
    /* Button Styling - Analytics Dashboard */
    .stButton > button {
        background: #3182CE !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.625rem 1.5rem !important;
        font-weight: 600 !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.875rem !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05) !important;
    }
    
    .stButton > button:hover {
        background: #2C5282 !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1) !important;
        transform: translateY(-1px);
    }
    
    .stButton > button[kind="primary"] {
        background: #3182CE !important;
    }
    
    .stButton > button[kind="primary"]:hover {
        background: #2C5282 !important;
    }
    
    /* Chart Container - Exact Figma Template Style */
    [data-testid="stPlotlyChart"] {
        background: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 8px !important;
        padding: 1.5rem !important;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05) !important;
        margin-bottom: 1.5rem !important;
    }
    
    /* Section Containers - Figma Style */
    .section-container {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
    }
    
    /* Card Title */
    .card-title {
        font-family: 'Inter', sans-serif;
        font-size: 1rem;
        font-weight: 600;
        color: #1A202C;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    
    /* Progress Bar Style */
    .progress-bar-container {
        margin: 0.75rem 0;
    }
    
    .progress-bar-label {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.5rem;
        font-family: 'Inter', sans-serif;
        font-size: 0.875rem;
        color: #4A5568;
    }
    
    .progress-bar {
        height: 8px;
        background-color: #E2E8F0;
        border-radius: 4px;
        overflow: hidden;
    }
    
    .progress-bar-fill {
        height: 100%;
        border-radius: 4px;
        transition: width 0.3s ease;
    }
    
    .progress-bar-fill.green {
        background-color: #38A169;
    }
    
    .progress-bar-fill.red {
        background-color: #E53E3E;
    }
    
    .progress-bar-fill.orange {
        background-color: #DD6B20;
    }
    
    /* Info Boxes - Analytics Dashboard Style */
    .stInfo {
        background: #EBF8FF !important;
        border: 1px solid #BEE3F8 !important;
        border-left: 4px solid #3182CE !important;
        border-radius: 8px !important;
        color: #2C5282 !important;
    }
    
    .stSuccess {
        background: #F0FFF4 !important;
        border: 1px solid #C6F6D5 !important;
        border-left: 4px solid #38A169 !important;
        border-radius: 8px !important;
        color: #22543D !important;
    }
    
    .stWarning {
        background: #FFFAF0 !important;
        border: 1px solid #FEEBC8 !important;
        border-left: 4px solid #DD6B20 !important;
        border-radius: 8px !important;
        color: #7C2D12 !important;
    }
    
    .stError {
        background: #FED7D7 !important;
        border: 1px solid #FEB2B2 !important;
        border-left: 4px solid #E53E3E !important;
        border-radius: 8px !important;
        color: #742A2A !important;
    }
    
    /* Chat Interface */
    [data-testid="stChatMessage"] {
        padding: 1rem;
        border-radius: 12px;
        margin-bottom: 1rem;
    }
    
    /* Section Headers - Analytics Dashboard Typography */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Inter', sans-serif !important;
        color: #1A202C !important;
    }
    
    h2 {
        font-weight: 700 !important;
        font-size: 1.5rem !important;
        margin-top: 1.5rem !important;
        margin-bottom: 1rem !important;
        color: #1A202C !important;
        letter-spacing: -0.01em !important;
    }
    
    h3 {
        font-weight: 600 !important;
        font-size: 1.125rem !important;
        margin-top: 1.25rem !important;
        margin-bottom: 0.75rem !important;
        color: #2D3748 !important;
    }
    
    p, div, span {
        font-family: 'Inter', sans-serif !important;
        color: #4A5568 !important;
    }
    
    /* Expander Styling */
    .streamlit-expanderHeader {
        font-weight: 600;
        color: #1e293b;
        background: #f8fafc;
        border-radius: 8px;
        padding: 0.75rem;
    }
    
    /* Input Fields - Analytics Dashboard */
    [data-baseweb="input"] {
        background-color: #F7FAFC !important;
        border-radius: 8px !important;
        border: 1px solid #E2E8F0 !important;
        font-family: 'Inter', sans-serif !important;
        color: #1A202C !important;
        padding: 0.5rem 0.75rem !important;
    }
    
    [data-baseweb="input"]:focus {
        border-color: #3182CE !important;
        box-shadow: 0 0 0 3px rgba(49, 130, 206, 0.1) !important;
        background-color: #FFFFFF !important;
    }
    
    /* Selectbox Styling */
    [data-baseweb="select"] {
        background-color: #F7FAFC !important;
        border-radius: 8px !important;
        border: 1px solid #E2E8F0 !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    [data-baseweb="select"]:focus {
        border-color: #3182CE !important;
        box-shadow: 0 0 0 3px rgba(49, 130, 206, 0.1) !important;
    }
    
    /* Divider */
    hr {
        margin: 1.5rem 0;
        border: none;
        border-top: 1px solid #E2E8F0;
    }
    
    /* Chat Interface - Analytics Style */
    [data-testid="stChatMessage"] {
        background: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 12px !important;
        padding: 1rem 1.25rem !important;
        margin-bottom: 1rem !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    [data-testid="stChatInput"] {
        background: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 12px !important;
    }
    
    /* Expander Styling */
    .streamlit-expanderHeader {
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        color: #2D3748 !important;
        background: #F7FAFC !important;
        border-radius: 8px !important;
        padding: 0.75rem 1rem !important;
        border: 1px solid #E2E8F0 !important;
    }
    
    /* Spinner Styling */
    .stSpinner > div {
        border-top-color: #3182CE !important;
    }
    
    /* Metric Delta Colors */
    [data-testid="stMetricDelta"] svg {
        color: inherit !important;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Additional Analytics Dashboard Styles */
    .analytics-grid {
        display: grid;
        gap: 1.5rem;
    }
    
    /* Scrollbar Styling */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #F7FAFC;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #CBD5E0;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #A0AEC0;
    }
    </style>
""", unsafe_allow_html=True)


@st.cache_resource
def initialize_clients():
    """Initialize API clients (cached)"""
    try:
        # Try to initialize Alpha Vantage client
        # It will raise ValueError if API key is missing, which is handled gracefully
        alpha_client = AlphaVantageClient()
        sec_client = SecEdgarClient()
        return alpha_client, sec_client
    except ValueError as e:
        # API key missing - this is expected if not configured yet
        return None, None
    except Exception as e:
        st.error(f"Error initializing clients: {e}")
        return None, None


@st.cache_resource
def initialize_llm(model_name: str = "gemini-2.0-flash-exp"):
    """Initialize LLM (cached)"""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return None
    
    try:
        if model_name.startswith("gemini"):
            # Gemini initialization with LlamaIndex
            # Format model name correctly (with or without "models/" prefix)
            if not model_name.startswith("models/"):
                # Try with models/ prefix first (required format for API)
                formatted_model = f"models/{model_name}"
            else:
                formatted_model = model_name
            
            # Try the specified model name first
            try:
            llm = Gemini(
                    model=formatted_model,
                temperature=0,
                api_key=api_key
            )
            except Exception as e:
                # If model not found, try gemini-2.0-flash-exp as fallback
                if "404" in str(e) or "not found" in str(e).lower():
                    st.warning(f"Modèle {model_name} non trouvé. Tentative avec models/gemini-2.0-flash-exp...")
                    try:
                        llm = Gemini(
                            model="models/gemini-2.0-flash-exp",
                            temperature=0,
                            api_key=api_key
                        )
                    except Exception as e2:
                        st.error(f"Impossible d'initialiser le modèle LLM: {e2}")
                        return None
        else:
                    raise e
        else:
            st.error(f"Model {model_name} not yet supported. Please use a Gemini model (gemini-1.5-pro, gemini-1.5-flash)")
            return None
        return llm
    except Exception as e:
        st.error(f"Error initializing LLM: {e}")
        return None


def initialize_rag_system(ticker: str, llm: LLM):
    """Initialize RAG system for a ticker"""
    try:
        # Get 10-K report
        sec_client = SecEdgarClient()
        report_data = sec_client.get_10k_text(ticker)
        
        # Check if we got valid data (not just an error message)
        if not report_data.get('sections') or len(report_data.get('sections', {})) == 0:
            raise ValueError("No valid report data retrieved")
        
        # Check if it's an error message section
        sections = report_data.get('sections', {})
        if 'Note' in sections and 'téléchargement automatique a échoué' in sections.get('Note', ''):
            raise ValueError("Automatic download failed - please use manual upload")
        
        # Create documents
        ingester = DocumentIngester()
        documents = ingester.create_documents_from_sections(
            sections=report_data['sections'],
            base_metadata={'ticker': ticker, 'year': '2024'}
        )
        
        if not documents or len(documents) == 0:
            raise ValueError("No documents created from report data")
        
        # Ingest documents
        collection_name = f"finsight_{ticker.lower()}"
        index = ingester.ingest_documents(
            documents=documents,
            collection_name=collection_name,
            reset=False
        )
        
        # Create retriever
        retriever = AdvancedRAGRetriever(
            index=index,
            llm=llm,
            similarity_top_k=5,
            rerank_top_k=3
        )
        
        return retriever, report_data
        
    except ValueError as e:
        # Re-raise ValueError with more context
        raise ValueError(f"RAG initialization failed: {e}")
    except Exception as e:
        raise RuntimeError(f"Error initializing RAG system: {e}")


def create_price_chart_only(df: pd.DataFrame, ticker: str):
    """Create price chart with SMAs only"""
    fig = go.Figure()
    
    # Analytics Dashboard Color Scheme
    primary_color = '#3182CE'
    accent_color = '#DD6B20'
    secondary_color = '#805AD5'
    
    # Price line
    fig.add_trace(
        go.Scatter(
            x=df.index, 
            y=df['close'], 
            name='Prix de Clôture', 
            line=dict(color=primary_color, width=2.5),
            fill='tozeroy',
            fillcolor=f'rgba(49, 130, 206, 0.08)'
        )
    )
    
    # Calculate SMAs
    sma_20 = df['close'].rolling(window=20).mean()
    sma_50 = df['close'].rolling(window=50).mean()
    
    fig.add_trace(
        go.Scatter(
            x=df.index, 
            y=sma_20, 
            name='SMA 20', 
            line=dict(color=accent_color, width=2, dash='dot')
        )
    )
    fig.add_trace(
        go.Scatter(
            x=df.index, 
            y=sma_50, 
            name='SMA 50', 
            line=dict(color=secondary_color, width=2, dash='dash')
        )
    )
    
    fig.update_layout(
        height=500,
        title={
            'text': f"{ticker} - Évolution du Prix",
            'x': 0,
            'xanchor': 'left',
            'font': {'size': 18, 'color': '#1A202C', 'family': 'Inter, sans-serif'}
        },
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=11, family='Inter, sans-serif', color='#4A5568'),
            bgcolor='rgba(255,255,255,0.8)',
            bordercolor='#E2E8F0',
            borderwidth=1
        ),
        plot_bgcolor='#FFFFFF',
        paper_bgcolor='#FFFFFF',
        font=dict(family="Inter, sans-serif", size=12, color="#4A5568"),
        hovermode='x unified',
        margin=dict(l=60, r=40, t=60, b=60),
        xaxis=dict(
            title_text="Date",
            title_font=dict(family='Inter, sans-serif', size=12, color='#718096'),
            showgrid=True,
            gridwidth=1,
            gridcolor='#E2E8F0',
            showline=True,
            linewidth=1,
            linecolor='#E2E8F0',
            tickfont=dict(family='Inter, sans-serif', size=11, color='#718096')
        ),
        yaxis=dict(
            title_text="Prix ($)",
            title_font=dict(family='Inter, sans-serif', size=12, color='#718096'),
            showgrid=True,
            gridwidth=1,
            gridcolor='#E2E8F0',
            showline=True,
            linewidth=1,
            linecolor='#E2E8F0',
            tickfont=dict(family='Inter, sans-serif', size=11, color='#718096')
        ),
        hoverlabel=dict(
            bgcolor='#FFFFFF',
            bordercolor='#E2E8F0',
            font_size=12,
            font_family='Inter, sans-serif'
        )
    )
    
    return fig


def create_volume_chart(df: pd.DataFrame, ticker: str):
    """Create volume chart only"""
    fig = go.Figure()
    
    # Color scheme
    positive_color = '#38A169'
    negative_color = '#E53E3E'
    
    # Volume bars with color coding
    colors = [negative_color if df['close'].iloc[i] < df['open'].iloc[i] else positive_color 
              for i in range(len(df))]
    
    fig.add_trace(
        go.Bar(
            x=df.index, 
            y=df['volume'], 
            name='Volume',
            marker_color=colors,
            opacity=0.7
        )
    )
    
    fig.update_layout(
        height=500,
        title={
            'text': f"{ticker} - Volume de Transactions",
            'x': 0,
            'xanchor': 'left',
            'font': {'size': 18, 'color': '#1A202C', 'family': 'Inter, sans-serif'}
        },
        showlegend=False,
        plot_bgcolor='#FFFFFF',
        paper_bgcolor='#FFFFFF',
        font=dict(family="Inter, sans-serif", size=12, color="#4A5568"),
        hovermode='x unified',
        margin=dict(l=60, r=40, t=60, b=60),
        xaxis=dict(
            title_text="Date",
            title_font=dict(family='Inter, sans-serif', size=12, color='#718096'),
            showgrid=True,
            gridwidth=1,
            gridcolor='#E2E8F0',
            showline=True,
            linewidth=1,
            linecolor='#E2E8F0',
            tickfont=dict(family='Inter, sans-serif', size=11, color='#718096')
        ),
        yaxis=dict(
            title_text="Volume",
            title_font=dict(family='Inter, sans-serif', size=12, color='#718096'),
            showgrid=True,
            gridwidth=1,
            gridcolor='#E2E8F0',
            showline=True,
            linewidth=1,
            linecolor='#E2E8F0',
            tickfont=dict(family='Inter, sans-serif', size=11, color='#718096')
        ),
        hoverlabel=dict(
            bgcolor='#FFFFFF',
            bordercolor='#E2E8F0',
            font_size=12,
            font_family='Inter, sans-serif'
        )
    )
    
    return fig


def create_rsi_chart(df: pd.DataFrame, ticker: str):
    """Create RSI chart only"""
    fig = go.Figure()
    
    # Color scheme
    primary_color = '#3182CE'
    negative_color = '#E53E3E'
    positive_color = '#38A169'
    
    # Calculate RSI
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    
    fig.add_trace(
        go.Scatter(
            x=df.index, 
            y=rsi, 
            name='RSI', 
            line=dict(color=primary_color, width=2.5),
            fill='tozeroy',
            fillcolor=f'rgba(49, 130, 206, 0.08)'
        )
    )
    
    # Add reference lines
    fig.add_hline(
        y=70, 
        line_dash="dash", 
        line_color=negative_color, 
        line_width=2,
        annotation_text="Surachat (70)",
        annotation_position="right",
        annotation_font=dict(size=10, color=negative_color)
    )
    fig.add_hline(
        y=30, 
        line_dash="dash", 
        line_color=positive_color, 
        line_width=2,
        annotation_text="Survente (30)",
        annotation_position="right",
        annotation_font=dict(size=10, color=positive_color)
    )
    fig.add_hline(
        y=50, 
        line_dash="dot", 
        line_color="#94a3b8", 
        line_width=1,
        opacity=0.5
    )
    
    fig.update_layout(
        height=500,
        title={
            'text': f"{ticker} - Indicateur RSI (Relative Strength Index)",
            'x': 0,
            'xanchor': 'left',
            'font': {'size': 18, 'color': '#1A202C', 'family': 'Inter, sans-serif'}
        },
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=11, family='Inter, sans-serif', color='#4A5568'),
            bgcolor='rgba(255,255,255,0.8)',
            bordercolor='#E2E8F0',
            borderwidth=1
        ),
        plot_bgcolor='#FFFFFF',
        paper_bgcolor='#FFFFFF',
        font=dict(family="Inter, sans-serif", size=12, color="#4A5568"),
        hovermode='x unified',
        margin=dict(l=60, r=40, t=60, b=60),
        xaxis=dict(
            title_text="Date",
            title_font=dict(family='Inter, sans-serif', size=12, color='#718096'),
            showgrid=True,
            gridwidth=1,
            gridcolor='#E2E8F0',
            showline=True,
            linewidth=1,
            linecolor='#E2E8F0',
            tickfont=dict(family='Inter, sans-serif', size=11, color='#718096')
        ),
        yaxis=dict(
            title_text="RSI",
            title_font=dict(family='Inter, sans-serif', size=12, color='#718096'),
            range=[0, 100],
            showgrid=True,
            gridwidth=1,
            gridcolor='#E2E8F0',
            showline=True,
            linewidth=1,
            linecolor='#E2E8F0',
            tickfont=dict(family='Inter, sans-serif', size=11, color='#718096')
        ),
        hoverlabel=dict(
            bgcolor='#FFFFFF',
            bordercolor='#E2E8F0',
            font_size=12,
            font_family='Inter, sans-serif'
        )
    )
    
    return fig


def create_price_chart(df: pd.DataFrame, ticker: str):
    """Create interactive price chart with indicators - Modern Analytics Style"""
    fig = make_subplots(
        rows=3, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.05,
        subplot_titles=('📈 Prix & Moyennes Mobiles', '📊 Volume', '📉 RSI (Relative Strength Index)'),
        row_heights=[0.5, 0.2, 0.3],
        specs=[[{"secondary_y": False}],
               [{"secondary_y": False}],
               [{"secondary_y": False}]]
    )
    
    # Analytics Dashboard Color Scheme (Figma Template Inspired)
    primary_color = '#3182CE'  # Blue
    secondary_color = '#805AD5'  # Purple
    positive_color = '#38A169'  # Green
    negative_color = '#E53E3E'  # Red
    volume_color = '#3182CE'  # Blue
    accent_color = '#DD6B20'  # Orange
    neutral_color = '#718096'  # Gray
    
    # Price and SMA - Analytics Dashboard Style
    fig.add_trace(
        go.Scatter(
            x=df.index, 
            y=df['close'], 
            name='Prix de Clôture', 
            line=dict(color=primary_color, width=2.5),
            fill='tonexty',
            fillcolor=f'rgba(49, 130, 206, 0.08)'
        ),
        row=1, col=1
    )
    
    # Calculate SMA
    sma_20 = df['close'].rolling(window=20).mean()
    sma_50 = df['close'].rolling(window=50).mean()
    
    fig.add_trace(
        go.Scatter(
            x=df.index, 
            y=sma_20, 
            name='SMA 20', 
            line=dict(color=accent_color, width=2, dash='dot')
        ),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(
            x=df.index, 
            y=sma_50, 
            name='SMA 50', 
            line=dict(color=secondary_color, width=2, dash='dash')
        ),
        row=1, col=1
    )
    
    # Volume - Modern bar chart
    colors = [negative_color if df['close'].iloc[i] < df['open'].iloc[i] else positive_color 
              for i in range(len(df))]
    fig.add_trace(
        go.Bar(
            x=df.index, 
            y=df['volume'], 
            name='Volume',
            marker_color=colors,
            opacity=0.7
        ),
        row=2, col=1
    )
    
    # RSI - Analytics Dashboard Style
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    
    fig.add_trace(
        go.Scatter(
            x=df.index, 
            y=rsi, 
            name='RSI', 
            line=dict(color=primary_color, width=2),
            fill='tozeroy',
            fillcolor=f'rgba(49, 130, 206, 0.08)'
        ),
        row=3, col=1
    )
    
    # Add RSI reference lines
    fig.add_hline(
        y=70, 
        line_dash="dash", 
        line_color=negative_color, 
        line_width=2,
        annotation_text="Surachat (70)",
        annotation_position="right",
        row=3, col=1
    )
    fig.add_hline(
        y=30, 
        line_dash="dash", 
        line_color=positive_color, 
        line_width=2,
        annotation_text="Survente (30)",
        annotation_position="right",
        row=3, col=1
    )
    fig.add_hline(
        y=50, 
        line_dash="dot", 
        line_color="#94a3b8", 
        line_width=1,
        opacity=0.5,
        row=3, col=1
    )
    
    # Analytics Dashboard Layout
    fig.update_layout(
        height=850,
        title={
            'text': f"{ticker} - Analyse Technique",
            'x': 0,
            'xanchor': 'left',
            'font': {'size': 18, 'color': '#1A202C', 'family': 'Inter, sans-serif'}
        },
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=11, family='Inter, sans-serif', color='#4A5568'),
            bgcolor='rgba(255,255,255,0.8)',
            bordercolor='#E2E8F0',
            borderwidth=1
        ),
        plot_bgcolor='#FFFFFF',
        paper_bgcolor='#FFFFFF',
        font=dict(family="Inter, sans-serif", size=12, color="#4A5568"),
        hovermode='x unified',
        margin=dict(l=60, r=40, t=60, b=60),
        hoverlabel=dict(
            bgcolor='#FFFFFF',
            bordercolor='#E2E8F0',
            font_size=12,
            font_family='Inter, sans-serif'
        )
    )
    
    # Update axes with Analytics Dashboard styling
    fig.update_xaxes(
        title_text="Date",
        title_font=dict(family='Inter, sans-serif', size=12, color='#718096'),
        row=3, col=1,
        showgrid=True,
        gridwidth=1,
        gridcolor='#E2E8F0',
        showline=True,
        linewidth=1,
        linecolor='#E2E8F0',
        tickfont=dict(family='Inter, sans-serif', size=11, color='#718096')
    )
    fig.update_yaxes(
        title_text="Prix ($)",
        title_font=dict(family='Inter, sans-serif', size=12, color='#718096'),
        row=1, col=1,
        showgrid=True,
        gridwidth=1,
        gridcolor='#E2E8F0',
        showline=True,
        linewidth=1,
        linecolor='#E2E8F0',
        tickfont=dict(family='Inter, sans-serif', size=11, color='#718096')
    )
    fig.update_yaxes(
        title_text="Volume",
        title_font=dict(family='Inter, sans-serif', size=12, color='#718096'),
        row=2, col=1,
        showgrid=True,
        gridwidth=1,
        gridcolor='#E2E8F0',
        showline=True,
        linewidth=1,
        linecolor='#E2E8F0',
        tickfont=dict(family='Inter, sans-serif', size=11, color='#718096')
    )
    fig.update_yaxes(
        title_text="RSI",
        title_font=dict(family='Inter, sans-serif', size=12, color='#718096'),
        row=3, col=1,
        range=[0, 100],
        showgrid=True,
        gridwidth=1,
        gridcolor='#E2E8F0',
        showline=True,
        linewidth=1,
        linecolor='#E2E8F0',
        tickfont=dict(family='Inter, sans-serif', size=11, color='#718096')
    )
    
    return fig


def main():
    """Main application - Analytics Dashboard Style"""
    # Check if first visit
    if 'first_visit' not in st.session_state:
        st.session_state.first_visit = True
    
    # Welcome screen for first-time users
    if st.session_state.first_visit and not os.getenv("GEMINI_API_KEY") and not os.getenv("ALPHA_VANTAGE_API_KEY"):
        show_welcome_screen()
        st.markdown("---")
    
    # Initialize ticker variable early (before filters)
    # Will be updated from sidebar input later
    ticker = st.session_state.get('current_ticker', '') or st.session_state.get('sidebar_ticker', '')
    
    # Page Header - Figma Template Style
    header_col1, header_col2 = st.columns([1, 0.2])
    
    with header_col1:
        st.markdown("""
        <div class="page-header">
            <h1>Dashboard Marché</h1>
        </div>
        """, unsafe_allow_html=True)
    
    with header_col2:
        if st.button("📥 Télécharger", use_container_width=True):
            st.info("Fonctionnalité de téléchargement à venir")
    
    # Filters Section - Figma Style
    st.markdown("""
    <div class="filters-section">
    </div>
    """, unsafe_allow_html=True)
    
    filter_col1, filter_col2, filter_col3 = st.columns(3)
    
    with filter_col1:
        timeframe = st.selectbox(
            "Période",
            ["7 jours", "30 jours", "90 jours", "1 an", "Tout"],
            index=4,
            label_visibility="collapsed"
        )
    
    with filter_col2:
        ticker_display = ticker if ticker else "Sélectionner..."
        st.selectbox(
            "Symbole",
            ["Tous", ticker_display],
            index=0,
            label_visibility="collapsed",
            disabled=True
        )
    
    with filter_col3:
        st.selectbox(
            "Type",
            ["Tous", "Actions", "ETF", "Indices"],
            index=0,
            label_visibility="collapsed",
            disabled=True
        )
    
    # Sidebar - Figma Template Style with Logo
    with st.sidebar:
        # Logo/Brand
        st.markdown("""
        <div class="sidebar-brand">
            FinSight AI
        </div>
        """, unsafe_allow_html=True)
        
        # Navigation Menu
        st.markdown("""
        <div style='margin-bottom: 2rem;'>
            <div class="sidebar-nav-item active">
                📊 Dashboard Marché
            </div>
            <div class="sidebar-nav-item">
                💬 Assistant Financier
            </div>
            <div class="sidebar-nav-item">
                📄 Explorateur Documents
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="sidebar-support">
            <h3 style='font-family: Inter, sans-serif; font-size: 0.75rem; font-weight: 600; 
                       color: #718096; text-transform: uppercase; letter-spacing: 0.05em; 
                       margin-bottom: 0.75rem;'>
                Support
            </h3>
            <div class="sidebar-nav-item">
                💡 Guide de Démarrage
            </div>
            <div class="sidebar-nav-item">
                ⚙️ Paramètres
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style='padding: 0.5rem 0; margin-top: 2rem; margin-bottom: 1.5rem; border-top: 1px solid #E2E8F0;'>
            <h3 style='font-family: Inter, sans-serif; font-size: 0.875rem; font-weight: 600; 
                       color: #1A202C; margin: 0;'>
                Configuration
            </h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Quick Start Guide
        show_quick_start_guide()
        st.divider()
        
        # API Keys Section with Help
        st.markdown("### 🔑 Clés API")
        
        gemini_key = st.text_input(
            "🔵 Gemini API Key",
            value=os.getenv("GEMINI_API_KEY", ""),
            type="password",
            help="Clé API Google Gemini (gratuite) - Commence par 'AIza...'",
            placeholder="AIza..."
        )
        if gemini_key:
            os.environ["GEMINI_API_KEY"] = gemini_key
            if gemini_key.startswith("AIza"):
                st.success("✓ Clé Gemini valide")
            else:
                st.warning("⚠️ Format de clé invalide")
        
        alpha_key = st.text_input(
            "📊 Alpha Vantage API Key",
            value=os.getenv("ALPHA_VANTAGE_API_KEY", ""),
            type="password",
            help="Clé API Alpha Vantage (gratuite) - 16 caractères",
            placeholder="Votre clé Alpha Vantage..."
        )
        if alpha_key:
            os.environ["ALPHA_VANTAGE_API_KEY"] = alpha_key
            if len(alpha_key) >= 10:
                st.success("✓ Clé Alpha Vantage valide")
            else:
                st.warning("⚠️ Clé trop courte")
        
        # Help button for API keys
        show_api_key_help()
        
        st.divider()
        
        # Model selection with better description
        st.markdown("### 🤖 Modèle IA")
        model_name = st.selectbox(
            "Modèle de Langage",
            options=["gemini-2.0-flash-exp", "gemini-1.5-pro", "gemini-1.5-flash"],
            index=0,
            help="gemini-2.0-flash-exp : Rapide et efficace (recommandé)\ngemini-1.5-pro : Plus précis mais plus lent\ngemini-1.5-flash : Équilibre vitesse/précision"
        )
        
        st.divider()
        
        # Ticker input with examples
        st.markdown("### 📈 Analyse d'Entreprise")
        sidebar_ticker_input = st.text_input(
            "Symbole Boursier",
            value=st.session_state.get('current_ticker', 'AAPL'),
            help="Entrez le symbole boursier (ex: AAPL pour Apple, MSFT pour Microsoft)",
            placeholder="AAPL, MSFT, GOOGL...",
            key="sidebar_ticker_input"
        ).upper()
        
        # Store ticker in session state and update main ticker variable
        if sidebar_ticker_input:
            st.session_state['sidebar_ticker'] = sidebar_ticker_input
            ticker = sidebar_ticker_input
        
        # Popular tickers quick select
        st.markdown("**Exemples rapides :**")
        quick_cols = st.columns(4)
        popular_tickers = ["AAPL", "MSFT", "GOOGL", "TSLA"]
        for i, tick in enumerate(popular_tickers):
            with quick_cols[i]:
                if st.button(tick, key=f"quick_{tick}", use_container_width=True):
                    st.session_state['sidebar_ticker'] = tick
                    ticker = tick
                    st.rerun()
        
        st.divider()
        
        analyze_button = st.button(
            "🚀 Lancer l'Analyse", 
            type="primary", 
            use_container_width=True,
            help="Cliquez pour analyser l'entreprise sélectionnée"
        )
        
        # Update main ticker variable from sidebar input
        if sidebar_ticker_input:
            ticker = sidebar_ticker_input
        
        # Status indicators
        st.divider()
        st.markdown("### 📊 Statut")
        
        if gemini_key and alpha_key:
            st.success("✅ Prêt à analyser")
        elif gemini_key:
            st.warning("⚠️ Clé Alpha Vantage manquante")
        elif alpha_key:
            st.warning("⚠️ Clé Gemini manquante")
        else:
            st.error("❌ Clés API requises")
    
    # Initialize clients with better error handling
    alpha_client, sec_client = initialize_clients()
    
    if not alpha_client or not sec_client:
        show_error_with_solution(
            "Les clés API ne sont pas configurées",
            """
            **Pour continuer :**
            1. Dans la sidebar à gauche, entrez votre clé Gemini API
            2. Entrez votre clé Alpha Vantage API
            3. Les deux clés sont gratuites (voir le guide dans la sidebar)
            4. Une fois configurées, cliquez sur "Lancer l'Analyse"
            """
        )
        show_info_card(
            "💡 Première utilisation ?",
            "Consultez le guide de démarrage rapide dans la sidebar pour obtenir vos clés API gratuitement."
        )
        st.stop()
    
    # Initialize LLM with better error handling
    llm = initialize_llm(model_name)
    if not llm:
        show_error_with_solution(
            "Le modèle IA n'a pas pu être initialisé",
            """
            **Vérifiez :**
            1. Votre clé Gemini API est correcte (commence par 'AIza...')
            2. Vous avez une connexion Internet active
            3. Le modèle sélectionné est disponible
            
            **Solution :** Vérifiez votre clé dans la sidebar et réessayez.
            """
        )
        st.stop()
    
    # Main content tabs
    tab1, tab2, tab3 = st.tabs(["📈 Dashboard Marché", "💬 Assistant Financier", "📄 Explorateur de Documents"])
    
    # Tab 1: Market Dashboard
    with tab1:
        if analyze_button or ticker:
            st.header(f"Analyse de {ticker}")
            
            # Check if clients are initialized
            if not alpha_client:
                st.warning("⚠️ Veuillez configurer votre clé Alpha Vantage API dans la sidebar")
                st.stop()
            
            with st.spinner("Récupération des données de marché..."):
                try:
                    # Get quote
                    quote = alpha_client.get_quote(ticker)
                    
                    # Get overview
                    overview = alpha_client.get_company_overview(ticker)
                    
                    # Display metrics - Figma Template Style with Icons
                    st.markdown("""
                    <div style='margin-bottom: 1.5rem;'>
                        <h3 style='font-family: Inter, sans-serif; font-size: 1rem; 
                                   font-weight: 600; color: #1A202C; margin-bottom: 1.25rem;'>
                            Métriques Clés
                        </h3>
                    </div>
                    """, unsafe_allow_html=True)
                    col1, col2, col3, col4 = st.columns(4)
                    
                    # Determine if price change is positive or negative
                    change_value = quote.get('change', 0)
                    change_percent = quote.get('change_percent', '0%')
                    delta_color = "normal"
                    if isinstance(change_percent, str) and change_percent != 'N/A':
                        try:
                            change_num = float(change_percent.replace('%', '').replace('+', ''))
                            if change_num > 0:
                                delta_color = "normal"
                            elif change_num < 0:
                                delta_color = "inverse"
                        except:
                            pass
                    
                    # Metric cards with icons - Figma Template Style
                    with col1:
                        st.markdown(f"""
                        <div class="metric-card-with-icon" style='background: #FFFFFF; border: 1px solid #E2E8F0; 
                                    border-radius: 8px; padding: 1.5rem; box-shadow: 0 1px 2px 0 rgba(0,0,0,0.05);'>
                            <div class="metric-icon" style='background: #EBF8FF; color: #3182CE;'>
                                💰
                            </div>
                            <div style='flex: 1;'>
                                <div style='font-family: Inter, sans-serif; font-size: 0.8125rem; color: #718096; 
                                           margin-bottom: 0.5rem;'>Prix Actuel</div>
                                <div style='font-family: Inter, sans-serif; font-size: 2rem; font-weight: 700; 
                                           color: #1A202C; margin-bottom: 0.25rem;'>
                                    ${quote['price']:.2f}
                                </div>
                                <div style='font-family: Inter, sans-serif; font-size: 0.875rem; font-weight: 600; 
                                           color: {"#38A169" if delta_color == "normal" else "#E53E3E"};'>
                                    {change_value:.2f} ({change_percent})
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    market_cap = overview.get('market_cap')
                    if market_cap:
                        market_cap_formatted = f"${int(market_cap):,}"
                        if int(market_cap) >= 1_000_000_000:
                            market_cap_formatted = f"${int(market_cap)/1_000_000_000:.2f}B"
                        elif int(market_cap) >= 1_000_000:
                            market_cap_formatted = f"${int(market_cap)/1_000_000:.2f}M"
                    else:
                        market_cap_formatted = "N/A"
                    
                    with col2:
                        st.markdown(f"""
                        <div class="metric-card-with-icon" style='background: #FFFFFF; border: 1px solid #E2E8F0; 
                                    border-radius: 8px; padding: 1.5rem; box-shadow: 0 1px 2px 0 rgba(0,0,0,0.05);'>
                            <div class="metric-icon" style='background: #F0FFF4; color: #38A169;'>
                                🏢
                            </div>
                            <div style='flex: 1;'>
                                <div style='font-family: Inter, sans-serif; font-size: 0.8125rem; color: #718096; 
                                           margin-bottom: 0.5rem;'>Capitalisation</div>
                                <div style='font-family: Inter, sans-serif; font-size: 2rem; font-weight: 700; 
                                           color: #1A202C;'>
                                    {market_cap_formatted}
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col3:
                        pe_ratio = overview.get('pe_ratio', 'N/A')
                        pe_display = f"{pe_ratio}" if pe_ratio and pe_ratio != 'N/A' else "N/A"
                        st.markdown(f"""
                        <div class="metric-card-with-icon" style='background: #FFFFFF; border: 1px solid #E2E8F0; 
                                    border-radius: 8px; padding: 1.5rem; box-shadow: 0 1px 2px 0 rgba(0,0,0,0.05);'>
                            <div class="metric-icon" style='background: #FFFAF0; color: #DD6B20;'>
                                📈
                            </div>
                            <div style='flex: 1;'>
                                <div style='font-family: Inter, sans-serif; font-size: 0.8125rem; color: #718096; 
                                           margin-bottom: 0.5rem;'>Ratio P/E</div>
                                <div style='font-family: Inter, sans-serif; font-size: 2rem; font-weight: 700; 
                                           color: #1A202C;'>
                                    {pe_display}
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col4:
                        dividend = overview.get('dividend_yield', 'N/A')
                        if dividend and dividend != 'N/A':
                            if isinstance(dividend, str) and '%' not in dividend:
                                dividend = f"{dividend}%"
                            div_display = f"{dividend}"
                        else:
                            div_display = "N/A"
                        st.markdown(f"""
                        <div class="metric-card-with-icon" style='background: #FFFFFF; border: 1px solid #E2E8F0; 
                                    border-radius: 8px; padding: 1.5rem; box-shadow: 0 1px 2px 0 rgba(0,0,0,0.05);'>
                            <div class="metric-icon" style='background: #FEF5E7; color: #F6AD55;'>
                                💵
                            </div>
                            <div style='flex: 1;'>
                                <div style='font-family: Inter, sans-serif; font-size: 0.8125rem; color: #718096; 
                                           margin-bottom: 0.5rem;'>Rendement Dividende</div>
                                <div style='font-family: Inter, sans-serif; font-size: 2rem; font-weight: 700; 
                                           color: #1A202C;'>
                                    {div_display}
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    # Get time series data
                    df = alpha_client.get_time_series_daily(ticker, outputsize="compact")
                    df = df.tail(100)  # Limit to last 100 days for performance
                    
                    # Create sub-tabs for each chart type
                    chart_tab1, chart_tab2, chart_tab3, chart_tab4 = st.tabs([
                        "📈 Prix & Tendances", 
                        "📊 Volume", 
                        "📉 RSI (Force Relative)",
                        "📋 Vue d'Ensemble"
                    ])
                    
                    # Tab 1: Price Chart
                    with chart_tab1:
                        st.markdown("""
                        <div style='background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px; 
                                    padding: 1.5rem; margin-bottom: 1.5rem; box-shadow: 0 1px 3px 0 rgba(0,0,0,0.05);'>
                            <h3 style='font-family: Inter, sans-serif; font-size: 1.125rem; font-weight: 600; 
                                      color: #2D3748; margin: 0 0 0.75rem 0;'>
                                Graphique des Prix avec Moyennes Mobiles
                            </h3>
                            <p style='font-family: Inter, sans-serif; font-size: 0.875rem; color: #718096; margin: 0;'>
                                Visualisez l'évolution du prix de clôture avec les moyennes mobiles simples (SMA) pour identifier les tendances.
                            </p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Create price chart only
                        fig_price = create_price_chart_only(df, ticker)
                        st.plotly_chart(fig_price, use_container_width=True)
                        
                        # Explanation card
                        st.markdown("""
                        <div style='background: #EBF8FF; border: 1px solid #BEE3F8; border-left: 4px solid #3182CE; 
                                    padding: 1.25rem; border-radius: 8px; margin-top: 1.5rem;'>
                            <h4 style='font-family: Inter, sans-serif; color: #2C5282; margin-bottom: 0.75rem; 
                                      font-size: 0.875rem; font-weight: 600;'>
                                💡 Comment Interpréter ce Graphique
                            </h4>
                            <ul style='font-family: Inter, sans-serif; color: #2C5282; font-size: 0.875rem; 
                                      margin: 0; padding-left: 1.5rem;'>
                                <li style='margin-bottom: 0.5rem;'>
                                    <strong>Prix de Clôture (Bleu) :</strong> Le prix auquel l'action s'est négociée à la fin de chaque jour
                                </li>
                                <li style='margin-bottom: 0.5rem;'>
                                    <strong>SMA 20 (Orange pointillée) :</strong> Moyenne mobile sur 20 jours - tendance à court terme
                                </li>
                                <li style='margin-bottom: 0.5rem;'>
                                    <strong>SMA 50 (Violette tiretée) :</strong> Moyenne mobile sur 50 jours - tendance à moyen terme
                                </li>
                                <li style='margin-bottom: 0.5rem;'>
                                    <strong>Signal d'Achat :</strong> Quand le prix croise au-dessus des SMA (tendance haussière)
                                </li>
                                <li>
                                    <strong>Signal de Vente :</strong> Quand le prix croise en dessous des SMA (tendance baissière)
                                </li>
                            </ul>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Tab 2: Volume Chart
                    with chart_tab2:
                        st.markdown("""
                        <div style='background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px; 
                                    padding: 1.5rem; margin-bottom: 1.5rem; box-shadow: 0 1px 3px 0 rgba(0,0,0,0.05);'>
                            <h3 style='font-family: Inter, sans-serif; font-size: 1.125rem; font-weight: 600; 
                                      color: #2D3748; margin: 0 0 0.75rem 0;'>
                                Graphique du Volume de Transactions
                            </h3>
                            <p style='font-family: Inter, sans-serif; font-size: 0.875rem; color: #718096; margin: 0;'>
                                Analysez le volume de transactions quotidien pour comprendre l'intérêt des investisseurs.
                            </p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Create volume chart only
                        fig_volume = create_volume_chart(df, ticker)
                        st.plotly_chart(fig_volume, use_container_width=True)
                        
                        # Explanation card
                        st.markdown("""
                        <div style='background: #F0FFF4; border: 1px solid #C6F6D5; border-left: 4px solid #38A169; 
                                    padding: 1.25rem; border-radius: 8px; margin-top: 1.5rem;'>
                            <h4 style='font-family: Inter, sans-serif; color: #22543D; margin-bottom: 0.75rem; 
                                      font-size: 0.875rem; font-weight: 600;'>
                                💡 Comment Interpréter le Volume
                            </h4>
                            <ul style='font-family: Inter, sans-serif; color: #22543D; font-size: 0.875rem; 
                                      margin: 0; padding-left: 1.5rem;'>
                                <li style='margin-bottom: 0.5rem;'>
                                    <strong>Volume Élevé (Vert) :</strong> Beaucoup d'intérêt, souvent accompagné de mouvements de prix significatifs
                                </li>
                                <li style='margin-bottom: 0.5rem;'>
                                    <strong>Volume Faible (Rouge) :</strong> Peu d'activité, peut indiquer un manque d'intérêt
                                </li>
                                <li style='margin-bottom: 0.5rem;'>
                                    <strong>Confirmation de Tendance :</strong> Un volume élevé confirme la force d'une tendance
                                </li>
                                <li>
                                    <strong>Divergence :</strong> Si le prix monte mais le volume baisse, la tendance peut être faible
                                </li>
                            </ul>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Tab 3: RSI Chart
                    with chart_tab3:
                        st.markdown("""
                        <div style='background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px; 
                                    padding: 1.5rem; margin-bottom: 1.5rem; box-shadow: 0 1px 3px 0 rgba(0,0,0,0.05);'>
                            <h3 style='font-family: Inter, sans-serif; font-size: 1.125rem; font-weight: 600; 
                                      color: #2D3748; margin: 0 0 0.75rem 0;'>
                                Indicateur RSI (Relative Strength Index)
                            </h3>
                            <p style='font-family: Inter, sans-serif; font-size: 0.875rem; color: #718096; margin: 0;'>
                                Mesurez la force relative d'un actif pour identifier les conditions de surachat et de survente.
                            </p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Create RSI chart only
                        fig_rsi = create_rsi_chart(df, ticker)
                        st.plotly_chart(fig_rsi, use_container_width=True)
                        
                        # Explanation card
                        st.markdown("""
                        <div style='background: #FFFAF0; border: 1px solid #FEEBC8; border-left: 4px solid #DD6B20; 
                                    padding: 1.25rem; border-radius: 8px; margin-top: 1.5rem;'>
                            <h4 style='font-family: Inter, sans-serif; color: #7C2D12; margin-bottom: 0.75rem; 
                                      font-size: 0.875rem; font-weight: 600;'>
                                💡 Comment Interpréter le RSI
                            </h4>
                            <ul style='font-family: Inter, sans-serif; color: #7C2D12; font-size: 0.875rem; 
                                      margin: 0; padding-left: 1.5rem;'>
                                <li style='margin-bottom: 0.5rem;'>
                                    <strong>RSI > 70 (Zone Rouge) :</strong> Surachat - L'actif est peut-être surévalué, possibilité de correction
                                </li>
                                <li style='margin-bottom: 0.5rem;'>
                                    <strong>RSI < 30 (Zone Verte) :</strong> Survente - L'actif est peut-être sous-évalué, possibilité de rebond
                                </li>
                                <li style='margin-bottom: 0.5rem;'>
                                    <strong>RSI autour de 50 :</strong> Zone neutre, pas de signal fort
                                </li>
                                <li>
                                    <strong>Divergences :</strong> Si le prix monte mais le RSI baisse (ou vice versa), cela peut indiquer un changement de tendance
                                </li>
                            </ul>
                            <p style='font-family: Inter, sans-serif; color: #7C2D12; font-size: 0.75rem; 
                                     margin-top: 0.75rem; margin-bottom: 0; font-style: italic;'>
                                ⚠️ Le RSI est un indicateur, pas une garantie. Utilisez-le en combinaison avec d'autres analyses.
                            </p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Tab 4: Overview (Combined view)
                    with chart_tab4:
                        st.markdown("""
                        <div style='background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px; 
                                    padding: 1.5rem; margin-bottom: 1.5rem; box-shadow: 0 1px 3px 0 rgba(0,0,0,0.05);'>
                            <h3 style='font-family: Inter, sans-serif; font-size: 1.125rem; font-weight: 600; 
                                      color: #2D3748; margin: 0 0 0.75rem 0;'>
                                Vue d'Ensemble Complète
                            </h3>
                            <p style='font-family: Inter, sans-serif; font-size: 0.875rem; color: #718096; margin: 0;'>
                                Visualisez tous les indicateurs techniques ensemble pour une analyse complète.
                            </p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Create combined chart
                        fig_combined = create_price_chart(df, ticker)
                        st.plotly_chart(fig_combined, use_container_width=True)
                        
                        # Summary analysis
                        st.markdown("""
                        <div style='background: #F7FAFC; border: 1px solid #E2E8F0; border-radius: 12px; 
                                    padding: 1.5rem; margin-top: 1.5rem;'>
                            <h4 style='font-family: Inter, sans-serif; color: #1A202C; margin-bottom: 1rem; 
                                      font-size: 1rem; font-weight: 600;'>
                                📊 Analyse Technique Résumée
                            </h4>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Calculate current indicators
                        current_price = df['close'].iloc[-1]
                        sma_20_current = df['close'].rolling(window=20).mean().iloc[-1]
                        sma_50_current = df['close'].rolling(window=50).mean().iloc[-1]
                        
                        delta = df['close'].diff()
                        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                        rs = gain / loss
                        rsi_current = 100 - (100 / (1 + rs.iloc[-1]))
                        
                        analysis_col1, analysis_col2 = st.columns(2)
                        
                        with analysis_col1:
                            st.markdown("""
                            <div style='background: #FFFFFF; border: 1px solid #E2E8F0; padding: 1rem; border-radius: 8px;'>
                                <h5 style='font-family: Inter, sans-serif; color: #2D3748; font-size: 0.875rem; 
                                         font-weight: 600; margin-bottom: 0.75rem;'>Tendance</h5>
                            """, unsafe_allow_html=True)
                            
                            if current_price > sma_20_current > sma_50_current:
                                st.success("✅ **Tendance Haussière** - Le prix est au-dessus des moyennes mobiles")
                            elif current_price < sma_20_current < sma_50_current:
                                st.error("❌ **Tendance Baissière** - Le prix est en dessous des moyennes mobiles")
                            else:
                                st.warning("⚠️ **Tendance Neutre** - Le prix est entre les moyennes mobiles")
                        
                        with analysis_col2:
                            st.markdown("""
                            <div style='background: #FFFFFF; border: 1px solid #E2E8F0; padding: 1rem; border-radius: 8px;'>
                                <h5 style='font-family: Inter, sans-serif; color: #2D3748; font-size: 0.875rem; 
                                         font-weight: 600; margin-bottom: 0.75rem;'>RSI Actuel</h5>
                            """, unsafe_allow_html=True)
                            
                            if rsi_current > 70:
                                st.error(f"⚠️ **Surachat** - RSI: {rsi_current:.1f} (au-dessus de 70)")
                            elif rsi_current < 30:
                                st.success(f"✅ **Survente** - RSI: {rsi_current:.1f} (en dessous de 30)")
                            else:
                                st.info(f"ℹ️ **Neutre** - RSI: {rsi_current:.1f} (zone normale)")
                    
                    # Company info - Analytics Dashboard Card
                    st.markdown("""
                    <div style='margin-top: 1.5rem;'>
                        <h3 style='font-family: Inter, sans-serif; font-size: 1.125rem; 
                                   font-weight: 600; color: #2D3748; margin-bottom: 1rem;'>
                            Informations sur l'Entreprise
                        </h3>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Create info cards
                    info_col1, info_col2 = st.columns(2)
                    
                    with info_col1:
                        st.markdown("""
                        <div style='background: #FFFFFF; border: 1px solid #E2E8F0; 
                                    padding: 1.25rem; border-radius: 12px; 
                                    box-shadow: 0 1px 3px 0 rgba(0,0,0,0.05); margin-bottom: 1rem;'>
                        """, unsafe_allow_html=True)
                        st.markdown(f"**Nom:** {overview.get('name', 'N/A')}")
                        st.markdown(f"**Secteur:** {overview.get('sector', 'N/A')}")
                        st.markdown(f"**Industrie:** {overview.get('industry', 'N/A')}")
                        st.markdown("</div>", unsafe_allow_html=True)
                    
                    with info_col2:
                        st.markdown("""
                        <div style='background: #FFFFFF; border: 1px solid #E2E8F0; 
                                    padding: 1.25rem; border-radius: 12px; 
                                    box-shadow: 0 1px 3px 0 rgba(0,0,0,0.05); margin-bottom: 1rem;'>
                        """, unsafe_allow_html=True)
                        high_52w = overview.get('52_week_high', 'N/A')
                        low_52w = overview.get('52_week_low', 'N/A')
                        beta = overview.get('beta', 'N/A')
                        
                        st.markdown(f"**📊 52W High:** ${high_52w}" if high_52w != 'N/A' else f"**📊 52W High:** {high_52w}")
                        st.markdown(f"**📉 52W Low:** ${low_52w}" if low_52w != 'N/A' else f"**📉 52W Low:** {low_52w}")
                        st.markdown(f"**📈 Beta:** {beta}")
                        st.markdown("</div>", unsafe_allow_html=True)
                    
                    # Description in an expandable card
                    if overview.get('description'):
                        with st.expander("📝 Description de l'Entreprise", expanded=False):
                            st.markdown(overview['description'][:800] + ("..." if len(overview['description']) > 800 else ""))
                    
                except Exception as e:
                    show_error_with_solution(
                        f"Erreur lors de la récupération des données : {str(e)}",
                        """
                        **Solutions :**
                        1. Vérifiez que votre clé Alpha Vantage API est valide
                        2. Vérifiez que le symbole boursier est correct
                        3. Assurez-vous d'avoir une connexion Internet
                        4. Réessayez dans quelques instants (limite de taux API)
                        """
                    )
    
    # Tab 2: Financial Assistant (Chat) - Analytics Dashboard Style
    with tab2:
        st.markdown("""
        <div style='margin-bottom: 1.5rem;'>
            <h3 style='font-family: Inter, sans-serif; font-size: 1.125rem; 
                       font-weight: 600; color: #2D3748; margin-bottom: 0.75rem;'>
                Assistant Financier IA
            </h3>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div style='background: #EBF8FF; border: 1px solid #BEE3F8; padding: 1rem; 
                    border-radius: 8px; margin-bottom: 1.5rem; border-left: 4px solid #3182CE;'>
            <p style='margin: 0; color: #2C5282; font-family: Inter, sans-serif; font-size: 0.875rem;'>
                <strong>Astuce :</strong> Posez des questions en langage naturel sur le rapport annuel (10-K) 
                et les données de marché. L'assistant IA analysera automatiquement les documents et vous fournira 
                des réponses précises avec citations.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        if not ticker:
            show_info_card(
                "📋 Pour commencer",
                "Entrez un symbole boursier dans la sidebar (ex: AAPL, MSFT) et cliquez sur 'Lancer l'Analyse' pour charger le rapport 10-K."
            )
        else:
            # Initialize RAG system with progress feedback and better error handling
            if 'rag_retriever' not in st.session_state or st.session_state.get('current_ticker') != ticker:
                with st.spinner("🔄 Chargement du rapport 10-K et indexation... Cela peut prendre 30-60 secondes."):
                    try:
                    retriever, report_data = initialize_rag_system(ticker, llm)
                        if retriever and report_data:
                        st.session_state['rag_retriever'] = retriever
                        st.session_state['report_data'] = report_data
                        st.session_state['current_ticker'] = ticker
                        
                        # Initialize agent
                        agent = FinanceAgent(
                            rag_retriever=retriever,
                            alpha_vantage_client=alpha_client,
                            llm=llm,
                            verbose=False
                        )
                        st.session_state['agent'] = agent
                            show_success_message(f"Rapport 10-K pour {ticker} chargé et indexé avec succès ! Vous pouvez maintenant poser vos questions.")
                        else:
                            # Try alternative: use uploaded document if available
                            if 'report_data' in st.session_state and st.session_state['report_data']:
                                show_info_card(
                                    "Utilisation du document chargé",
                                    f"Le téléchargement automatique a échoué, mais un document est disponible. Vous pouvez l'utiliser ou télécharger manuellement dans l'onglet Explorateur de Documents."
                                )
                            else:
                                show_error_with_solution(
                                    "Impossible de charger le rapport 10-K automatiquement",
                                    """
                                    **Solutions :**
                                    1. **Téléchargement manuel** : Allez dans l'onglet "Explorateur de Documents" et téléchargez le rapport manuellement
                                    2. Vérifiez que le symbole boursier existe (ex: AAPL, MSFT, GOOGL)
                                    3. Assurez-vous d'avoir une connexion Internet stable
                                    4. Le rapport peut ne pas être disponible pour ce ticker sur SEC EDGAR
                                    """
                                )
                    except Exception as e:
                        error_msg = str(e)
                        # Provide more specific error messages
                        # Show helpful error message with manual upload option
                        st.markdown(f"""
                        <div style='background: #FFFAF0; border: 1px solid #FEEBC8; border-left: 4px solid #DD6B20; 
                                    padding: 1.25rem; border-radius: 8px; margin: 1rem 0;'>
                            <h4 style='font-family: Inter, sans-serif; color: #7C2D12; margin-bottom: 0.75rem; 
                                      font-size: 0.875rem; font-weight: 600;'>
                                ⚠️ Téléchargement Automatique Non Disponible
                            </h4>
                            <p style='font-family: Inter, sans-serif; color: #7C2D12; font-size: 0.875rem; margin-bottom: 0.75rem;'>
                                Le téléchargement automatique depuis SEC EDGAR n'est pas disponible pour le moment. 
                                Ceci est normal et peut être dû à des limitations de l'API ou des problèmes de réseau.
                            </p>
                            <div style='background: #FFFFFF; padding: 1rem; border-radius: 6px; margin-top: 0.75rem;'>
                                <p style='font-family: Inter, sans-serif; color: #1A202C; font-size: 0.875rem; 
                                         font-weight: 600; margin-bottom: 0.5rem;'>
                                    ✅ <strong>Solution : Upload Manuel</strong>
                                </p>
                                <ol style='font-family: Inter, sans-serif; color: #4A5568; font-size: 0.875rem; 
                                          margin: 0; padding-left: 1.5rem;'>
                                    <li style='margin-bottom: 0.5rem;'>
                                        Allez dans l'onglet <strong>"📄 Explorateur de Documents"</strong> (onglet à droite)
                                    </li>
                                    <li style='margin-bottom: 0.5rem;'>
                                        Téléchargez le rapport 10-K depuis 
                                        <a href='https://www.sec.gov/edgar/searchedgar/companysearch.html' 
                                           target='_blank' style='color: #3182CE; text-decoration: underline;'>SEC.gov</a>
                                        (recherchez "{ticker}" puis téléchargez le fichier HTML du 10-K)
                                    </li>
                                    <li style='margin-bottom: 0.5rem;'>
                                        Utilisez le bouton <strong>"Télécharger un fichier"</strong> dans l'onglet Explorateur
                                    </li>
                                    <li>
                                        Une fois uploadé, revenez ici et l'assistant IA fonctionnera automatiquement
                                    </li>
                                </ol>
                            </div>
                            <p style='font-family: Inter, sans-serif; color: #7C2D12; font-size: 0.75rem; 
                                     margin-top: 0.75rem; margin-bottom: 0; font-style: italic;'>
                                💡 Note : Vous pouvez toujours utiliser le Dashboard Marché (onglet 1) pour voir les données de marché même sans le rapport 10-K.
                            </p>
                        </div>
                        """, unsafe_allow_html=True)
            
            # Chat interface - Professional UX
            # Check if we have report data (from upload or download)
            if 'report_data' in st.session_state and st.session_state['report_data']:
                # Initialize RAG from existing report data if agent not initialized
                if 'rag_retriever' not in st.session_state or st.session_state.get('current_ticker') != ticker:
                    with st.spinner("🔄 Indexation du document pour l'assistant IA..."):
                        try:
                            report_data = st.session_state['report_data']
                            # Create documents
                            ingester = DocumentIngester()
                            documents = ingester.create_documents_from_sections(
                                sections=report_data['sections'],
                                base_metadata={'ticker': ticker, 'year': '2024'}
                            )
                            
                            # Ingest documents
                            collection_name = f"finsight_{ticker.lower()}"
                            index = ingester.ingest_documents(
                                documents=documents,
                                collection_name=collection_name,
                                reset=False
                            )
                            
                            # Create retriever
                            retriever = AdvancedRAGRetriever(
                                index=index,
                                llm=llm,
                                similarity_top_k=5,
                                rerank_top_k=3
                            )
                            st.session_state['rag_retriever'] = retriever
                            st.session_state['current_ticker'] = ticker
                            
                            # Initialize agent
                            agent = FinanceAgent(
                                rag_retriever=retriever,
                                alpha_vantage_client=alpha_client,
                                llm=llm,
                                verbose=False
                            )
                            st.session_state['agent'] = agent
                            show_success_message("Document indexé ! Vous pouvez maintenant poser vos questions.")
                        except Exception as e:
                            st.error(f"Erreur lors de l'indexation : {str(e)}")
            
            if 'agent' in st.session_state:
                # Initialize chat history
                if 'messages' not in st.session_state:
                    st.session_state.messages = []
                    # Welcome message
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": f"""
                        👋 Bonjour ! Je suis votre assistant financier IA pour **{ticker}**.
                        
                        Je peux répondre à vos questions sur :
                        - 📊 Les données de marché et les performances boursières
                        - 📄 Le rapport annuel 10-K (risques, stratégie, performance)
                        - 🔍 Des analyses combinées (marché + rapport)
                        
                        **Exemples de questions :**
                        - "Quels sont les principaux risques identifiés ?"
                        - "Quelle est la stratégie de croissance ?"
                        - "Compare la performance boursière avec les risques mentionnés"
                        
                        Posez votre question ci-dessous ! 💬
                        """
                    })
                
                # Display example questions
                if len(st.session_state.messages) == 1:
                    example_q = show_example_questions()
                    if example_q:
                        prompt = example_q
                    else:
                        prompt = None
                else:
                    prompt = None
                
                # Display chat history
                for message in st.session_state.messages:
                    with st.chat_message(message["role"]):
                        st.markdown(message["content"])
                
                # Chat input
                user_prompt = st.chat_input("💬 Posez votre question sur le rapport ou les données de marché...")
                
                if user_prompt or prompt:
                    final_prompt = user_prompt if user_prompt else prompt
                    # Add user message
                    st.session_state.messages.append({"role": "user", "content": final_prompt})
                    with st.chat_message("user"):
                        st.markdown(final_prompt)
                    
                    # Get agent response with better feedback
                    with st.chat_message("assistant"):
                        with st.spinner("🤔 Analyse en cours... L'assistant IA consulte les documents et les données de marché..."):
                            try:
                                response = st.session_state['agent'].chat(final_prompt)
                            st.markdown(response)
                            st.session_state.messages.append({"role": "assistant", "content": response})
                            except Exception as e:
                                error_msg = f"""
                                ❌ **Erreur lors de l'analyse**
                                
                                {str(e)}
                                
                                **Veuillez réessayer ou reformuler votre question.**
                                """
                                st.error(error_msg)
                                st.session_state.messages.append({"role": "assistant", "content": error_msg})
                
                # Chat actions
                col1, col2 = st.columns([1, 1])
                with col1:
                    if st.button("🗑️ Effacer l'historique", use_container_width=True):
                    st.session_state.messages = []
                    st.session_state['agent'].reset()
                    st.rerun()
    
                with col2:
                    if st.button("💡 Voir des exemples", use_container_width=True):
                        st.session_state.messages = []
                        st.rerun()
    
    # Tab 3: Document Explorer - Analytics Dashboard Style with Upload
    with tab3:
        st.markdown("""
        <div style='margin-bottom: 1.5rem;'>
            <h3 style='font-family: Inter, sans-serif; font-size: 1.125rem; 
                       font-weight: 600; color: #2D3748; margin-bottom: 0.75rem;'>
                Explorateur de Documents
            </h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Upload document option
        st.markdown("""
        <div style='background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px; 
                    padding: 1.5rem; margin-bottom: 1.5rem; box-shadow: 0 1px 3px 0 rgba(0,0,0,0.05);'>
            <h4 style='font-family: Inter, sans-serif; font-size: 1rem; font-weight: 600; 
                       color: #2D3748; margin-bottom: 0.75rem;'>
                📤 Ajouter un Document
            </h4>
            <p style='font-family: Inter, sans-serif; font-size: 0.875rem; color: #718096; margin-bottom: 1rem;'>
                Vous pouvez télécharger un rapport 10-K manuellement ou utiliser le téléchargement automatique.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        upload_col1, upload_col2 = st.columns([2, 1])
        
        with upload_col1:
            uploaded_file = st.file_uploader(
                "Télécharger un fichier (HTML, TXT, PDF)",
                type=['html', 'htm', 'txt', 'pdf'],
                help="Téléchargez un rapport 10-K au format HTML, TXT ou PDF"
            )
        
        with upload_col2:
            if st.button("📥 Télécharger depuis SEC", use_container_width=True):
                if ticker:
                    with st.spinner(f"Téléchargement du rapport 10-K pour {ticker}..."):
                        try:
                            sec_client = SecEdgarClient()
                            html_path = sec_client.download_10k(ticker)
                            if html_path:
                                st.success(f"✅ Rapport téléchargé : {html_path}")
                                # Parse and store
                                report_data = sec_client.parse_10k_html(html_path)
                                st.session_state['report_data'] = report_data
                                st.session_state['current_ticker'] = ticker
                                st.rerun()
                        except Exception as e:
                            st.error(f"Erreur : {str(e)}")
        else:
                    st.warning("Veuillez entrer un symbole boursier dans la sidebar")
        
        # Process uploaded file
        if uploaded_file is not None:
            try:
                # Read file content
                if uploaded_file.type == "text/html" or uploaded_file.name.endswith(('.html', '.htm')):
                    content = uploaded_file.read().decode('utf-8', errors='ignore')
                    # Parse HTML
                    sec_client = SecEdgarClient()
                    # Save temporarily
                    temp_path = os.path.join("data/raw", f"uploaded_{uploaded_file.name}")
                    os.makedirs("data/raw", exist_ok=True)
                    with open(temp_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    report_data = sec_client.parse_10k_html(temp_path)
                    st.session_state['report_data'] = report_data
                    st.session_state['current_ticker'] = uploaded_file.name.replace('.html', '').replace('.htm', '')
                    st.success("✅ Document chargé avec succès !")
                    st.rerun()
                elif uploaded_file.type == "text/plain" or uploaded_file.name.endswith('.txt'):
                    content = uploaded_file.read().decode('utf-8', errors='ignore')
                    # Create simple document structure
                    report_data = {
                        'sections': {'Document Complet': content},
                        'full_text': content,
                        'metadata': {
                            'file_path': uploaded_file.name,
                            'parsed_date': datetime.now().isoformat(),
                            'total_length': len(content)
                        }
                    }
                    st.session_state['report_data'] = report_data
                    st.session_state['current_ticker'] = uploaded_file.name.replace('.txt', '')
                    st.success("✅ Document texte chargé avec succès !")
                    st.rerun()
            except Exception as e:
                st.error(f"Erreur lors du traitement du fichier : {str(e)}")
        
        st.divider()
        
        # Display existing report
        if 'report_data' in st.session_state and st.session_state['report_data']:
                report_data = st.session_state['report_data']
            current_ticker = st.session_state.get('current_ticker', ticker if ticker else 'Document')
            
            st.markdown("""
            <div style='background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px; 
                        padding: 1.5rem; margin-bottom: 1.5rem; box-shadow: 0 1px 3px 0 rgba(0,0,0,0.05);'>
                <h4 style='font-family: Inter, sans-serif; font-size: 1rem; font-weight: 600; 
                          color: #2D3748; margin-bottom: 0.5rem;'>
                    Document Chargé
                </h4>
                <p style='font-family: Inter, sans-serif; font-size: 0.875rem; color: #718096; margin: 0;'>
                    <strong>Source:</strong> {current_ticker} • 
                    <strong>Longueur:</strong> {total_length:,} caractères
                </p>
            </div>
            """.format(
                current_ticker=current_ticker,
                total_length=report_data['metadata']['total_length']
            ), unsafe_allow_html=True)
                
                # Display sections
            st.markdown("""
            <div style='margin-top: 1.5rem;'>
                <h4 style='font-family: Inter, sans-serif; font-size: 1rem; font-weight: 600; 
                           color: #2D3748; margin-bottom: 1rem;'>
                    Sections du Document
                </h4>
            </div>
            """, unsafe_allow_html=True)
            
                for section_name, section_text in report_data['sections'].items():
                with st.expander(f"📑 {section_name}", expanded=False):
                        st.text_area(
                            "Contenu",
                        value=section_text[:5000] + "..." if len(section_text) > 5000 else section_text,
                        height=300,
                        disabled=True,
                        key=f"section_{section_name}"
                    )
                    st.caption(f"Longueur : {len(section_text):,} caractères")
        elif not ticker:
            show_info_card(
                "Pour commencer",
                "Entrez un symbole boursier dans la sidebar et cliquez sur 'Lancer l'Analyse', ou téléchargez un document manuellement ci-dessus."
                        )
            else:
            show_info_card(
                "Aucun document chargé",
                "Lancez l'analyse dans l'onglet Dashboard pour charger automatiquement le rapport 10-K, ou téléchargez un document manuellement ci-dessus."
            )


if __name__ == "__main__":
    main()

