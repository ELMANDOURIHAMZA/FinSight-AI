"""
Tests for RAG system
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from llama_index.core import Document
from src.rag.ingestion import DocumentIngester
from src.rag.retrieval import AdvancedRAGRetriever


class TestDocumentIngester:
    """Test document ingestion"""
    
    @pytest.fixture
    def ingester(self, tmp_path):
        """Create ingester instance with temp directory"""
        return DocumentIngester(persist_dir=str(tmp_path / "vector_db"))
    
    def test_create_documents_from_text(self, ingester):
        """Test creating documents from text"""
        text = "This is a test document about financial analysis."
        metadata = {"source": "test"}
        
        documents = ingester.create_documents_from_text(text, metadata)
        
        assert len(documents) == 1
        assert documents[0].text == text
        assert documents[0].metadata["source"] == "test"
    
    def test_create_documents_from_sections(self, ingester):
        """Test creating documents from sections"""
        sections = {
            "Item 1": "Business section content",
            "Item 1A": "Risk factors content"
        }
        
        documents = ingester.create_documents_from_sections(sections)
        
        assert len(documents) == 2
        assert all(doc.metadata.get('document_type') == '10-K' for doc in documents)
        assert {doc.metadata.get('section') for doc in documents} == {"Item 1", "Item 1A"}


class TestAdvancedRAGRetriever:
    """Test RAG retriever"""
    
    @pytest.fixture
    def mock_index(self):
        """Create mock index"""
        index = Mock()
        return index
    
    @pytest.fixture
    def mock_llm(self):
        """Create mock LLM"""
        llm = Mock()
        llm.complete.return_value = Mock(text="Test response")
        return llm
    
    def test_create_query_engine(self, mock_index, mock_llm):
        """Test query engine creation"""
        retriever = AdvancedRAGRetriever(
            index=mock_index,
            llm=mock_llm,
            similarity_top_k=5
        )
        
        query_engine = retriever.create_query_engine()
        
        assert query_engine is not None






