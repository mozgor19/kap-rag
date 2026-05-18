# KAP RAG — BIST 30 Bildirim Vektör Veritabanı

Son 3 ayın BIST 30 KAP raporlarını KAP web sitesinden indirir, parse eder, embed eder, **Qdrant Cloud**'a yazar ve semantic search yapar.

## 📦 Proje yapısı

```
kap_rag/
├── src/
│   ├── bist30.py             # BIST 30 ticker listesi
│   ├── config.py             # Parametreler + .env okuma
│   ├── download.py           # KAP web sitesinden metadata + PDF indir
│   ├── parse.py              # PDF parse + chunking
│   ├── embed_and_index.py    # Embed + Qdrant'a yaz
│   ├── search.py             # Semantic search
│   ├── test_connection.py    # Cloud bağlantı + embedding sağlık testi
│   └── pipeline.py           # Tek komutla hepsi
├── data/                     # (otomatik oluşur)
│   ├── metadata/{TICKER}.json
│   ├── pdfs/{TICKER}/*.pdf
│   └── text/chunks.jsonl
├── .env.example              # Kopyalayıp .env yapın
├── .gitignore
└── requirements.txt
```

## 🚀 Kurulum (Qdrant Cloud)

### 1. Qdrant Cloud cluster ve API key

Qdrant Cloud paneli üzerinden:

1. **Create a Free Cluster** kartında:
   - **Cluster Name**: `kap-bist30`
   - **Cloud Provider**: AWS
   - **Region**: Frankfurt (eu-central-1) — Türkiye'den en düşük latency
   - **Create Free Cluster** butonuna tıklayın
2. Cluster ayağa kalktıktan sonra detayına girin → **API Keys** sekmesi → **+ Create**
3. **API key tek seferlik gösterilir — kopyalayın**
4. **Cluster URL**'yi (örn. `https://abc-def.eu-central-1-0.aws.cloud.qdrant.io:6333`) kopyalayın

### 2. Python ortamı

Python 3.10+ gerekli.

```bash
cd kap_rag
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. `.env` dosyası oluşturun

```bash
cp .env.example .env
```

`.env` dosyasını açıp doldurun:

```
QDRANT_URL=https://abc-def.eu-central-1-0.aws.cloud.qdrant.io:6333
QDRANT_API_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
QDRANT_COLLECTION=kap_bist30

KAP_START_DATE=
KAP_END_DATE=
KAP_LOOKBACK_DAYS=90

KAP_BASE_URL=https://www.kap.org.tr
KAP_LANGUAGE=tr
KAP_DOWNLOAD_EXTENSIONS=.pdf
```

KAP indirme adımı MKK API key/secret kullanmaz. `KAP_START_DATE` ve `KAP_END_DATE` boş bırakılırsa son 90 gün indirilir.

> ⚠️ **`.env` dosyasını git'e commit etmeyin.** `.gitignore`'da hariç tutulmuş durumda.

### 4. Bağlantıyı test edin (ÖNEMLİ)

PDF indirip embedding yapmadan **önce** Cloud bağlantısını doğrulayın:

```bash
python -m src.test_connection
```

Başarılı çıktı şöyle görünür:

```
QDRANT BAĞLANTI TESTİ
============================================================
  Mod:          Qdrant Cloud
  URL:          https://...
  API Key:      ...xyz123  (uzunluk: 152)
  Collection:   kap_bist30
  ✓ Bağlantı OK. Mevcut collection sayısı: 0
  ℹ Collection 'kap_bist30' henüz yok — embed adımında oluşturulacak.
  ✓ Yazma/okuma round-trip testi başarılı.
  🎉 Qdrant hazır.
