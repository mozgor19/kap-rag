"""
Kullanım kılavuzunu PDF olarak üretir.
Çalıştır: python docs/make_pdf.py
"""
from __future__ import annotations
from fpdf import FPDF
from pathlib import Path

OUT = Path(__file__).parent / "kap_rag_kullanim_kilavuzu.pdf"

FONT_REGULAR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"

SECTIONS = [
    {
        "title": "KAP-RAG: BIST30 Bildirim Arama Sistemi",
        "subtitle": "Kullanım Kılavuzu ve Örnek Sorgular",
        "body": None,
    },
    {
        "title": "1. Proje Özeti",
        "body": (
            "KAP-RAG, Kamuyu Aydınlatma Platformu (KAP) üzerinde yayınlanan "
            "BIST30 şirketlerinin bildirim PDF'lerini indirerek vektör veritabanına "
            "yükleyen ve doğal dil sorgularıyla semantik arama yapılmasını sağlayan "
            "bir RAG (Retrieval-Augmented Generation) altyapısıdır.\n\n"
            "Veri kaynağı  : KAP (kap.org.tr) — herkese açık bildirim uçları\n"
            "Vektör DB     : Qdrant (Cloud veya lokal Docker)\n"
            "Embedding     : BAAI/bge-m3 (1024 boyut, çok dilli)\n"
            "Kapsam        : BIST30 hisseleri, son 90 gün (yapılandırılabilir)\n"
            "Bildirim tipleri: FR (Finansal Rapor), ODA (Özel Durum),\n"
            "                  CA (Genel Kurul), DG (Diğer), DUY (Duyuru)"
        ),
    },
    {
        "title": "2. Sistem Gereksinimleri",
        "body": (
            "Python       : 3.10+\n"
            "GPU          : Opsiyonel (bge-m3 CPU'da da çalışır, yavaştır)\n"
            "Disk         : ~900 MB (PDF'ler ~760 MB, model ~2 GB)\n"
            "Qdrant       : Cloud hesabı VEYA Docker (localhost:6333)\n\n"
            "Bağımlılıklar (pip install -r requirements.txt):\n"
            "  httpx, pypdf, sentence-transformers, qdrant-client, python-dotenv"
        ),
    },
    {
        "title": "3. Kurulum",
        "body": (
            "# 1. Repoyu klonla\n"
            "git clone https://github.com/mozgor19/kap-rag.git\n"
            "cd kap-rag\n\n"
            "# 2. Sanal ortam\n"
            "python -m venv .venv\n"
            "source .venv/bin/activate  # Windows: .venv\\Scripts\\activate\n\n"
            "# 3. Bağımlılıklar\n"
            "pip install -r requirements.txt\n\n"
            "# 4. Ortam değişkenleri\n"
            "cp .env.example .env\n"
            "# .env dosyasını düzenleyip Qdrant bilgilerini gir"
        ),
    },
    {
        "title": "4. Pipeline Adımları",
        "body": (
            "Pipeline 4 adımdan oluşur; her adım bağımsız çalıştırılabilir.\n\n"
            "ADIM 1 — Veri İndirme\n"
            "  python -m src.pipeline --steps download\n"
            "  KAP'tan tüm BIST30 şirketlerinin son 90 günlük bildirimlerini\n"
            "  ve PDF eklerini data/pdfs/ altına indirir.\n\n"
            "ADIM 2 — PDF Parse & Chunking\n"
            "  python -m src.pipeline --steps parse\n"
            "  PDF'leri metne dönüştürür, 800 karakter (150 örtüşmeli) chunk'lara\n"
            "  böler; sonuç: data/text/chunks.jsonl (58.000+ chunk).\n\n"
            "ADIM 3 — Embed & İndeksleme\n"
            "  python -m src.pipeline --steps embed\n"
            "  Chunk'ları bge-m3 modeli ile vektörleştirip Qdrant'a yazar.\n"
            "  GPU varsa otomatik kullanır.\n\n"
            "ADIM 4 — Arama Testi\n"
            "  python -m src.pipeline --steps search --query \"sorgu metni\"\n"
            "  Belirtilen sorgu için Qdrant'ta semantik arama yapar.\n\n"
            "Tüm adımları birden çalıştırmak için:\n"
            "  python -m src.pipeline"
        ),
    },
    {
        "title": "5. Arama Komutları",
        "body": (
            "Temel kullanım:\n"
            "  python -m src.search \"<sorgu>\"\n\n"
            "Parametreler:\n"
            "  --top-k N              Kaç sonuç dönsün (varsayılan: 5)\n"
            "  --ticker THYAO         Belirli bir hisseye kısıtla\n"
            "  --disclosure-type FR   Bildirim tipine göre filtrele\n"
            "  --since YYYY-MM-DD     Bu tarihten itibaren\n"
            "  --until YYYY-MM-DD     Bu tarihe kadar\n\n"
            "Disclosure type kodları:\n"
            "  FR  — Finansal Rapor (yıllık/çeyreklik)\n"
            "  ODA — Özel Durum Açıklaması\n"
            "  CA  — Genel Kurul / Çeşitli\n"
            "  DG  — Diğer\n"
            "  DUY — Duyuru"
        ),
    },
    {
        "title": "6. Örnek Sorgu — Finansal Performans",
        "body": (
            "Komut:\n"
            "  python -m src.pipeline --steps search \\\n"
            "    --query \"şirketin son finansal performansı ve karlılığı\"\n\n"
            "Örnek Çıktı:\n"
            "  [1] (skor=0.6430) AKSEN | Faaliyet Raporu (Konsolide)  |  FR\n"
            "      2026-03-05  |  kap.org.tr/tr/Bildirim/1566680\n"
            "      \"FİNANSAL DURUM Şirketin özet finansal rakamları ile kârlılık\n"
            "       durumuna ilişkin tabloları aşağıda yer almaktadır.\n"
            "       Dönen Varlıklar 19.990.857.936 ... Toplam 129.590.455.824\"\n\n"
            "  [2] (skor=0.6417) AKSEN | Faaliyet Raporu (Konsolide)  |  FR\n"
            "      2026-05-11  |  kap.org.tr/tr/Bildirim/1605542\n"
            "      \"31 Mart 2026 Dönen Varlıklar 18.453.221.231\n"
            "       Toplam Varlıklar 138.902.758.229\"\n\n"
            "  [5] (skor=0.6337) PGSUS | Finansal Rapor  |  FR\n"
            "      2026-03-04  |  kap.org.tr/tr/Bildirim/1566087\n"
            "      \"Sales 154.127.554.444 TL | Cost of sales 127.931.805.322 TL\"\n\n"
            "Yorum: Tüm sonuçlar FR tipinde, bilanço/gelir tablosu içeriyor. Skor\n"
            "0.63-0.64 aralığı, finansal raporların standart terminoloji içermesi\n"
            "nedeniyle beklenen değerdir."
        ),
    },
    {
        "title": "7. Örnek Sorgu — Temettü",
        "body": (
            "Komut:\n"
            "  python -m src.pipeline --steps search \\\n"
            "    --query \"temettü kar payı dağıtım kararı\"\n\n"
            "Örnek Çıktı:\n"
            "  [1] (skor=0.6998) EKGYO | Faaliyet Raporu (Konsolide)  |  FR\n"
            "      2026-03-07  |  kap.org.tr/tr/Bildirim/1567860\n"
            "      \"işçilere kardan pay dağıtılmasına karar verilemeyeceği gibi,\n"
            "       belirlenen birinci temettü dağıtılmadıkça...\"\n\n"
            "  [2] (skor=0.6859) TOASO | Faaliyet Raporu (Konsolide)  |  FR\n"
            "      2026-05-05  |  kap.org.tr/tr/Bildirim/1601475\n"
            "      \"Nakit Kar Payı (Temettü) Dağıtımı — ortaklarımıza %2000\n"
            "       oranında (brüt) temettü dağıtılmasına karar verilmiştir.\"\n\n"
            "Yorum: En yüksek skor (0.70), sorgunun doğrudan temettü metni içeren\n"
            "chunk'larla eşleştiğini gösteriyor."
        ),
    },
    {
        "title": "8. Örnek Sorgu — Ticker + Filtre",
        "body": (
            "Komut:\n"
            "  python -m src.search \"banka kredi büyümesi net faiz marjı\" \\\n"
            "    --ticker AKBNK\n\n"
            "Örnek Çıktı:\n"
            "  [1] (skor=0.6604) AKBNK | Faaliyet Raporu (Konsolide)  |  FR\n"
            "      2026-03-02  |  kap.org.tr/tr/Bildirim/1564365\n"
            "      \"yıllık TL kredi büyümesi yaklaşık %44,0, YP kredi yıllık\n"
            "       büyümesi ise ABD Doları cinsinden yaklaşık %19\"\n\n"
            "  [3] (skor=0.6240) AKBNK | Finansal Rapor  |  FR\n"
            "      2026-04-28  |  kap.org.tr/tr/Bildirim/1598264\n"
            "      \"2026 Beklentileri: TL Kredi Büyümesi > %30\n"
            "       Net Faiz Marjı (Swap düzeltilmiş) ~ %4\"\n\n"
            "Yorum: --ticker filtresi tüm sonuçları yalnızca AKBNK ile sınırladı.\n"
            "Gelen chunk'lar gerçek KAP finansal verisi içeriyor (halüsinasyon yok)."
        ),
    },
    {
        "title": "9. Örnek Sorgu — Trafik Verileri (THYAO)",
        "body": (
            "Komut:\n"
            "  python -m src.pipeline --steps search \\\n"
            "    --query \"Türk Hava Yolları yolcu trafik sonuçları\"\n\n"
            "Örnek Çıktı:\n"
            "  [1] (skor=0.6792) THYAO | Özel Durum Açıklaması (Genel)  |  ODA\n"
            "      2026-04-29  |  kap.org.tr/tr/Bildirim/1598902\n"
            "      \"January-March 2026: Passengers Carried 21M (+12.7%)\n"
            "       Fleet 528 (+11.9%)  |  Load Factor 83.5% (+2.9 puan)\"\n\n"
            "  [2] (skor=0.6672) THYAO | Faaliyet Raporu (Konsolide)  |  FR\n"
            "      2026-04-29  |  kap.org.tr/tr/Bildirim/1598900\n"
            "      \"3A'26: Yolcu Sayısı 21 milyon (%12.7 artış)\n"
            "       Kargo+Posta 552 bin ton (%14.8 artış)\"\n\n"
            "Yorum: Sorgu şirket adını içerdiği hâlde tüm 5 sonuç THYAO geldi.\n"
            "Model 'Türk Hava Yolları' ile THYAO ticker'ını ilişkilendirebildi."
        ),
    },
    {
        "title": "10. Yapılandırma Referansı",
        "body": (
            ".env dosyasındaki temel değişkenler:\n\n"
            "QDRANT_URL        Qdrant Cloud endpoint URL'i\n"
            "                  (Boş bırakılırsa localhost:6333 kullanılır)\n"
            "QDRANT_API_KEY    Qdrant Cloud API anahtarı\n"
            "QDRANT_COLLECTION Collection adı (varsayılan: kap_bist30)\n\n"
            "KAP_START_DATE    Başlangıç tarihi YYYY-MM-DD (boş = otomatik)\n"
            "KAP_END_DATE      Bitiş tarihi YYYY-MM-DD (boş = bugün)\n"
            "KAP_LOOKBACK_DAYS Kaç gün geriye git (varsayılan: 90)\n\n"
            "KAP_REQUEST_DELAY_SEC   İstekler arası bekleme (varsayılan: 1.0)\n"
            "KAP_MAX_RETRIES         Yeniden deneme sayısı (varsayılan: 4)\n\n"
            "Sadece belirli tickerlar için indirme:\n"
            "  python -m src.pipeline --steps download --tickers THYAO GARAN"
        ),
    },
    {
        "title": "11. Mimari Özeti",
        "body": (
            "                   ┌─────────────┐\n"
            "                   │  KAP Web    │\n"
            "                   │  (kap.org.tr│\n"
            "                   └──────┬──────┘\n"
            "                          │ HTTP scraping\n"
            "                   ┌──────▼──────┐\n"
            "            ┌──────│  download   │ PDF + metadata\n"
            "            │      └─────────────┘\n"
            "            │\n"
            "            │      ┌─────────────┐\n"
            "            └─────►│    parse    │ chunk (800 char)\n"
            "                   └──────┬──────┘\n"
            "                          │\n"
            "                   ┌──────▼──────┐\n"
            "                   │   embed     │ BAAI/bge-m3\n"
            "                   └──────┬──────┘\n"
            "                          │ upsert\n"
            "                   ┌──────▼──────┐\n"
            "                   │   Qdrant    │ 1024-dim cosine\n"
            "                   │  (Cloud)    │\n"
            "                   └──────┬──────┘\n"
            "                          │ semantic_search()\n"
            "                   ┌──────▼──────┐\n"
            "                   │   search    │ top-k + filter\n"
            "                   └─────────────┘\n\n"
            "Veri akışı:\n"
            "  data/pdfs/{TICKER}/*.pdf\n"
            "  data/metadata/{TICKER}.json\n"
            "  data/text/chunks.jsonl  →  Qdrant collection: kap_bist30"
        ),
    },
    {
        "title": "12. Bilinen Sınırlamalar",
        "body": (
            "1. Standart SPK metni eşleşmesi\n"
            "   Faaliyet raporlarının yasal zorunlu bölümleri (yönetim kurulunun\n"
            "   sorumluluğu, bağımsız denetçi beyanı vb.) tüm şirketlerde aynıdır.\n"
            "   Bu chunk'lar yüksek benzerlik skoru ile gelebilir; içerik yerine\n"
            "   boilerplate metin döndürme riski taşır.\n\n"
            "2. Cosine benzerlik skoru 0.62-0.70 aralığında\n"
            "   Finansal terminolojinin standart ve tekrarlı yapısı nedeniyle\n"
            "   skorlar 0.80+ seviyesine ulaşmıyor. Bu bge-m3'ün finansal\n"
            "   Türkçe üzerindeki bilinen bir karakteristiğidir.\n\n"
            "3. İki dilli PDF\n"
            "   Bazı şirketlerin raporları hem Türkçe hem İngilizce içermektedir.\n"
            "   Sorgu dilinin belge diliyle eşleşmesi skor kalitesini artırır."
        ),
    },
]

