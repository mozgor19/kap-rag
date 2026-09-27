
import os

from dotenv import load_dotenv
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import faithfulness, context_precision, context_recall, answer_similarity
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings

load_dotenv()
api_key = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise SystemExit("GOOGLE_API_KEY bulunamadı: .env dosyasına GOOGLE_API_KEY=... ekleyin.")

# Hakem LLM — Gemini. Bu modelin üretim (generateContent) kotası olan bir anahtar gerekir.
lc_llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=api_key)
# Embeddings — Gemini embedding yerine projenin yerel modeli (ücretsiz, kotasız).
lc_emb = HuggingFaceEmbeddings(model_name="BAAI/bge-m3")

ragas_llm = LangchainLLMWrapper(lc_llm)
ragas_emb = LangchainEmbeddingsWrapper(lc_emb)

data = {
    "user_input": [
        "ASTOR hissesi son 2 haftada nasıl bir fiyat hareketi sergiledi?",
        "Son 2 haftadaki fiyat verilerine göre EREGL hissesi nasıl seyretmiştir?",
        "AKBNK hissesinde son 2 haftalık trend nasıl oluşmuştur?",
        "Son 2 hafta itibarıyla SASA hissesi nasıl fiyatlanmaktadır?",
        "HEKTS hissesinin son 2 haftadaki performansı nasıl değerlendirilebilir?",
        "ASELS hissesi son 1 ayda nasıl bir performans sergilemiştir?",
        "Son 1 aylık fiyat verisine göre BIMAS hissesinin seyri nasıldır?",
        "FROTO hissesinde son 1 aydaki fiyat hareketi nasıl olmuştur?",
        "Son 1 ay içinde PETKM hissesinin fiyat trendi nasıl oluşmuştur?",
        "TCELL hissesi son 1 aylık dönemde nasıl fiyatlanmıştır?",
        "GUBRF hissesi son 2 ayda nasıl bir seyir izlemiştir?",
        "Son 2 aylık fiyat verilerine göre TUPRS hissesinin performansı nasıldır?",
        "THYAO hissesinde son 2 aydaki fiyat hareketi nasıl değerlendirilebilir?",
        "Son 2 ay itibarıyla MGROS hissesinin fiyat trendi nasıl oluşmuştur?",
        "EKGYO hissesi son 2 aylık dönemde nasıl fiyatlanmıştır?",
        "GARAN hissesi son 3 ayda nasıl bir performans sergilemiştir?",
        "Son 3 aylık fiyat verisine göre VAKBN hissesinin seyri nasıldır?",
        "OYAKC hissesinde son 3 aydaki fiyat hareketi nasıl olmuştur?",
        "Son 3 ay itibarıyla YKBNK hissesinin fiyat trendi nasıl değerlendirilebilir?",
        "SAHOL hissesi son 3 aylık dönemde nasıl fiyatlanmıştır?"
    ],
    "retrieved_contexts": [
        ["Start: 326.0 (08 May 2026), End: 345.0 (22 May 2026), Change: %5.8, Min: 322.0 (15 May 2026), Max: 345.0 (22 May 2026)"],
        ["Start: 41.26 (08 May 2026), End: 38.68 (22 May 2026), Change: %-6.3, Min: 38.68 (22 May 2026), Max: 41.26 (08 May 2026)"],
        ["Start: 75.25 (08 May 2026), End: 63.6 (22 May 2026), Change: %-15.5, Min: 63.6 (22 May 2026), Max: 75.25 (08 May 2026)"],
        ["Start: 3.52 (08 May 2026), End: 2.65 (22 May 2026), Change: %-24.7, Min: 2.65 (22 May 2026), Max: 3.52 (08 May 2026)"],
        ["Start: 4.44 (08 May 2026), End: 3.84 (22 May 2026), Change: %-13.5, Min: 3.84 (22 May 2026), Max: 4.59 (15 May 2026)"],
        ["Start: 392.0 (24 Apr 2026), End: 410.0 (22 May 2026), Change: %4.6, Min: 392.0 (24 Apr 2026), Max: 428.5 (08 May 2026)"],
        ["Start: 380.0 (24 Apr 2026), End: 392.75 (22 May 2026), Change: %3.4, Min: 370.75 (01 May 2026), Max: 405.25 (15 May 2026)"],
        ["Start: 104.5 (24 Apr 2026), End: 86.85 (22 May 2026), Change: %-16.9, Min: 86.85 (22 May 2026), Max: 104.5 (24 Apr 2026)"],
        ["Start: 23.16 (24 Apr 2026), End: 23.22 (22 May 2026), Change: %0.3, Min: 23.16 (24 Apr 2026), Max: 26.0 (15 May 2026)"],
        ["Start: 114.3 (24 Apr 2026), End: 106.5 (22 May 2026), Change: %-6.8, Min: 106.5 (22 May 2026), Max: 120.0 (08 May 2026)"],
        ["Start: 462.75 (27 Mar 2026), End: 544.5 (22 May 2026), Change: %17.7, Min: 462.75 (27 Mar 2026), Max: 607.0 (08 May 2026)"],
        ["Start: 240.5 (27 Mar 2026), End: 243.1 (22 May 2026), Change: %1.1, Min: 240.5 (27 Mar 2026), Max: 271.0 (01 May 2026)"],
        ["Start: 294.0 (27 Mar 2026), End: 288.0 (22 May 2026), Change: %-2.0, Min: 288.0 (22 May 2026), Max: 329.0 (17 Apr 2026)"],
        ["Start: 598.95 (27 Mar 2026), End: 686.5 (22 May 2026), Change: %14.6, Min: 596.96 (03 Apr 2026), Max: 686.5 (22 May 2026)"],
        ["Start: 19.27 (27 Mar 2026), End: 19.29 (22 May 2026), Change: %0.1, Min: 19.27 (27 Mar 2026), Max: 22.34 (17 Apr 2026)"],
        ["Start: 153.88 (27 Feb 2026), End: 122.3 (22 May 2026), Change: %-20.5, Min: 121.59 (27 Mar 2026), Max: 153.88 (27 Feb 2026)"],
        ["Start: 41.08 (27 Feb 2026), End: 30.0 (22 May 2026), Change: %-27.0, Min: 30.0 (22 May 2026), Max: 41.08 (27 Feb 2026)"],
        ["Start: 24.5 (27 Feb 2026), End: 20.74 (22 May 2026), Change: %-15.3, Min: 20.74 (22 May 2026), Max: 25.6 (10 Apr 2026)"],
        ["Start: 43.3 (27 Feb 2026), End: 32.86 (22 May 2026), Change: %-24.1, Min: 32.86 (22 May 2026), Max: 43.3 (27 Feb 2026)"],
        ["Start: 99.21 (27 Feb 2026), End: 89.15 (22 May 2026), Change: %-10.1, Min: 87.69 (27 Mar 2026), Max: 105.1 (17 Apr 2026)"]
    ],
    "response": [
        "Son 2 haftada ASTOR hissesi 326 TL'den 345 TL'ye yükselerek %5,8 oranında artış göstermiştir. En düşük seviye 15 Mayıs'ta 322 TL, en yüksek seviye ise 22 Mayıs'ta 345 TL olmuştur.",
        "EREGL hissesi son 2 haftada 41,26 TL'den 38,68 TL'ye gerilemiş ve toplamda %6,3 düşüş yaşamıştır. Bu dönemde 22 Mayıs'ta en düşük seviye olan 38,68 TL, 8 Mayıs'ta ise en yüksek seviye olan 41,26 TL kaydedilmiştir.",
        "AKBNK son 2 haftada 75,25 TL'den 63,6 TL'ye düşerek %15,5 oranında değer kaybetmiştir. 22 Mayıs'ta en düşük seviye 63,6 TL, 8 Mayıs'ta ise en yüksek seviye 75,25 TL olmuştur.",
        "SASA hissesi 2 haftalık dönemde 3,52 TL'den 2,65 TL'ye gerileyerek %24,7 düşmüştür. 22 Mayıs tarihinde en düşük seviye 2,65 TL, 8 Mayıs'ta ise en yüksek seviye 3,52 TL olarak kaydedilmiştir.",
        "HEKTS hissesi 2 haftada 4,44 TL'den 3,84 TL'ye düşerek %13,5 oranında değer kaybı yaşamıştır. En düşük fiyat 22 Mayıs'ta 3,84 TL olurken, 15 Mayıs'ta en yüksek fiyat 4,59 TL olarak görülmüştür.",
        "ASELS hissesi son 1 ayda 392 TL'den 410 TL'ye yükselmiş, böylece %4,6 artış kaydetmiştir. 24 Nisan'da en düşük fiyat 392 TL, 8 Mayıs'ta ise en yüksek seviye 428,5 TL olmuştur.",
        "BIMAS hissesi son 1 ayda 380 TL'den 392,75 TL'ye yükselerek %3,4 oranında artmıştır. 1 Mayıs'ta en düşük seviye 370,75 TL, 15 Mayıs'ta ise en yüksek seviye 405,25 TL kaydedilmiştir.",
        "FROTO hissesi 1 ayda 104,5 TL'den 86,85 TL'ye gerileyerek %16,9 oranında düşüş göstermiştir. Bu dönemde 22 Mayıs'ta en düşük fiyat 86,85 TL, 24 Nisan'da en yüksek fiyat 104,5 TL olmuştur.",
        "PETKM hissesi son 1 ayda 23,16 TL'den 23,22 TL'ye yükselmiş ve %0,3 oranında artış kaydetmiştir. En düşük fiyat 24 Nisan'da 23,16 TL, en yüksek fiyat 15 Mayıs'ta 26 TL olmuştur.",
        "TCELL hissesi 1 aylık dönemde 114,3 TL'den 106,5 TL'ye düşmüş, toplam kayıp oranı %6,8 olmuştur. En düşük fiyat 22 Mayıs'ta 106,5 TL, en yüksek fiyat 8 Mayıs'ta 120 TL olarak gerçekleşmiştir.",
        "GUBRF hissesi son 2 ayda 462,75 TL'den 544,5 TL'ye yükselmiş ve %17,7 oranında değer kazanmıştır. En düşük fiyat 27 Mart'ta 462,75 TL, en yüksek fiyat 8 Mayıs'ta 607 TL olarak görülmüştür.",
        "TUPRS hissesi 2 ayda 240,5 TL'den 243,1 TL'ye yükselmiş, toplam artış oranı %1,1 olmuştur. En düşük fiyat 27 Mart'ta 240,5 TL, en yüksek fiyat 1 Mayıs'ta 271 TL olarak kaydedilmiştir.",
        "THYAO hissesi 2 ayda 294 TL'den 288 TL'ye düşerek %2 oranında gerilemiştir. Bu süreçte en düşük fiyat 22 Mayıs'ta 288 TL, en yüksek fiyat ise 17 Nisan'da 329 TL olarak gerçekleşmiştir.",
        "MGROS hissesi 2 ayda 598,95 TL'den 686,5 TL'ye yükselmiş ve %14,6 oranında artış göstermiştir. En düşük fiyat 3 Nisan'da 596,96 TL, en yüksek fiyat 22 Mayıs'ta 686,5 TL olmuştur.",
        "EKGYO hissesi son 2 ayda 19,27 TL'den 19,29 TL'ye sınırlı bir artış göstermiştir. En düşük fiyat 27 Mart'ta 19,27 TL, en yüksek fiyat 17 Nisan'da 22,34 TL olmuştur.",
        "GARAN hissesi 3 ayda 153,88 TL'den 122,3 TL'ye düşmüş ve %20,5 oranında değer kaybetmiştir. En düşük fiyat 27 Mart'ta 121,59 TL, en yüksek fiyat 27 Şubat'ta 153,88 TL olarak kaydedilmiştir.",
        "VAKBN hissesi son 3 ayda 41,08 TL'den 30 TL'ye gerilemiş ve %27 oranında düşmüştür. En düşük fiyat 22 Mayıs'ta 30 TL, en yüksek fiyat 27 Şubat'ta 41,08 TL olmuştur.",
        "OYAKC hissesi 3 ayda 24,5 TL'den 20,74 TL'ye düşerek %15,3 oranında azalmıştır. Bu dönemde 22 Mayıs'ta en düşük seviye 20,74 TL olarak gerçekleşmiş, en yüksek fiyat 10 Nisan'da 25,6 TL olmuştur.",
        "YKBNK hissesi son 3 ayda 43,3 TL'den 32,86 TL'ye düşerek %24,1 oranında kayıp yaşamıştır. En düşük seviye 22 Mayıs'ta 32,86 TL, en yüksek seviye 27 Şubat'ta 43,3 TL olmuştur.",
        "SAHOL hissesi 3 ayda 99,21 TL'den 89,15 TL'ye gerilemiş ve %10,1 oranında değer kaybetmiştir. En düşük seviye 27 Mart'ta 87,69 TL, en yüksek seviye 17 Nisan'da 105,1 TL olarak kaydedilmiştir."
    ],
    "reference": [
        "ASTOR hissesi son 2 hafta içinde 08 May 2026 kapanışındaki 326.00 TL seviyesinden 22 May 2026 itibarıyla 345.00 TL'ye yükselmiş ve %5.8 değişim kaydetmiştir.",
        "EREGL hissesi son 2 hafta içinde 08 May 2026 kapanışındaki 41.26 TL seviyesinden 22 May 2026 itibarıyla 38.68 TL'ye gerilemiş ve %6.3 değişim kaydetmiştir.",
        "AKBNK hissesi son 2 hafta içinde 08 May 2026 kapanışındaki 75.25 TL seviyesinden 22 May 2026 itibarıyla 63.60 TL'ye gerilemiş ve %15.5 değişim kaydetmiştir.",
        "SASA hissesi son 2 hafta içinde 08 May 2026 kapanışındaki 3.52 TL seviyesinden 22 May 2026 itibarıyla 2.65 TL'ye gerilemiş ve %24.7 değişim kaydetmiştir.",
        "HEKTS hissesi son 2 hafta içinde 08 May 2026 kapanışındaki 4.44 TL seviyesinden 22 May 2026 itibarıyla 3.84 TL'ye gerilemiş ve %13.5 değişim kaydetmiştir.",
        "ASELS hissesi son 1 ay içinde 24 Apr 2026 kapanışındaki 392.00 TL seviyesinden 22 May 2026 itibarıyla 410.00 TL'ye yükselmiş ve %4.6 değişim kaydetmiştir.",
        "BIMAS hissesi son 1 ay içinde 24 Apr 2026 kapanışındaki 380.00 TL seviyesinden 22 May 2026 itibarıyla 392.75 TL'ye yükselmiş ve %3.4 değişim kaydetmiştir.",
        "FROTO hissesi son 1 ay içinde 24 Apr 2026 kapanışındaki 104.50 TL seviyesinden 22 May 2026 itibarıyla 86.85 TL'ye gerilemiş ve %16.9 değişim kaydetmiştir.",
        "PETKM hissesi son 1 ay içinde 24 Apr 2026 kapanışındaki 23.16 TL seviyesinden 22 May 2026 itibarıyla 23.22 TL'ye yükselmiş ve %0.3 değişim kaydetmiştir.",
        "TCELL hissesi son 1 ay içinde 24 Apr 2026 kapanışındaki 114.30 TL seviyesinden 22 May 2026 itibarıyla 106.50 TL'ye gerilemiş ve %6.8 değişim kaydetmiştir.",
        "GUBRF hissesi son 2 ay içinde 27 Mar 2026 kapanışındaki 462.75 TL seviyesinden 22 May 2026 itibarıyla 544.50 TL'ye yükselmiş ve %17.7 değişim kaydetmiştir.",
        "TUPRS hissesi son 2 ay içinde 27 Mar 2026 kapanışındaki 240.50 TL seviyesinden 22 May 2026 itibarıyla 243.10 TL'ye yükselmiş ve %1.1 değişim kaydetmiştir.",
        "THYAO hissesi son 2 ay içinde 27 Mar 2026 kapanışındaki 294.00 TL seviyesinden 22 May 2026 itibarıyla 288.00 TL'ye gerilemiş ve %2.0 değişim kaydetmiştir.",
        "MGROS hissesi son 2 ay içinde 27 Mar 2026 kapanışındaki 598.95 TL seviyesinden 22 May 2026 itibarıyla 686.50 TL'ye yükselmiş ve %14.6 değişim kaydetmiştir.",
        "EKGYO hissesi son 2 ay içinde 27 Mar 2026 kapanışındaki 19.27 TL seviyesinden 22 May 2026 itibarıyla 19.29 TL'ye yükselmiş ve %0.1 değişim kaydetmiştir.",
        "GARAN hissesi son 3 ay içinde 27 Feb 2026 kapanışındaki 153.88 TL seviyesinden 22 May 2026 itibarıyla 122.30 TL'ye gerilemiş ve %20.5 değişim kaydetmiştir.",
        "VAKBN hissesi son 3 ay içinde 27 Feb 2026 kapanışındaki 41.08 TL seviyesinden 22 May 2026 itibarıyla 30.00 TL'ye gerilemiş ve %27.0 değişim kaydetmiştir.",
        "OYAKC hissesi son 3 ay içinde 27 Feb 2026 kapanışındaki 24.50 TL seviyesinden 22 May 2026 itibarıyla 20.74 TL'ye gerilemiş ve %15.3 değişim kaydetmiştir.",
        "YKBNK hissesi son 3 ay içinde 27 Feb 2026 kapanışındaki 43.30 TL seviyesinden 22 May 2026 itibarıyla 32.86 TL'ye gerilemiş ve %24.1 değişim kaydetmiştir.",
        "SAHOL hissesi son 3 ay içinde 27 Feb 2026 kapanışındaki 99.21 TL seviyesinden 22 May 2026 itibarıyla 89.15 TL'ye gerilemiş ve %10.1 değişim kaydetmiştir."
    ]
}

dataset = Dataset.from_dict(data)

# Değerlendirmeyi çalıştır
from ragas.run_config import RunConfig
run_config = RunConfig(timeout=120, max_retries=3, max_wait=60, max_workers=4)

results = evaluate(
    dataset,
    metrics=[faithfulness, context_precision, context_recall, answer_similarity],
    llm=ragas_llm,
    embeddings=ragas_emb,
    run_config=run_config,
)

print("---- Ragas Değerlendirme Sonuçları ---")
print(results)

df = results.to_pandas()
df.to_csv("rag_performans_raporu.csv", index=False)
print("Detaylı rapor 'rag_performans_raporu.csv' dosyasına kaydedildi.")