```

Embedding modelini de test etmek istiyorsanız (~2GB indirir):

```bash
python -m src.test_connection --embed
```

## 🎯 Çalıştırma

### Mini test (önerilen ilk adım) — 2 hisseyle ~5-10 dakika:

```bash
python -m src.pipeline --tickers THYAO ASELS
```

Hızlı sağlık kontrolü. Sorunsuz çalışırsa BIST 30'un hepsini koşturun:

### Tam pipeline:

```bash
python -m src.pipeline
```

Sırayla yapar:
1. KAP web sitesinden BIST 30'un son 3 ay bildirim metadata + PDF'leri indir
2. PDF'leri parse + chunk'la
3. BAAI/bge-m3 ile embed + Qdrant Cloud'a yaz
4. Test sorgusu çalıştır

### Adım adım kontrollü:

```bash
python -m src.pipeline --steps download
python -m src.pipeline --steps parse
python -m src.pipeline --steps embed
python -m src.pipeline --steps search --query "yeni sözleşme"
```

## 🔍 Semantic search örnekleri

```bash
python -m src.search "şirket kar payı dağıtacak"
python -m src.search "üretim kapasitesi" --ticker EREGL
python -m src.search "yönetim kurulu" --since 2026-04-01
python -m src.search "yabancı yatırımcı" --top-k 10
```

Programmatic:

```python
from src.search import semantic_search

results = semantic_search(
    "fabrika yatırımı",
    top_k=5,
    ticker="TUPRS",
    since="2026-03-01",
)
for r in results:
    print(r["score"], r["subject"], r["url"])
```

## ⚙️ Konfigürasyon

Tüm parametreler `src/config.py` içinde. `.env` üzerinden override:

| Parametre | Default | Override (env) |
|-----------|---------|----------------|
| Tarih aralığı | Son 90 gün | — |
| Başlangıç tarihi | Son 90 gün hesabından gelir | `KAP_START_DATE` |
| Bitiş tarihi | Bugün | `KAP_END_DATE` |
| Lookback gün | `90` | `KAP_LOOKBACK_DAYS` |
| Embedding modeli | `BAAI/bge-m3` | — |
| Chunk size | 800 char | — |
| Qdrant URL | — | `QDRANT_URL` |
| Qdrant API key | — | `QDRANT_API_KEY` |
| Collection adı | `kap_bist30` | `QDRANT_COLLECTION` |
| KAP base URL | `https://www.kap.org.tr` | `KAP_BASE_URL` |
| KAP dil | `tr` | `KAP_LANGUAGE` |
| İndirilecek ek uzantıları | `.pdf` | `KAP_DOWNLOAD_EXTENSIONS` |
| İstek bekleme süresi | `1.0` sn | `KAP_REQUEST_DELAY_SEC` |
| HTTP timeout | `60.0` sn | `KAP_DOWNLOAD_TIMEOUT_SEC` |
| Retry sayısı | `4` | `KAP_MAX_RETRIES` |
| Retry bekleme çarpanı | `2.0` sn | `KAP_RETRY_BACKOFF_SEC` |

## 💡 Qdrant Cloud notları

- **Free tier**: 1 GB RAM, 4 GB disk → ~200K-500K chunk kapasitesi. BIST 30 × 3 ay için 10x fazlasıyla yeterli.
- **Suspend riski**: 1 hafta inaktivite sonrası cluster suspend olur. Veri korunur, tekrar başlatılır.
- **Dashboard**: Qdrant Cloud paneli üzerinden cluster detayına girip **Open Dashboard** ile collection'ları görsel olarak inceleyebilirsiniz.
- **Bağlantı kopuklarsa**: `python -m src.test_connection` ile teşhis. Genelde API key süresi dolmuş veya yeniden oluşturulmuş olur.

## ⚠️ KAP web indirme notları

İndirme MKK API Portal/gateway kullanmaz. KAP bildirim sorgu sayfasındaki halka açık web akışıyla şirket kaydı bulunur; her bildirim için KAP'ın ürettiği bildirim PDF'i ve varsa PDF ek dosyaları `data/pdfs/{TICKER}` altına yazılır. Default `request_delay_sec=1.0` makul hızda çalışır.

## 📝 Sonraki adımlar (akademik scope)

- **Fon raporları**: KAP fon bildirim sorgusu aynı pipeline'a ikinci kaynak olarak eklenebilir.
- **DataKapital FinAI entegrasyonu**: `search.semantic_search()` doğrudan RAG bağlamı olarak çağrılabilir.
- **Uzman skorlama UI**: `search()` çıktısı + LLM cevabı yan yana gösteren basit Streamlit/Gradio.
