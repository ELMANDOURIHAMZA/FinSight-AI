"""
ReAct Agent for autonomous financial analysis
"""
import asyncio
import threading
from typing import Optional, List
from llama_index.core.agent import ReActAgent
from llama_index.core.llms import LLM
from llama_index.core.tools import FunctionTool
from src.rag.retrieval import AdvancedRAGRetriever
from src.data.alpha_vantage import AlphaVantageClient
from src.agents.tools import get_all_tools

# Try to import AgentRunner and AgentChatEngine if available
try:
    from llama_index.core.agent import AgentRunner
    HAS_AGENT_RUNNER = True
except ImportError:
    HAS_AGENT_RUNNER = False

try:
    from llama_index.core.agent import AgentChatEngine
    HAS_AGENT_CHAT_ENGINE = True
except ImportError:
    HAS_AGENT_CHAT_ENGINE = False

# Note: Some imports may not be available in all LlamaIndex versions


class FinanceAgent:
    """
    Autonomous financial analyst agent using ReAct pattern
    """
    
    SYSTEM_PROMPT = """You are an expert financial analyst AI assistant. Your goal is to provide 
    accurate, well-reasoned insights about companies and their financial performance.

Key principles:
1. Always use the provided tools to gather factual information before making claims
2. When analyzing reports, cite specific sections and page numbers when available
3. Combine quantitative market data with qualitative report insights when answering questions
4. If information is not available in the tools, clearly state "I don't have access to that information"
5. Never make up numbers or facts - always rely on tool outputs
6. Format your responses professionally using markdown
7. When comparing data, provide specific numbers and percentages
8. Highlight risks and opportunities clearly

Your responses should be:
- Professional and objective
- Well-structured with clear sections
- Supported by evidence from tools
- Actionable when appropriate"""

    def __init__(
        self,
        rag_retriever: AdvancedRAGRetriever,
        alpha_vantage_client: AlphaVantageClient,
        llm: LLM,
        verbose: bool = True
    ):
        """
        Initialize the finance agent
        
        Args:
            rag_retriever: AdvancedRAGRetriever instance for report analysis
            alpha_vantage_client: AlphaVantageClient instance for market data
            llm: LLM instance for reasoning
            verbose: Whether to print agent reasoning steps
        """
        self.rag_retriever = rag_retriever
        self.alpha_vantage_client = alpha_vantage_client
        self.llm = llm
        self.verbose = verbose
        
        # Get all tools
        tools = get_all_tools(
            rag_retriever=rag_retriever,
            alpha_vantage_client=alpha_vantage_client,
            llm=llm
        )
        
        # Try to create AgentChatEngine first (newer API)
        self.agent = None
        self.chat_engine = None
        
        # Method 1: Try AgentChatEngine (newer LlamaIndex versions)
        if HAS_AGENT_CHAT_ENGINE:
            try:
                self.chat_engine = AgentChatEngine.from_tools(
                    tools=tools,
                    llm=llm,
                    verbose=verbose,
                    system_prompt=self.SYSTEM_PROMPT
                )
                print("Using AgentChatEngine")
                return  # Success, exit early
            except Exception as e:
                print(f"AgentChatEngine failed: {e}, trying ReActAgent...")
        
        # Method 2: Create ReAct agent
        # Handle different LlamaIndex versions and API changes
        try:
            # Check if from_tools method exists
            if hasattr(ReActAgent, 'from_tools'):
                # Method 1: from_tools (LlamaIndex 0.10+)
                try:
                    self.agent = ReActAgent.from_tools(
                        tools=tools,
                        llm=llm,
                        verbose=verbose,
                        system_prompt=self.SYSTEM_PROMPT,
                        max_iterations=10
                    )
                except TypeError as e:
                    # Try with different parameter names
                    try:
                        self.agent = ReActAgent.from_tools(
                            tool_list=tools,
                            llm=llm,
                            verbose=verbose,
                            system_prompt=self.SYSTEM_PROMPT,
                            max_iterations=10
                        )
                    except Exception:
                        # Fallback to direct initialization
                        self.agent = ReActAgent(
                            tools=tools,
                            llm=llm,
                            verbose=verbose,
                            system_prompt=self.SYSTEM_PROMPT,
                            max_iterations=10
                        )
            else:
                # Method 2: Direct initialization (older versions)
                self.agent = ReActAgent(
                    tools=tools,
                    llm=llm,
                    verbose=verbose,
                    system_prompt=self.SYSTEM_PROMPT,
                    max_iterations=10
                )
        except Exception as e:
            # Last resort: try with minimal parameters
            try:
                self.agent = ReActAgent(
                    tools=tools,
                    llm=llm,
                    verbose=verbose
                )
            except Exception as e2:
                raise RuntimeError(
                    f"Failed to initialize ReActAgent: {str(e)}. "
                    f"Fallback also failed: {str(e2)}. "
                    f"Please ensure LlamaIndex is properly installed and check the version compatibility."
                )
    
    def _run_with_event_loop(self, coro):
        """Run async code with proper event loop handling"""
        try:
            # Try to get the current event loop
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # If loop is already running, we need to use a different approach
                # Create a new thread with a new event loop
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(asyncio.run, coro)
                    return future.result(timeout=300)  # 5 minute timeout
            else:
                # Loop exists but not running, we can use it
                return loop.run_until_complete(coro)
        except RuntimeError:
            # No event loop exists, create a new one
            return asyncio.run(coro)
    
    def _execute_tools_directly(self, message: str) -> str:
        """
        Execute tools directly without using ReActAgent
        This is a workaround for LlamaIndex version compatibility issues
        """
        # Get tools
        tools = get_all_tools(
            rag_retriever=self.rag_retriever,
            alpha_vantage_client=self.alpha_vantage_client,
            llm=self.llm
        )
        
        # Analyze the question to determine which tools to use
        message_lower = message.lower()
        
        # Check if question is about 10-K report
        report_keywords = ['stratégie', 'croissance', 'risque', 'revenu', 'performance', 
                          'entreprise', 'business', 'secteur', 'marché', 'concurrent',
                          'rapport', '10-k', 'annuel', 'financier']
        is_report_question = any(keyword in message_lower for keyword in report_keywords)
        
        # Check if question is about market data
        market_keywords = ['prix', 'cours', 'action', 'bourse', 'volume', 'capitalisation',
                          'pe ratio', 'dividende', 'tendance', 'graphique', 'indicateur']
        is_market_question = any(keyword in message_lower for keyword in market_keywords)
        
        # Collect information from tools
        report_info = ""
        market_info = ""
        
        # Get report information if relevant
        if is_report_question:
            try:
                # Try direct RAG query first (most reliable)
                try:
                    report_info = self.rag_retriever.query(message)
                        # Check if response is meaningful
                    if report_info and len(str(report_info).strip()) > 20:
                            # Good response, attach sources if available
                            try:
                                # Attempt to retrieve source nodes for attribution
                                nodes = self.rag_retriever.retrieve_with_metadata_filter(message)
                                if nodes and len(nodes) > 0:
                                    sources = []
                                    for n in nodes[:5]:
                                        meta = getattr(n, 'metadata', {}) or {}
                                        section = meta.get('section') or meta.get('title') or meta.get('part') or 'Unknown section'
                                        ticker = meta.get('ticker') or meta.get('symbol') or ''
                                        snippet = n.get_content()[:200].replace('\n', ' ')
                                        src_desc = f"Section: {section}"
                                        if ticker:
                                            src_desc += f" (Ticker: {ticker})"
                                        src_desc += f" — \"{snippet}...\""
                                        sources.append(src_desc)
                                    sources_text = "\n".join([f"- {s}" for s in sources])
                                    report_info = f"{report_info}\n\n**Sources :**\n{sources_text}"
                            except Exception as src_err:
                                # If sources can't be fetched, ignore and return original report_info
                                print(f"Could not fetch source nodes for attribution: {src_err}")
                    else:
                            # Empty or too short, try tool
                            report_info = ""
                except Exception as rag_error:
                    print(f"Direct RAG query failed: {rag_error}")
                    report_info = ""
                
                # If RAG didn't work, try tool
                if not report_info or len(str(report_info).strip()) < 20:
                    for tool in tools:
                        tool_name = tool.metadata.name if hasattr(tool, 'metadata') and hasattr(tool.metadata, 'name') else (tool.name if hasattr(tool, 'name') else '')
                        if 'analyze' in tool_name.lower() or '10k' in tool_name.lower() or 'report' in tool_name.lower():
                            try:
                                tool_result = tool.fn(question=message)
                                if tool_result and len(str(tool_result).strip()) > 20:
                                    report_info = tool_result
                                    break
                            except Exception as e:
                                print(f"Tool execution error: {e}")
            except Exception as e:
                print(f"Error getting report info: {e}")
                report_info = ""
        
        # Get market information if relevant
        if is_market_question:
            try:
                # Try to extract ticker from context (this could be improved)
                # For now, we'll skip market data if no ticker is available
                # The market tools require a ticker symbol
                pass
            except Exception as e:
                print(f"Error getting market info: {e}")
        
        # Combine information and generate response
        from llama_index.core.llms import ChatMessage
        
        # Build context
        context_parts = []
        if report_info:
            context_parts.append(f"**Informations du rapport 10-K :**\n{str(report_info)}")
        if market_info:
            context_parts.append(f"**Données de marché :**\n{str(market_info)}")
        
        context = "\n\n".join(context_parts) if context_parts else ""
        
        # Create prompt
        if context and len(context.strip()) > 50:
            prompt = f"{self.SYSTEM_PROMPT}\n\n{context}\n\n**Question de l'utilisateur :** {message}\n\n**Réponse :**"
        else:
            # If no context, try RAG directly with multiple attempts
            rag_response = None
            try:
                rag_response = self.rag_retriever.query(message)
                if rag_response and len(str(rag_response).strip()) > 50:
                    # Try to fetch source nodes and append attribution
                    try:
                        nodes = self.rag_retriever.retrieve_with_metadata_filter(message)
                        if nodes and len(nodes) > 0:
                            sources = []
                            for n in nodes[:5]:
                                meta = getattr(n, 'metadata', {}) or {}
                                section = meta.get('section') or meta.get('title') or meta.get('part') or 'Unknown section'
                                ticker = meta.get('ticker') or meta.get('symbol') or ''
                                snippet = n.get_content()[:200].replace('\n', ' ')
                                src_desc = f"Section: {section}"
                                if ticker:
                                    src_desc += f" (Ticker: {ticker})"
                                src_desc += f" — \"{snippet}...\""
                                sources.append(src_desc)
                            sources_text = "\n".join([f"- {s}" for s in sources])
                            return f"**Réponse basée sur le rapport 10-K :**\n\n{str(rag_response)}\n\n**Sources :**\n{sources_text}"
                    except Exception as src_err:
                        print(f"Could not fetch source nodes for attribution: {src_err}")
                    return f"**Réponse basée sur le rapport 10-K :**\n\n{str(rag_response)}"
            except Exception as e:
                print(f"RAG query error: {e}")
            
            # If RAG returned empty, provide helpful message
            if not rag_response or len(str(rag_response).strip()) < 50:
                return "❌ **Aucune information trouvée**\n\nJe n'ai pas pu trouver d'informations pertinentes dans le rapport 10-K pour répondre à votre question.\n\n**Suggestions :**\n1. Vérifiez que le rapport 10-K a été correctement chargé dans l'onglet 'Explorateur de Documents'\n2. Reformulez votre question avec des termes plus spécifiques\n3. Essayez des questions comme :\n   - 'Quels sont les principaux risques de cette entreprise ?'\n   - 'Quelle est la stratégie de l'entreprise ?'\n   - 'Quels sont les revenus de cette entreprise ?'"
            
            prompt = f"{self.SYSTEM_PROMPT}\n\n**Question de l'utilisateur :** {message}\n\n**Réponse :**"
        
        # Get response from LLM
        try:
            messages = [
                ChatMessage(role="system", content=prompt),
                ChatMessage(role="user", content=message)
            ]
            
            if hasattr(self.llm, 'chat'):
                response = self.llm.chat(messages)
                return self._extract_response_text(response)
            elif hasattr(self.llm, 'complete'):
                response = self.llm.complete(prompt)
                return str(response)
        except Exception as e:
            print(f"LLM call failed: {e}")
            # Last resort: return RAG response if available
            if report_info:
                return f"**Réponse basée sur le rapport 10-K :**\n\n{str(report_info)}"
            return f"Erreur lors de la génération de la réponse: {str(e)}"
    
    def chat(self, message: str) -> str:
        """
        Chat with the agent
        
        Args:
            message: User message/question
            
        Returns:
            Agent response
        """
        try:
            # Method 1: Try AgentChatEngine first (if available)
            if self.chat_engine is not None:
                try:
                    if hasattr(self.chat_engine, 'chat'):
                        response = self.chat_engine.chat(message)
                        return self._extract_response_text(response)
                    elif hasattr(self.chat_engine, 'stream_chat'):
                        response_parts = []
                        for chunk in self.chat_engine.stream_chat(message):
                            response_parts.append(self._extract_response_text(chunk))
                        return ''.join(response_parts)
                except Exception as e:
                    print(f"AgentChatEngine failed: {e}, using direct tool execution...")
            
            # Method 2: Try ReActAgent methods (if available)
            if self.agent is not None:
                # Try standard methods first
                for method_name in ['run', 'query', 'chat', 'stream_chat', 'stream_query']:
                    if hasattr(self.agent, method_name):
                        try:
                            method = getattr(self.agent, method_name)
                            if asyncio.iscoroutinefunction(method):
                                response = self._run_with_event_loop(method(message))
                            else:
                                response = method(message)
                            
                            # Handle streaming responses
                            if hasattr(response, '__iter__') and not isinstance(response, str):
                                response_parts = []
                                for chunk in response:
                                    response_parts.append(self._extract_response_text(chunk))
                                return ''.join(response_parts)
                            
                            return self._extract_response_text(response)
                        except Exception as e:
                            error_str = str(e).lower()
                            if 'not callable' not in error_str and 'event loop' not in error_str:
                                continue  # Try next method
                            if 'event loop' in error_str:
                                try:
                                    if asyncio.iscoroutinefunction(method):
                                        response = asyncio.run(method(message))
                                    else:
                                        response = method(message)
                                    return self._extract_response_text(response)
                                except:
                                    continue
            
            # Method 3: Use direct tool execution (workaround for LlamaIndex compatibility)
            print("Using direct tool execution (ReActAgent not compatible)")
            return self._execute_tools_directly(message)
            
        except Exception as e:
            error_msg = str(e)
            print(f"Chat error: {error_msg}")
            # Try direct RAG as last resort
            try:
                rag_response = self.rag_retriever.query(message)
                if rag_response:
                    return f"**Réponse basée sur le rapport 10-K :**\n\n{str(rag_response)}"
            except:
                pass
            
            if 'event loop' in error_msg.lower():
                return f"Erreur technique : Problème de gestion asynchrone. Veuillez réessayer ou contacter le support. Détails: {error_msg}"
            return f"Erreur lors de l'exécution: {error_msg}"
    
    def _extract_response_text(self, response) -> str:
        """Extract text from various response object types"""
        if isinstance(response, str):
            return response
        
        # Try common response attributes
        if hasattr(response, 'response'):
            return str(response.response)
        if hasattr(response, 'output'):
            return str(response.output)
        if hasattr(response, 'text'):
            return str(response.text)
        if hasattr(response, 'message'):
            return str(response.message)
        if hasattr(response, 'source_nodes'):
            # It's a Response object, try to get the response text
            return str(response)
        
        # Last resort: convert to string
        return str(response)
    
    def stream_chat(self, message: str):
        """
        Stream chat response (for real-time UI updates)
        
        Args:
            message: User message/question
            
        Yields:
            Response chunks
        """
        try:
            if hasattr(self.agent, 'stream_chat'):
                response_stream = self.agent.stream_chat(message)
                for chunk in response_stream:
                    if hasattr(chunk, 'response'):
                        yield str(chunk.response)
                    else:
                        yield str(chunk)
            elif hasattr(self.agent, 'stream_query'):
                response_stream = self.agent.stream_query(message)
                for chunk in response_stream:
                    if hasattr(chunk, 'response'):
                        yield str(chunk.response)
                    else:
                        yield str(chunk)
            else:
                # Fallback: use regular query and yield as single chunk
                response = self.chat(message)
                yield response
        except Exception as e:
            yield f"Error: {str(e)}"
    
    def reset(self):
        """Reset agent conversation history"""
        self.agent.reset()




