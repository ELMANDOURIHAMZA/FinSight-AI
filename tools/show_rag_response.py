"""Show RAG raw response and formatted sources for inspection
Usage: python tools/show_rag_response.py --ticker AAPL --question "...""" 
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.rag.ingestion import DocumentIngester
from src.rag.retrieval import AdvancedRAGRetriever
from llama_index.core import QueryBundle


def show_response(ticker: str, question: str):
    print(f"Showing RAG response for ticker={ticker} question={question}")
    ingester = DocumentIngester()
    collection_name = f"finsight_{ticker.lower()}"
    try:
        index = ingester.create_or_load_index(collection_name=collection_name)
    except Exception as e:
        print(f"Error loading index: {e}")
        return

    retriever = AdvancedRAGRetriever(index=index, llm=None)

    # Retrieve nodes
    qb = QueryBundle(query_str=question)
    try:
        nodes = retriever.retriever.retrieve(qb)
    except Exception as e:
        print(f"Retrieval failed: {e}")
        nodes = []

    print(f"Retrieved {len(nodes)} nodes")

    # Build context from top-k nodes
    k = min(5, len(nodes))
    context = "\n\n".join([nodes[i].get_content() for i in range(k)]) if k > 0 else ""

    # Format sources
    sources = []
    for n in nodes[:5]:
        try:
            meta = getattr(n, 'metadata', {}) or {}
            section = meta.get('section') or meta.get('title') or meta.get('part') or 'Unknown section'
            ticker_meta = meta.get('ticker') or ''
            snippet = n.get_content()[:300].replace('\n', ' ')
            src = f"Section: {section}"
            if ticker_meta:
                src += f" (Ticker: {ticker_meta})"
            src += f" — \"{snippet}...\""
            sources.append(src)
        except Exception:
            continue

    response_text = "Informations extraites du rapport 10-K :\n\n" + (context[:8000] if context else "(aucun contexte trouvé)")
    if sources:
        response_text += "\n\n**Sources :**\n" + "\n".join([f"- {s}" for s in sources])

    print("\n--- Formatted response (truncated) ---\n")
    print(response_text)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--ticker', default='AAPL')
    parser.add_argument('--question', default="Quels sont les principaux risques de cette entreprise ?")
    args = parser.parse_args()
    show_response(args.ticker, args.question)
