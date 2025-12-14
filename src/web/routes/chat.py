"""
Chat/Assistant routes for Flask application
"""
from flask import Blueprint, request, jsonify, session
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from src.agents.finance_agent import FinanceAgent
from src.rag.ingestion import DocumentIngester
from src.rag.retrieval import AdvancedRAGRetriever
from llama_index.core import QueryBundle
from src.data.alpha_vantage import AlphaVantageClient
from src.data.sec_edgar import SecEdgarClient
from llama_index.llms.gemini import Gemini
from llama_index.core.llms import LLM

bp = Blueprint('chat', __name__, url_prefix='/api/chat')

# Store agents in memory (in production, use Redis or database)
_agents_cache = {}
_rag_retrievers_cache = {}

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

def get_agent(ticker: str):
    """Get or create agent for ticker"""
    if ticker in _agents_cache:
        return _agents_cache[ticker]
    return None

def initialize_rag_system(ticker: str):
    """Initialize RAG system for a ticker"""
    try:
        # Check if already initialized
        if ticker in _rag_retrievers_cache:
            return _rag_retrievers_cache[ticker], True
        
        # Initialize LLM (optional). It's fine if no GEMINI_API_KEY is configured;
        # in that case we will still ingest SEC files and allow raw-context answers.
        llm = initialize_llm()
        
        # Get 10-K report
        sec_client = SecEdgarClient()
        report_data = sec_client.get_10k_text(ticker)
        
        # Check if we got valid data
        if not report_data.get('sections') or len(report_data.get('sections', {})) == 0:
            raise ValueError("No valid report data retrieved")
        
        # Check if it's an error message section
        sections = report_data.get('sections', {})
        if 'Note' in sections and 'téléchargement automatique a échoué' in sections.get('Note', ''):
            # Indicate automatic download failed; do not prompt for manual upload
            raise ValueError("Le téléchargement automatique du rapport 10-K a échoué. Vérifiez le symbole boursier ou réessayez plus tard.")
        
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
        
        # Diagnostic retrieval: verify index returns nodes even before creating main retriever
        try:
            test_retriever = AdvancedRAGRetriever(index=index, llm=None, similarity_top_k=5, rerank_top_k=3)
            test_qb = QueryBundle(query_str="Quelle est la stratégie de croissance de cette entreprise ?")
            try:
                test_nodes = test_retriever.retriever.retrieve(test_qb)
                print(f"[RAG init] Diagnostic: retrieved {len(test_nodes)} nodes for ticker {ticker}")
                if test_nodes:
                    try:
                        snippet = test_nodes[0].get_content()[:200]
                    except Exception:
                        snippet = str(test_nodes[0])[:200]
                    print(f"[RAG init] Sample node meta={getattr(test_nodes[0], 'metadata', {})} snippet={snippet!r}")
            except Exception as e:
                print(f"[RAG init] Diagnostic retrieval failed: {e}")
        except Exception as e:
            print(f"[RAG init] Could not create diagnostic retriever: {e}")

        # Create retriever used by the agent
        retriever = AdvancedRAGRetriever(
            index=index,
            llm=llm,
            similarity_top_k=5,
            rerank_top_k=3
        )
        
        # Cache retriever
        _rag_retrievers_cache[ticker] = retriever
        
        return retriever, report_data
        
    except ValueError as e:
        raise ValueError(f"RAG initialization failed: {e}")
    except Exception as e:
        raise RuntimeError(f"Error initializing RAG system: {e}")

