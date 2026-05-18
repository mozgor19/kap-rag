"""
Qdrant Cloud (veya lokal) bağlantısını test et.

Bu scripti diğer adımlardan ÖNCE çalıştırın — bağlantı, API key
ve embedding modeli boyutu uyumunu doğrular.

Kullanım:
    python -m src.test_connection
"""
from __future__ import annotations

import logging
import sys

from qdrant_client import QdrantClient
from qdrant_client.http import models as qm

from .config import CONFIG

log = logging.getLogger("test_connection")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)


def test_qdrant() -> bool:
    """Qdrant bağlantısı + collection durumunu kontrol et."""
    print("\n" + "=" * 60)
    print("QDRANT BAĞLANTI TESTİ")
    print("=" * 60)

    if CONFIG.using_cloud:
        print(f"  Mod:          Qdrant Cloud")
        print(f"  URL:          {CONFIG.qdrant_url}")
        # API key'in son 6 hanesini göster (debug için)
        key_tail = CONFIG.qdrant_api_key[-6:] if CONFIG.qdrant_api_key else "?"
        print(f"  API Key:      ...{key_tail}  (uzunluk: {len(CONFIG.qdrant_api_key or '')})")
    else:
        print(f"  Mod:          Lokal Docker (localhost:6333)")
        print(f"  ⚠️  QDRANT_URL ve QDRANT_API_KEY ortam değişkenleri set edilmemiş.")
        print(f"     Cloud kullanmak için .env dosyası oluşturup şu satırları ekleyin:")
        print(f"        QDRANT_URL=https://...cloud.qdrant.io:6333")
        print(f"        QDRANT_API_KEY=...")

    print(f"  Collection:   {CONFIG.qdrant_collection}")
    print(f"  Embed dim:    {CONFIG.embedding_dim}")
    print()

    try:
        if CONFIG.using_cloud:
            client = QdrantClient(
                url=CONFIG.qdrant_url,
                api_key=CONFIG.qdrant_api_key,
                prefer_grpc=CONFIG.qdrant_prefer_grpc,
                timeout=30,
            )
        else:
            client = QdrantClient(host="localhost", port=6333)
    except Exception as e:
        print(f"  ✗ Client oluşturulamadı: {e}")
        return False

    # 1) Collection listesi al — bağlantı + auth kontrolü
    try:
        collections = client.get_collections().collections
        names = [c.name for c in collections]
        print(f"  ✓ Bağlantı OK. Mevcut collection sayısı: {len(names)}")
        if names:
            print(f"    Collections: {', '.join(names)}")
    except Exception as e:
        msg = str(e).lower()
        if "unauthorized" in msg or "401" in msg or "403" in msg:
            print(f"  ✗ Auth hatası: API key yanlış veya yetkisi yetersiz.")
            print(f"     Detay: {e}")
        else:
            print(f"  ✗ Bağlantı hatası: {e}")
        return False

    # 2) Hedef collection var mı? Varsa boyutunu kontrol et
    if CONFIG.qdrant_collection in names:
        info = client.get_collection(CONFIG.qdrant_collection)
        existing_dim = info.config.params.vectors.size
        print(f"  ℹ Collection '{CONFIG.qdrant_collection}' zaten var.")
        print(f"    - Vector dim: {existing_dim}")
        print(f"    - Point sayısı: {info.points_count}")
        if existing_dim != CONFIG.embedding_dim:
            print(f"  ⚠ DİKKAT: Mevcut collection {existing_dim}-dim, config {CONFIG.embedding_dim}-dim.")
            print(f"    Embedding modeli farklıysa collection'ı silip yeniden oluşturmalısınız.")
            return False
    else:
        print(f"  ℹ Collection '{CONFIG.qdrant_collection}' henüz yok — embed adımında oluşturulacak.")

    # 3) Hızlı yazma/okuma testi (Cloud'da gerçek round-trip için)
    test_collection = "_connection_test_tmp"
    try:
        if test_collection in names:
            client.delete_collection(test_collection)
        client.create_collection(
            collection_name=test_collection,
            vectors_config=qm.VectorParams(size=4, distance=qm.Distance.COSINE),
        )
        client.upsert(
            collection_name=test_collection,
            points=[qm.PointStruct(id=1, vector=[0.1, 0.2, 0.3, 0.4], payload={"test": "ok"})],
        )
        hits = client.query_points(
            collection_name=test_collection,
            query=[0.1, 0.2, 0.3, 0.4],
            limit=1,
        ).points
        assert len(hits) == 1 and hits[0].payload["test"] == "ok"
        client.delete_collection(test_collection)
        print(f"  ✓ Yazma/okuma round-trip testi başarılı.")
    except Exception as e:
        print(f"  ✗ Round-trip testi başarısız: {e}")
        return False

    print()
    print("  🎉 Qdrant hazır. Pipeline'ı çalıştırabilirsiniz:")
    print("     python -m src.pipeline")
    return True


def test_embedding() -> bool:
    """Embedding modeli yüklenebiliyor mu + boyut config ile uyuyor mu?"""
    print("\n" + "=" * 60)
    print("EMBEDDING MODELİ TESTİ")
    print("=" * 60)
    print(f"  Model: {CONFIG.embedding_model}")
    print(f"  (İlk çalıştırmada ~2GB indirme olabilir; bekleyin...)")

    try:
        from sentence_transformers import SentenceTransformer
    except ImportError:
        print("  ✗ sentence-transformers yüklü değil. pip install sentence-transformers")
        return False

    try:
        model = SentenceTransformer(CONFIG.embedding_model)
        print(f"  ✓ Model yüklendi. Cihaz: {model.device}")
        vec = model.encode(["Merhaba dünya"], normalize_embeddings=True)[0]
        print(f"  ✓ Test embedding üretildi. Boyut: {len(vec)}")
        if len(vec) != CONFIG.embedding_dim:
            print(f"  ⚠ DİKKAT: Modelden {len(vec)}-dim çıkıyor, config {CONFIG.embedding_dim}-dim diyor.")
            print(f"    config.py'da embedding_dim'i {len(vec)} olarak güncelleyin.")
            return False
        return True
    except Exception as e:
        print(f"  ✗ Model yüklenemedi: {e}")
        return False


if __name__ == "__main__":
    ok_qdrant = test_qdrant()
    # Embedding testi ağır (model indirme), isteğe bağlı:
    if "--embed" in sys.argv:
        ok_embed = test_embedding()
        sys.exit(0 if (ok_qdrant and ok_embed) else 1)
    else:
        print("\n  (Embedding modelini de test etmek için: python -m src.test_connection --embed)")
        sys.exit(0 if ok_qdrant else 1)
