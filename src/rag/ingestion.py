"""
Document ingestion and indexing for RAG
"""
import os
from typing import List, Optional
from llama_index.core import Document, VectorStoreIndex, StorageContext, Settings
from llama_index.core.node_parser import SentenceSplitter
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
import chromadb
from chromadb.config import Settings as ChromaSettings


class DocumentIngester:
    """
    Handles document ingestion, chunking, and vector store indexing
    """
    
    def __init__(
        self,
        embedding_model: str = "BAAI/bge-small-en-v1.5",
        chunk_size: int = 1024,
        chunk_overlap: int = 200,
        persist_dir: str = "data/vector_db"
    ):
        """
        Initialize the document ingester
        
        Args:
            embedding_model: HuggingFace model name for embeddings
            chunk_size: Size of text chunks in tokens
            chunk_overlap: Overlap between chunks in tokens
            persist_dir: Directory for vector store persistence
        """
        self.persist_dir = persist_dir
        os.makedirs(persist_dir, exist_ok=True)
        
        # Initialize embedding model
        try:
            self.embed_model = HuggingFaceEmbedding(model_name=embedding_model)
            Settings.embed_model = self.embed_model
        except Exception as e:
            print(f"Warning: Failed to load HuggingFace embedding '{embedding_model}': {e}\nFalling back to 'sentence-transformers/all-MiniLM-L6-v2'")
            try:
                from llama_index.embeddings.huggingface import HuggingFaceEmbedding as HfEmb
                self.embed_model = HfEmb(model_name="sentence-transformers/all-MiniLM-L6-v2")
                Settings.embed_model = self.embed_model
            except Exception as e2:
                print(f"Fallback embedding also failed: {e2}. Embedding initialization aborted.")
                self.embed_model = None
        
        # Initialize text splitter
        self.text_splitter = SentenceSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        
        # Initialize ChromaDB
        self.chroma_client = chromadb.PersistentClient(
            path=persist_dir,
            settings=ChromaSettings(anonymized_telemetry=False)
        )
    
    def create_or_load_index(self, collection_name: str = "finsight_documents") -> VectorStoreIndex:
        """
        Create a new index or load existing one
        
        Args:
            collection_name: Name of the ChromaDB collection
            
        Returns:
            VectorStoreIndex instance
        """
        try:
            # Try to get existing collection
            chroma_collection = self.chroma_client.get_collection(collection_name)
            vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
            storage_context = StorageContext.from_defaults(vector_store=vector_store)
            
            # Load existing index
            index = VectorStoreIndex.from_vector_store(
                vector_store=vector_store,
                storage_context=storage_context
            )
            print(f"Loaded existing index from {self.persist_dir}")
            return index
            
        except Exception:
            # Create new collection
            chroma_collection = self.chroma_client.create_collection(collection_name)
            vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
            storage_context = StorageContext.from_defaults(vector_store=vector_store)
            
            # Create new index
            index = VectorStoreIndex.from_vector_store(
                vector_store=vector_store,
                storage_context=storage_context
            )
            print(f"Created new index at {self.persist_dir}")
            return index
    
    def ingest_documents(
        self,
        documents: List[Document],
        collection_name: str = "finsight_documents",
        reset: bool = False
    ) -> VectorStoreIndex:
        """
        Ingest documents into the vector store
        
        Args:
            documents: List of Document objects to ingest
            collection_name: Name of the ChromaDB collection
            reset: If True, delete existing collection and create new one
            
        Returns:
            VectorStoreIndex instance
        """
        if reset:
            try:
                self.chroma_client.delete_collection(collection_name)
            except Exception:
                pass
        
        # Create or load index
        index = self.create_or_load_index(collection_name)

        # Add documents to index
        if documents:
            # Split documents into nodes
            nodes = []
            for doc in documents:
                doc_nodes = self.text_splitter.get_nodes_from_documents([doc])
                nodes.extend(doc_nodes)

            # Insert nodes into index
            try:
                index.insert_nodes(nodes)
                print(f"Ingested {len(nodes)} nodes from {len(documents)} documents into collection '{collection_name}'")

                # Debug: print a small sample of nodes (content snippet + metadata)
                sample_count = min(3, len(nodes))
                for i in range(sample_count):
                    try:
                        content = nodes[i].get_content()
                    except Exception:
                        content = str(nodes[i])[:200]
                    metadata = getattr(nodes[i], 'metadata', {}) or {}
                    print(f"  Sample node {i+1}: meta={metadata} content_snippet={content[:200]!r}")
            except Exception as e:
                print(f"Error inserting nodes into index: {e}")

        return index
    
    def create_documents_from_text(
        self,
        text: str,
        metadata: Optional[dict] = None
    ) -> List[Document]:
        """
        Create Document objects from text
        
        Args:
            text: Text content
            metadata: Optional metadata dictionary
            
        Returns:
            List of Document objects
        """
        if metadata is None:
            metadata = {}
        
        document = Document(
            text=text,
            metadata=metadata
        )
        
        return [document]
    
    def create_documents_from_sections(
        self,
        sections: dict,
        base_metadata: Optional[dict] = None
    ) -> List[Document]:
        """
        Create Document objects from sectioned text (e.g., 10-K sections)
        
        Args:
            sections: Dictionary of section_name -> section_text
            base_metadata: Base metadata to add to all documents
            
        Returns:
            List of Document objects
        """
        if base_metadata is None:
            base_metadata = {}
        
        documents = []
        for section_name, section_text in sections.items():
            metadata = {
                **base_metadata,
                'section': section_name,
                'document_type': '10-K'
            }
            doc = Document(
                text=section_text,
                metadata=metadata
            )
            documents.append(doc)
        
        return documents