COLORS = {
    "cover_bg": (15, 55, 105),
    "cover_text": (255, 255, 255),
    "title_bar": (30, 80, 140),
    "title_text": (255, 255, 255),
    "body_text": (30, 30, 30),
    "code_bg": (240, 244, 248),
    "code_text": (40, 60, 100),
    "section_line": (30, 80, 140),
}

class KapPDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=20)
        self.set_margins(20, 20, 20)
        self.add_font("DejaVu", "", FONT_REGULAR)
        self.add_font("DejaVu", "B", FONT_BOLD)
        self.add_font("DejaVuMono", "", FONT_MONO)

    def _is_code(self, line: str) -> bool:
        stripped = line.lstrip()
        return (
            stripped.startswith("#")
            or stripped.startswith("python")
            or stripped.startswith("pip")
            or stripped.startswith("git")
            or stripped.startswith("source")
            or stripped.startswith("cp")
            or stripped.startswith("cd")
            or stripped.startswith("--")
            or "└" in line
            or "┌" in line
            or "│" in line
            or "▼" in line
            or "►" in line
            or stripped.startswith("data/")
            or "    " == line[:4]
        )

    def header(self):
        pass

    def footer(self):
        self.set_y(-12)
        self.set_font("DejaVu", "", 8)
        self.set_text_color(140, 140, 140)
        self.cell(0, 5, f"KAP-RAG Kullanım Kılavuzu  |  Sayfa {self.page_no()}", align="C")

    def cover_page(self, title: str, subtitle: str):
        self.add_page()
        r, g, b = COLORS["cover_bg"]
        self.set_fill_color(r, g, b)
        self.rect(0, 0, 210, 297, "F")

        W = 170  # usable width

        self.set_y(80)
        self.set_x(20)
        self.set_font("DejaVu", "B", 28)
        self.set_text_color(*COLORS["cover_text"])
        self.multi_cell(W, 12, title, align="C")

        self.set_y(self.get_y() + 10)
        self.set_x(20)
        self.set_font("DejaVu", "", 14)
        self.set_text_color(180, 210, 240)
        self.multi_cell(W, 8, subtitle, align="C")

        self.set_y(self.get_y() + 20)
        self.set_x(20)
        self.set_font("DejaVu", "", 11)
        self.set_text_color(160, 200, 230)
        self.multi_cell(W, 7, "BIST30  |  KAP Bildirimleri  |  RAG Mimarisi", align="C")
        self.set_x(20)
        self.multi_cell(W, 7, "BAAI/bge-m3  |  Qdrant Vector DB", align="C")

        self.set_y(250)
        self.set_x(20)
        self.set_font("DejaVu", "", 9)
        self.set_text_color(140, 170, 200)
        self.multi_cell(W, 6, "mozgor19  |  2026", align="C")

    def section(self, title: str, body: str):
        self.add_page()

        # Title bar
        r, g, b = COLORS["title_bar"]
        self.set_fill_color(r, g, b)
        self.rect(0, 0, 210, 18, "F")
        self.set_y(4)
        self.set_x(20)
        self.set_font("DejaVu", "B", 13)
        self.set_text_color(*COLORS["title_text"])
        self.cell(0, 10, title)

        self.set_y(26)
        self.set_text_color(*COLORS["body_text"])

        for line in body.split("\n"):
            if self._is_code(line):
                y = self.get_y()
                r2, g2, b2 = COLORS["code_bg"]
                self.set_fill_color(r2, g2, b2)
                self.rect(18, y, 172, 5.5, "F")
                self.set_font("DejaVuMono", "", 8)
                self.set_text_color(*COLORS["code_text"])
                self.set_x(21)
                self.cell(0, 5.5, line)
                self.ln()
            else:
                self.set_font("DejaVu", "", 10)
                self.set_text_color(*COLORS["body_text"])
                self.set_x(20)
                if line.strip() == "":
                    self.ln(3)
                else:
                    self.multi_cell(170, 5.5, line)


def build():
    pdf = KapPDF()

    cover = SECTIONS[0]
    pdf.cover_page(cover["title"], cover["subtitle"])

    for sec in SECTIONS[1:]:
        pdf.section(sec["title"], sec["body"])

    OUT.parent.mkdir(parents=True, exist_ok=True)
    pdf.output(str(OUT))
    print(f"PDF oluşturuldu: {OUT}")


if __name__ == "__main__":
    build()
