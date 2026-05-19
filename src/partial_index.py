"""
Belirtilen tickerların metadata dosyalarını okuyup sadece onları parse+embed eder.
Doğrudan Qdrant'a upsert eder, chunks.jsonl'ye yazmaz.

Kullanım:
    python -m src.partial_index GARAN ISCTR TCELL
    python -m src.partial_index GARAN --device cuda  # GPU kullanmak için
"""
from __future__ import annotations

import argparse
import dataclasses
import json
import logging
import time
from typing import Iterator

from .config import CONFIG
from .parse import ChunkRecord, extract_text_from_pdf, clean_text, chunk_text
from .embed_and_index import (
    get_embedder,
    get_qdrant_client,
    ensure_collection,
    deterministic_id,
    batch,
)
from qdrant_client.http import models as qm

log = logging.getLogger("partial_index")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)


def iter_ticker_chunks(tickers: set[str]) -> Iterator[ChunkRecord]:
    """Sadece belirtilen tickerların metadata dosyalarını okur — diğerlerini atlar."""
    for ticker in sorted(tickers):
        meta_file = CONFIG.metadata_dir / f"{ticker}.json"
        if not meta_file.exists():
            log.warning("Metadata dosyası bulunamadı: %s — atlanıyor", ticker)
            continue

        try:
            records = json.loads(meta_file.read_text(encoding="utf-8"))
        except Exception as e:
            log.warning("Metadata okunamadı %s: %s", ticker, e)
            continue

        ticker_chunks = 0
        for disc in records:
            for att in disc.get("attachments", []):
                pdf_path = CONFIG.project_root / att["local_path"]
                if not pdf_path.exists():
                    continue

                raw = extract_text_from_pdf(pdf_path)
                cleaned = clean_text(raw)
                if len(cleaned) < CONFIG.min_chunk_chars:
                    continue

                for i, ch in enumerate(chunk_text(cleaned)):
                    ticker_chunks += 1
                    yield ChunkRecord(
                        chunk_id=f"{disc['index']}_{pdf_path.stem}_{i}",
                        text=ch,
                        ticker=ticker,
                        company_name=disc.get("company_name", ""),
                        disclosure_index=disc["index"],
                        publish_datetime=disc["publish_datetime"],
                        subject=disc.get("subject", ""),
                        disclosure_type=disc.get("disclosure_type", ""),
                        is_corrective=disc.get("is_corrective", False),
                        is_late=disc.get("is_late", False),
                        url=disc.get("url", ""),
                        source_filename=pdf_path.name,
                        chunk_position=i,
                    )

        log.info("  %s: %d chunk parse edildi", ticker, ticker_chunks)


def _upsert_with_retry(client, points: list, max_retries: int = 6) -> None:
    for attempt in range(max_retries):
        try:
            client.upsert(collection_name=CONFIG.qdrant_collection, points=points)
            return
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            wait = 2 ** attempt
            log.warning("Qdrant upsert hatası (deneme %d/%d), %ds sonra tekrar: %s",
                        attempt + 1, max_retries, wait, e)
            time.sleep(wait)


def run(tickers: list[str], batch_size: int = 64, device: str = "cpu") -> int:
    ticker_set = {t.upper() for t in tickers}
    log.info("Tickerlar: %s  |  batch_size=%d  |  device=%s",
             sorted(ticker_set), batch_size, device)

    embedder = get_embedder(device=device)
    client = get_qdrant_client()
    ensure_collection(client)

    total = 0
    for batch_chunks in batch(iter_ticker_chunks(ticker_set), batch_size):
        texts = [c.text for c in batch_chunks]
        vectors = embedder.encode(
            texts,
            batch_size=batch_size,
            normalize_embeddings=True,
            show_progress_bar=False,
        )

        points = [
            qm.PointStruct(
                id=deterministic_id(c.chunk_id),
                vector=vec.tolist(),
                payload={k: v for k, v in dataclasses.asdict(c).items() if k != "chunk_id"},
            )
            for c, vec in zip(batch_chunks, vectors)
        ]

        _upsert_with_retry(client, points)
        total += len(points)
        if total % (batch_size * 10) == 0:
            log.info("  %d chunk indexlendi...", total)

    log.info("✓ %s için toplam %d chunk indexlendi.", sorted(ticker_set), total)
    return total


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("tickers", nargs="+")
    parser.add_argument("--batch-size", type=int, default=64)
    parser.add_argument("--device", default="cpu", choices=["cpu", "cuda"],
                        help="Embedding cihazı (varsayılan: cpu)")
    args = parser.parse_args()
    run(args.tickers, batch_size=args.batch_size, device=args.device)


if __name__ == "__main__":
    main()
