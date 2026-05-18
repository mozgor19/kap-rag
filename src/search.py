from __future__ import annotations

import argparse
import logging
from datetime import datetime
from functools import lru_cache
from typing import Optional

from qdrant_client import QdrantClient
from qdrant_client.http import models as qm
from sentence_transformers import SentenceTransformer

from .config import CONFIG

log = logging.getLogger("search")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)


@lru_cache(maxsize=1)
def _embedder() -> SentenceTransformer:
    return SentenceTransformer(CONFIG.embedding_model)


@lru_cache(maxsize=1)
def _client() -> QdrantClient:
    if CONFIG.using_cloud:
        return QdrantClient(
            url=CONFIG.qdrant_url,
            api_key=CONFIG.qdrant_api_key,
            prefer_grpc=CONFIG.qdrant_prefer_grpc,
            timeout=60,
        )
    return QdrantClient(host="localhost", port=6333)


def _build_filter(
    ticker: Optional[str],
    disclosure_type: Optional[str],
    since: Optional[str],
    until: Optional[str],
) -> Optional[qm.Filter]:
    must = []
    if ticker:
        must.append(qm.FieldCondition(key="ticker", match=qm.MatchValue(value=ticker.upper())))
    if disclosure_type:
        must.append(qm.FieldCondition(
            key="disclosure_type",
            match=qm.MatchValue(value=disclosure_type),
        ))
    if since or until:
        rng = {}
        if since:
            rng["gte"] = datetime.fromisoformat(since).isoformat()
        if until:
            rng["lte"] = datetime.fromisoformat(until).isoformat()
        must.append(qm.FieldCondition(key="publish_datetime", range=qm.DatetimeRange(**rng)))
    return qm.Filter(must=must) if must else None


def semantic_search(
    query: str,
    *,
    top_k: int = 5,
    ticker: Optional[str] = None,
    disclosure_type: Optional[str] = None,
    since: Optional[str] = None,
    until: Optional[str] = None,
) -> list[dict]:
    embedder = _embedder()
    client = _client()

    qvec = embedder.encode(
        [query],
        normalize_embeddings=True,
        show_progress_bar=False,
    )[0].tolist()

    flt = _build_filter(ticker, disclosure_type, since, until)

    hits = client.query_points(
        collection_name=CONFIG.qdrant_collection,
        query=qvec,
        query_filter=flt,
        limit=top_k,
        with_payload=True,
    ).points

    results = []
    for h in hits:
        p = h.payload or {}
        results.append({
            "score": float(h.score),
            "text": p.get("text", ""),
            "ticker": p.get("ticker"),
            "company_name": p.get("company_name"),
            "subject": p.get("subject"),
            "disclosure_type": p.get("disclosure_type"),
            "publish_datetime": p.get("publish_datetime"),
            "url": p.get("url"),
            "source_filename": p.get("source_filename"),
        })
    return results


def pretty_print(results: list[dict]) -> None:
    for i, r in enumerate(results, 1):
        print(f"\n— [{i}] (skor={r['score']:.4f}) {r['ticker']} | {r['subject']}")
        print(f"   📅 {r['publish_datetime']}  |  {r['disclosure_type']}")
        print(f"   🔗 {r['url']}")
        snippet = r["text"][:400].replace("\n", " ")
        print(f"   📄 {snippet}{'...' if len(r['text']) > 400 else ''}")


def main():
    parser = argparse.ArgumentParser(description="KAP RAG semantic search")
    parser.add_argument("query", help="Doğal dil sorgusu")
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--ticker", type=str, default=None)
    parser.add_argument("--disclosure-type", type=str, default=None)
    parser.add_argument("--since", type=str, default=None, help="YYYY-MM-DD")
    parser.add_argument("--until", type=str, default=None, help="YYYY-MM-DD")
    args = parser.parse_args()

    results = semantic_search(
        args.query,
        top_k=args.top_k,
        ticker=args.ticker,
        disclosure_type=args.disclosure_type,
        since=args.since,
        until=args.until,
    )
    print(f"\nSorgu: {args.query}")
    print(f"Sonuç sayısı: {len(results)}")
    pretty_print(results)


if __name__ == "__main__":
    main()
