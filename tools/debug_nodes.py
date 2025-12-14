#!/usr/bin/env python3
"""Debug script to inspect node content"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from llama_index.core import VectorStoreIndex, Settings
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core import QueryBundle
import chromadb
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ticker', default='AAPL')
    parser.add_argument('--query', default='Quels sont les principaux risques ?')
    args = parser.parse_args()

    # Initialize embeddings (same as DocumentIngester)
    try:
        embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
        Settings.embed_model = embed_model
    except Exception as e:
        print(f"Warning: Failed to load embedding: {e}")
        try:
            embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")
            Settings.embed_model = embed_model
        except Exception:
            print("Failed to initialize embeddings")
            return

    # Load index via Chroma
    collection_name = f"finsight_{args.ticker.lower()}"
    persist_dir = str(Path(__file__).parent.parent / "data" / "vector_db")
    
    try:
        chroma_client = chromadb.PersistentClient(path=persist_dir)
        chroma_collection = chroma_client.get_collection(name=collection_name)
        vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
        index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
    except Exception as e:
        print(f"Error loading index: {e}")
        return

    # Create retriever
    retriever = VectorIndexRetriever(index=index, similarity_top_k=5)
    
    # Retrieve nodes
    qb = QueryBundle(query_str=args.query)
    nodes = retriever.retrieve(qb)
    
    print(f"Retrieved {len(nodes)} nodes for query: {args.query!r}\n")
    
    for i, node in enumerate(nodes):
        print(f"--- Node {i+1} ---")
        print(f"Metadata: {getattr(node, 'metadata', {})}")
        content = node.get_content() if hasattr(node, 'get_content') else str(node)
        print(f"Content length: {len(content)}")
        print(f"Content preview (first 300 chars):\n{content[:300]}\n")
        print(f"Content is empty: {not content or not content.strip()}\n")

if __name__ == '__main__':
    main()
