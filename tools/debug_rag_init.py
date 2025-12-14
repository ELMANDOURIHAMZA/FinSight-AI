"""Debug script to initialize RAG ingestion for a given ticker and show logs."""
import os
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.data.sec_edgar import SecEdgarClient
from src.rag.ingestion import DocumentIngester


def debug_ticker(ticker: str = "GOOGL"):
    print(f"Debugging RAG ingestion for ticker: {ticker}")
    sec = SecEdgarClient()
    try:
        report = sec.get_10k_text(ticker)
        print(f"Report sections keys: {list(report.get('sections', {}).keys())}")
        print(f"Full text length: {report.get('metadata', {}).get('total_length')}")
    except Exception as e:
        print(f"Error getting 10-K text: {e}")
        return

    ingester = DocumentIngester()
    try:
        documents = ingester.create_documents_from_sections(report.get('sections', {}), base_metadata={'ticker': ticker})
        print(f"Created {len(documents)} Document objects from sections")
        index = ingester.ingest_documents(documents, collection_name=f"finsight_{ticker.lower()}", reset=False)
        print("Ingestion complete")
    except Exception as e:
        print(f"Error during ingestion: {e}")


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
        # No-op patch to trigger file update (ensures tools reflect parser changes)
    parser.add_argument('--ticker', default='GOOGL')
    args = parser.parse_args()
    debug_ticker(args.ticker)