@bp.route('/message', methods=['POST'])
def send_message():
    """Send message to financial assistant"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        ticker = data.get('ticker', session.get('ticker', ''))
        
        if not ticker:
            return jsonify({
                'error': 'Ticker not specified',
                'response': 'Veuillez d\'abord sélectionner un symbole boursier dans la sidebar et lancer l\'analyse.'
            }), 400
        
        # Get or initialize agent
        agent = get_agent(ticker)
        if not agent:
            # Try to initialize agent
            try:
                # Initialize RAG system (this also ingests SEC files if needed)
                retriever, _ = initialize_rag_system(ticker)

                # Initialize clients
                llm = initialize_llm()  # may be None

                # If no LLM configured, skip creating the full FinanceAgent and
                # answer directly from the indexed SEC files (raw-context + sources).
                alpha_client = AlphaVantageClient()

                if not llm:
                    # Create a lightweight placeholder in cache so we don't re-ingest repeatedly
                    _agents_cache[ticker] = None
                else:
                    # Create the full agent when LLM is available
                    agent = FinanceAgent(
                        rag_retriever=retriever,
                        alpha_vantage_client=alpha_client,
                        llm=llm,
                        verbose=False
                    )
                    _agents_cache[ticker] = agent
            except ValueError as e:
                error_msg = str(e)
                # Inform user that automatic download failed and ask to verify ticker/network
                return jsonify({
                    'error': 'RAG initialization failed',
                    'response': (
                        '❌ Le téléchargement automatique du rapport 10-K a échoué. '
                        'Vérifiez le symbole boursier, votre connexion réseau, puis réessayez. '
                        f'Détails: {error_msg}'
                    )
                }), 400
            except RuntimeError as e:
                error_msg = str(e)
                if 'from_tools' in error_msg.lower() or 'ReActAgent' in error_msg:
                    return jsonify({
                        'error': 'Agent initialization failed',
                        'response': f'❌ Erreur lors de l\'initialisation de l\'agent.\n\n💡 **Problème technique :** Incompatibilité avec la version de LlamaIndex.\n\n🔧 **Solution :**\n1. Vérifiez que LlamaIndex est à jour : `pip install --upgrade llama-index`\n2. Redémarrez l\'application\n3. Si le problème persiste, contactez le support technique.\n\nDétails: {error_msg}'
                    }), 500
                else:
                    return jsonify({
                        'error': 'Agent initialization failed',
                        'response': f'❌ Erreur lors de l\'initialisation de l\'agent: {error_msg}'
                    }), 500
            except Exception as e:
                return jsonify({
                    'error': 'Agent initialization failed',
                    'response': f'❌ Erreur lors de l\'initialisation de l\'agent: {str(e)}'
                }), 500
        
        # Get response from agent (use chat method) OR fallback to direct retrieval
        try:
            # If agent exists and is a FinanceAgent instance, use it
            agent = _agents_cache.get(ticker)
            if agent is None:
                # No LLM/agent available: perform direct retrieval and return context + sources
                retriever = _rag_retrievers_cache.get(ticker)
                if not retriever:
                    return jsonify({
                        'error': 'retriever_missing',
                        'response': 'Système RAG non initialisé pour ce ticker.'
                    }), 500

                # Run retrieval (AdvancedRAGRetriever.query handles llm=None)
                try:
                    raw_response = retriever.query(message)
                except Exception as e:
                    return jsonify({
                        'error': 'retrieval_failed',
                        'response': f'Erreur lors de la récupération: {str(e)}'
                    }), 500

                # Collect source nodes for attribution
                try:
                    nodes = retriever.retriever.retrieve(QueryBundle(query_str=message))
                    sources = []
                    for n in nodes[:5]:
                        meta = getattr(n, 'metadata', {}) or {}
                        section = meta.get('section') or meta.get('title') or 'Unknown section'
                        ticker_meta = meta.get('ticker') or ''
                        snippet = n.get_content()[:200].replace('\n', ' ')
                        src = f"Section: {section}"
                        if ticker_meta:
                            src += f" (Ticker: {ticker_meta})"
                        src += f" — \"{snippet}...\""
                        sources.append(src)
                    sources_text = "\n".join([f"- {s}" for s in sources]) if sources else ''
                except Exception:
                    sources_text = ''

                response_text = str(raw_response)
                if sources_text:
                    response_text = f"{response_text}\n\n**Sources :**\n{sources_text}"

                return jsonify({
                    'response': response_text,
                    'ticker': ticker
                })

            # Otherwise use the agent.chat path
            response = agent.chat(message)
            response_str = str(response)

            # If agent signals no information found, fallback to raw retrieval + sources
            lower_resp = response_str.lower() if isinstance(response_str, str) else ''
            if 'aucune information trouv' in lower_resp or lower_resp.strip().startswith('❌'):
                retriever = _rag_retrievers_cache.get(ticker)
                if retriever:
                    try:
                        raw_response = retriever.query(message)
                    except Exception as e:
                        return jsonify({
                            'error': 'retrieval_failed',
                            'response': f'Erreur lors de la récupération: {str(e)}'
                        }), 500

                    # Collect source nodes
                    try:
                        nodes = retriever.retriever.retrieve(QueryBundle(query_str=message))
                        sources = []
                        for n in nodes[:5]:
                            meta = getattr(n, 'metadata', {}) or {}
                            section = meta.get('section') or meta.get('title') or 'Unknown section'
                            ticker_meta = meta.get('ticker') or ''
                            snippet = n.get_content()[:200].replace('\n', ' ')
                            src = f"Section: {section}"
                            if ticker_meta:
                                src += f" (Ticker: {ticker_meta})"
                            src += f" — \"{snippet}...\""
                            sources.append(src)
                        sources_text = "\n".join([f"- {s}" for s in sources]) if sources else ''
                    except Exception:
                        sources_text = ''

                    response_text = str(raw_response)
                    if sources_text:
                        response_text = f"{response_text}\n\n**Sources :**\n{sources_text}"

                    return jsonify({
                        'response': response_text,
                        'ticker': ticker
                    })

            return jsonify({
                'response': response_str,
                'ticker': ticker
            })
        except Exception as e:
            return jsonify({
                'error': 'Query failed',
                'response': f'Erreur lors de la génération de la réponse: {str(e)}'
            }), 500
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'response': f'Erreur inattendue: {str(e)}'
        }), 500

@bp.route('/initialize/<ticker>', methods=['POST'])
def initialize_rag(ticker):
    """Initialize RAG system for ticker"""
    try:
        # Initialize RAG system
        retriever, report_data = initialize_rag_system(ticker)
        
        # Initialize LLM
        llm = initialize_llm()
        if not llm:
            return jsonify({
                'error': 'LLM not initialized',
                'message': 'Please configure GEMINI_API_KEY'
            }), 400
        
        # Initialize clients
        alpha_client = AlphaVantageClient()
        
        # Create agent
        agent = FinanceAgent(
            rag_retriever=retriever,
            alpha_vantage_client=alpha_client,
            llm=llm,
            verbose=False
        )
        
        # Cache agent
        _agents_cache[ticker] = agent
        
        return jsonify({
            'success': True,
            'message': f'RAG system and agent initialized for {ticker}',
            'sections_count': len(report_data.get('sections', {}))
        })
    except ValueError as e:
        return jsonify({
            'error': str(e),
            'message': f'RAG initialization failed: {str(e)}'
        }), 400
    except Exception as e:
        return jsonify({
            'error': str(e),
            'message': f'Error: {str(e)}'
        }), 500

