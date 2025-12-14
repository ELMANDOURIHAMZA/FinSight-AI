"""Debug script: load vector index for a ticker and retrieve nodes for a sample query."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.rag.ingestion import DocumentIngester
from src.rag.retrieval import AdvancedRAGRetriever
from llama_index.core import QueryBundle


def debug_query(ticker: str = "GOOGL", question: str = "Quelle est la stratégie de croissance de cette entreprise ?"):
    print(f"Debugging RAG query for ticker: {ticker}")
    ingester = DocumentIngester()
    collection_name = f"finsight_{ticker.lower()}"
    try:
        index = ingester.create_or_load_index(collection_name=collection_name)
    except Exception as e:
        print(f"Error loading index: {e}")
        return

    retriever = AdvancedRAGRetriever(index=index, llm=None)
    qb = QueryBundle(query_str=question)
    try:
        nodes = retriever.retriever.retrieve(qb)
        print(f"Retrieved {len(nodes)} nodes for query: {question}")
        for i, node in enumerate(nodes[:5], start=1):
            try:
                content = node.get_content()
            except Exception:
                content = str(node)[:500]
            meta = getattr(node, 'metadata', {}) or {}
            print(f" Node {i}: meta={meta} snippet={content[:300]!r}")
    except Exception as e:
        print(f"Retrieval failed: {e}")

    # Try the query method (may use LLM if available)
    try:
        response = retriever.query(question)
        print("--- RAG query response ---")
        print(response)
    except Exception as e:
        print(f"Query method failed: {e}")


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--ticker', default='GOOGL')
    parser.add_argument('--question', default='Quelle est la stratégie de croissance de cette entreprise ?')
    args = parser.parse_args()
    debug_query(args.ticker, args.question)
