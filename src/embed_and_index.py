from __future__ import annotations

import json
import logging
import uuid
from pathlib import Path
from typing import Iterator

from qdrant_client import QdrantClient
from qdrant_client.http import models as qm
from sentence_transformers import SentenceTransformer

from .config import CONFIG

log = logging.getLogger("embed")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)


def get_embedder() -> SentenceTransformer:
    log.info("Embedding modeli yükleniyor: %s", CONFIG.embedding_model)
    model = SentenceTransformer(CONFIG.embedding_model)
    log.info("  Cihaz: %s", model.device)
    return model


def get_qdrant_client() -> QdrantClient:
    if CONFIG.using_cloud:
        log.info("Qdrant Cloud bağlantısı: %s", CONFIG.qdrant_url)
        return QdrantClient(
            url=CONFIG.qdrant_url,
            api_key=CONFIG.qdrant_api_key,
            prefer_grpc=CONFIG.qdrant_prefer_grpc,
            timeout=60,  # Cloud round-trip'i daha uzun olabilir
        )
    log.info("Qdrant lokal: localhost:6333")
    return QdrantClient(host="localhost", port=6333)


def ensure_collection(client: QdrantClient) -> None:
    collections = {c.name for c in client.get_collections().collections}
    if CONFIG.qdrant_collection in collections:
        log.info("Collection mevcut: %s", CONFIG.qdrant_collection)
        return

    client.create_collection(
        collection_name=CONFIG.qdrant_collection,
        vectors_config=qm.VectorParams(
            size=CONFIG.embedding_dim,
            distance=qm.Distance.COSINE,
        ),
    )
    log.info("Collection oluşturuldu: %s (dim=%d, cosine)",
             CONFIG.qdrant_collection, CONFIG.embedding_dim)

    for field, schema in [
        ("ticker", qm.PayloadSchemaType.KEYWORD),
        ("disclosure_type", qm.PayloadSchemaType.KEYWORD),
        ("disclosure_index", qm.PayloadSchemaType.INTEGER),
        ("publish_datetime", qm.PayloadSchemaType.DATETIME),
    ]:
        try:
            client.create_payload_index(
                collection_name=CONFIG.qdrant_collection,
                field_name=field,
                field_schema=schema,
            )
        except Exception as e:
            log.debug("Index oluşturma uyarısı (%s): %s", field, e)


def iter_chunks(path: Path) -> Iterator[dict]:
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                yield json.loads(line)


def batch(iterable, n: int):
    buf = []
    for item in iterable:
        buf.append(item)
        if len(buf) >= n:
            yield buf
            buf = []
    if buf:
        yield buf


def deterministic_id(chunk_id: str) -> str:
    return str(uuid.uuid5(uuid.NAMESPACE_URL, chunk_id))


def index_chunks() -> int:
    chunks_path = CONFIG.text_dir / "chunks.jsonl"
    if not chunks_path.exists():
        raise FileNotFoundError(f"Chunk dosyası yok: {chunks_path}. Önce src.parse'ı çalıştırın.")

    embedder = get_embedder()
    client = get_qdrant_client()
    ensure_collection(client)

    total = 0
    for batch_chunks in batch(iter_chunks(chunks_path), CONFIG.embedding_batch_size):
        texts = [c["text"] for c in batch_chunks]
        # bge-m3 için normalize_embeddings=True önerilir (cosine similarity)
        vectors = embedder.encode(
            texts,
            batch_size=CONFIG.embedding_batch_size,
            normalize_embeddings=True,
            show_progress_bar=False,
        )

        points = []
        for chunk, vec in zip(batch_chunks, vectors):
            payload = {k: v for k, v in chunk.items() if k != "chunk_id"}
            points.append(qm.PointStruct(
                id=deterministic_id(chunk["chunk_id"]),
                vector=vec.tolist(),
                payload=payload,
            ))

        client.upsert(collection_name=CONFIG.qdrant_collection, points=points)
        total += len(points)
        if total % (CONFIG.embedding_batch_size * 10) == 0:
            log.info("  %d chunk indexlendi...", total)

    log.info("✓ Toplam %d chunk indexlendi.", total)
    return total


if __name__ == "__main__":
    index_chunks()
