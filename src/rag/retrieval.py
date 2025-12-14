"""
RAG retrieval configuration with advanced features
"""
from typing import Optional, List
import re
from llama_index.core import VectorStoreIndex, QueryBundle
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.response_synthesizers import ResponseMode
from llama_index.core.postprocessor import SimilarityPostprocessor
from llama_index.core.llms import LLM


class AdvancedRAGRetriever:
    """
    Advanced RAG retriever with reranking and metadata filtering
    """
    
    def __init__(
        self,
        index: VectorStoreIndex,
        llm: Optional[LLM] = None,
        similarity_top_k: int = 5,
        rerank_top_k: int = 3
    ):
        """
        Initialize the advanced retriever
        
        Args:
            index: VectorStoreIndex instance
            llm: LLM instance for synthesis
            similarity_top_k: Number of top similar chunks to retrieve
            rerank_top_k: Number of chunks to keep after reranking
        """
        self.index = index
        self.llm = llm
        self.similarity_top_k = similarity_top_k
        self.rerank_top_k = rerank_top_k
        
        # Create retriever
        self.retriever = VectorIndexRetriever(
            index=index,
            similarity_top_k=similarity_top_k
        )
        
        # Create postprocessor for similarity filtering
        self.postprocessor = SimilarityPostprocessor(
            similarity_cutoff=0.7  # Minimum similarity threshold
        )
    
    def create_query_engine(
        self,
        response_mode: ResponseMode = ResponseMode.COMPACT,
        streaming: bool = False
    ) -> RetrieverQueryEngine:
        """
        Create a query engine with the configured retriever
        
        Args:
            response_mode: Response synthesis mode
            streaming: Whether to enable streaming responses
            
        Returns:
            RetrieverQueryEngine instance
        """
        query_engine = RetrieverQueryEngine.from_args(
            retriever=self.retriever,
            node_postprocessors=[self.postprocessor],
            response_mode=response_mode,
            streaming=streaming,
            llm=self.llm
        )
        
        return query_engine
    
    def retrieve_with_metadata_filter(
        self,
        query: str,
        metadata_filters: Optional[dict] = None
    ) -> List:
        """
        Retrieve nodes with metadata filtering
        
        Args:
            query: Query string
            metadata_filters: Dictionary of metadata filters (e.g., {'section': 'Item 1A'})
            
        Returns:
            List of retrieved nodes
        """
        query_bundle = QueryBundle(query_str=query)
        
        if metadata_filters:
            # Filter nodes by metadata
            nodes = self.retriever.retrieve(query_bundle)
            filtered_nodes = [
                node for node in nodes
                if all(
                    node.metadata.get(key) == value
                    for key, value in metadata_filters.items()
                )
            ]
            return filtered_nodes[:self.similarity_top_k]
        
        return self.retriever.retrieve(query_bundle)
    
    def _create_french_synthesis(self, query: str, context: str) -> str:
        """
        Create a French synthesis of the context when LLM is unavailable.
        This provides a better response than just raw context.
        """
        # Clean context
        context_clean = re.sub(r'\s+', ' ', context).strip()
        if not context_clean or len(context_clean) < 20:
            return "Aucune information pertinente trouvée pour cette question."
        
        # Extract first sentences as summary
        sentences = re.split(r'[.!?]+', context_clean)
        summary_sentences = [s.strip() for s in sentences[:3] if s.strip() and len(s.strip()) > 10]
        
        if summary_sentences:
            summary = ". ".join(summary_sentences) + "."
            return f"**Résumé basé sur le rapport 10-K :**\n\n{summary}\n\n**Détails complets :**\n{context_clean[:2000]}..."
        else:
            return f"**Informations extraites du rapport 10-K :**\n\n{context_clean[:2000]}..."
    
    def query(
        self,
        query: str,
        metadata_filters: Optional[dict] = None,
        response_mode: ResponseMode = ResponseMode.COMPACT
    ) -> str:
        """
        Query the RAG system and return response
        
        Args:
            query: Query string
            metadata_filters: Optional metadata filters
            response_mode: Response synthesis mode
            
        Returns:
            Response string
        """
        try:
            # First, check if index has documents
            try:
                # Try to retrieve nodes to check if index is populated
                test_nodes = self.retriever.retrieve(QueryBundle(query_str=query))
                if not test_nodes or len(test_nodes) == 0:
                    return "Aucun document n'est actuellement indexé dans le système RAG. Veuillez charger un rapport 10-K."
            except Exception as check_error:
                print(f"Index check error: {check_error}")
            
            # Detect if question is about risks and prioritize Item 1A
            query_lower = query.lower()
            risk_keywords = ['risque', 'danger', 'menace', 'problème', 'défi', 'difficulté', 'exposure', 'risk', 'hazard']
            is_risk_question = any(kw in query_lower for kw in risk_keywords)
            
            # Try with lower similarity threshold if first attempt fails
            original_cutoff = self.postprocessor.similarity_cutoff
            
            # First attempt with normal threshold
            # If no LLM is configured, avoid creating a query engine that may try to load a default LLM
            query_engine = None
            if self.llm is not None:
                query_engine = self.create_query_engine(response_mode=response_mode)
            else:
                # No LLM: retrieve and synthesize with fallback prompt in French
                nodes = self.retriever.retrieve(QueryBundle(query_str=query))
                
                # Prioritize Item 1A for risk questions
                if is_risk_question:
                    item_1a_nodes = [n for n in nodes if 'Item 1A' in (n.metadata.get('section') or '')]
                    if item_1a_nodes:
                        nodes = item_1a_nodes[:self.similarity_top_k]
                
                if nodes:
                    context = "\n\n".join([node.get_content() for node in nodes[:self.similarity_top_k]])
                    if context.strip():
                        # Create French synthesis prompt without LLM
                        synthesis = self._create_french_synthesis(query, context)
                        return synthesis
            
            if metadata_filters:
                # Use custom retrieval with filters
                nodes = self.retrieve_with_metadata_filter(query, metadata_filters)
                # If nodes found, synthesize with LLM if available, otherwise return raw context
                if nodes:
                    if self.llm:
                        context = "\n\n".join([node.get_content() for node in nodes])
                        if context.strip():
                            prompt = f"""Based on the following context from financial documents, answer the question in French.

Context:
{context}

Question: {query}

Answer in French:"""
                            response = self.llm.complete(prompt)
                            response_text = str(response)
                            if response_text and len(response_text.strip()) > 10:
                                return response_text
                    else:
                        context = "\n\n".join([node.get_content() for node in nodes[:self.similarity_top_k]])
                        if context.strip():
                            return self._create_french_synthesis(query, context)
                else:
                    # If no nodes, try without filters by lowering threshold
                    self.postprocessor.similarity_cutoff = 0.5
                    nodes = self.retrieve_with_metadata_filter(query, metadata_filters)
                    self.postprocessor.similarity_cutoff = original_cutoff
                    if nodes:
                        if self.llm:
                            context = "\n\n".join([node.get_content() for node in nodes])
                            if context.strip():
                                prompt = f"""Based on the following context from financial documents, answer the question in French.

Context:
{context}

Question: {query}

Answer in French:"""
                                response = self.llm.complete(prompt)
                                response_text = str(response)
                                if response_text and len(response_text.strip()) > 10:
                                    return response_text
                        else:
                            context = "\n\n".join([node.get_content() for node in nodes[:self.similarity_top_k]])
                            if context.strip():
                                return self._create_french_synthesis(query, context)
                return "Aucune information pertinente trouvée dans le rapport 10-K pour cette question."
            
            # Standard query without filters
            response = query_engine.query(query)
            
            # Extract response text properly - handle different response types
            response_text = ""
            
            # Try different ways to extract text from response
            if isinstance(response, str):
                response_text = response
            elif hasattr(response, 'response'):
                response_text = str(response.response)
            elif hasattr(response, 'text'):
                response_text = str(response.text)
            elif hasattr(response, 'get_response'):
                response_text = str(response.get_response())
            elif hasattr(response, 'source_nodes'):
                # It's a Response object, try multiple extraction methods
                # First try to get response text directly
                if hasattr(response, 'response'):
                    response_text = str(response.response)
                elif hasattr(response, 'text'):
                    response_text = str(response.text)
                else:
                    # Try to get from source nodes and synthesize
                    if response.source_nodes and len(response.source_nodes) > 0:
                        context = "\n\n".join([node.get_content() for node in response.source_nodes[:5]])
                        if self.llm and context.strip():
                            prompt = f"""Basé sur le contexte suivant du rapport 10-K, répondez à la question en français de manière détaillée et professionnelle.

Contexte:
{context}

Question: {query}

Réponse en français (détaillée et bien structurée):"""
                            try:
                                response_obj = self.llm.complete(prompt)
                                response_text = str(response_obj)
                            except Exception as llm_error:
                                print(f"LLM synthesis error: {llm_error}")
                                # Fallback: return context directly
                                response_text = f"**Informations trouvées dans le rapport 10-K :**\n\n{context[:2000]}"
                    else:
                        # No source nodes, try string conversion
                        response_text = str(response)
            else:
                # Last resort: convert to string
                response_text = str(response)
            
            # Check if response is empty or too short
            if not response_text or len(response_text.strip()) < 10:
                # Retry with lower similarity threshold
                self.postprocessor.similarity_cutoff = 0.5
                query_engine = self.create_query_engine(response_mode=response_mode)
                response = query_engine.query(query)
                
                # Extract again
                if hasattr(response, 'response'):
                    response_text = str(response.response)
                elif hasattr(response, 'source_nodes'):
                    if response.source_nodes:
                        context = "\n\n".join([node.get_content() for node in response.source_nodes[:3]])
                        if self.llm and context.strip():
                            prompt = f"""Based on the following context from financial documents, answer the question in French.

Context:
{context}

Question: {query}

Answer in French:"""
                            response_obj = self.llm.complete(prompt)
                            response_text = str(response_obj)
                else:
                    response_text = str(response)
                
                self.postprocessor.similarity_cutoff = original_cutoff
            
            # Final check
            if not response_text or len(response_text.strip()) < 10:
                # Last resort: try direct retrieval without postprocessing
                try:
                    nodes = self.retriever.retrieve(QueryBundle(query_str=query))
                    if nodes:
                        context = "\n\n".join([node.get_content() for node in nodes[:5]])
                        # If LLM available, synthesize; otherwise return the raw context
                        if context.strip():
                            if self.llm:
                                prompt = f"""Based on the following context from financial documents, answer the question in French.

Context:
{context}

Question: {query}

Answer in French:"""
                                response_obj = self.llm.complete(prompt)
                                response_text = str(response_obj)
                            else:
                                response_text = f"Informations extraites du rapport 10-K :\n\n{context[:4000]}"
                except Exception as e:
                    print(f"Direct retrieval fallback failed: {e}")
            
            if not response_text or len(response_text.strip()) < 10:
                return "Désolé, je n'ai pas trouvé d'informations pertinentes dans le rapport 10-K pour répondre à cette question. Veuillez reformuler votre question ou vérifier que le rapport a été correctement chargé."
            
            return response_text.strip()
            
        except Exception as e:
            print(f"RAG query error: {e}")
            return f"Erreur lors de la recherche dans le rapport 10-K: {str(e)}. Veuillez vérifier que le rapport a été correctement chargé."





