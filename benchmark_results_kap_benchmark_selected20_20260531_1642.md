# KAP-RAG Benchmark — RAG Sonuçları

**Üretildi:** 2026-05-31 16:42  
**Dataset:** KAP-RAG Benchmark — Seçili 20 Soru vv4_scored  
**Evaluation target:** retrieval_and_extraction_faithfulness  
**Soru sayısı:** 20  
**Corpus snapshot:** 2026-05-31 (knowledge cutoff: 2026-05-18)  

## Özet Skor Tablosu

| Metrik | Değer |
|--------|-------|
| KAP belgesi recall@k | **13/20 (65%)** |
| Ortalama top-1 cosine skor | 0.6723 |
| Median sorgu süresi | 0.062s |

### Kategori Bazlı Recall

| Kategori | Recall@k | N |
|----------|----------|---|
| banka_kredi_buyumesi | 4/5 | 5 |
| finansal_performans | 4/5 | 5 |
| genel_finansal_durum | 4/5 | 5 |
| temettu | 1/5 | 5 |

> **Not:** Bu recall metriği gold KAP bildirim numarasının top-5 sonuçlarında görünüp görünmediğini ölçer.
> `rag_answer` sütunu LLM üretimi değil, top-1 retrieved chunk'ın ilk 600 karakteridir.

---

## ✓ KAP_RAG_01 · AEFES · finansal_performans · hard

**Dönem:** 2025Y  
**Kaynak belge:** AEFES 2025 Yıllık Faaliyet Raporu (Konsolide) – KAP #1570140, 11.03.2026  
**Top-1 skor:** 0.6776  |  **KAP match:** ✓  |  **Süre:** 8.817s  
**human_validation_required:** False  

### Soru
> Anadolu Efes'in 2025 yılı hisse başı kazancı nedir ve 2024 yılıyla karşılaştırıldığında ne yönde değişmiştir?

### Gold Answer
> 2025 hisse başı kazanç 1,5127 TL'dir; 2024'te 2,8997 TL idi. 2025 yılında gerçekleştirilen 1:10 sermaye artışı (hisse bölünmesi) nedeniyle iki dönem doğrudan karşılaştırılabilir değildir. Kaynak: KAP #1570140, 11.03.2026

### RAG Top-1 Retrieved Chunk  _(retrieval only — LLM generation yok)_

```
2 Barth R
eport 2024-2025, 2024 yıl sonu sonuçlarına göre bilgi paylaşılmıştır. Anadolu Efes, tüketicilerine 
unutulmaz deneyimler 
sunan; faaliyeti bulunan 
toplulukları zenginleştiren, 
duygulara dokunan 
markalarla büyüyen, içecek 
dünyasının en sevilen ve en 
hızlı büyüyen oyuncusu olma 
yolunda ilerleme vizyonu ile 
faaliyetlerini sürdürmektedir. ANADOLU EFES 
ENTEGRE FAALİYET 
RAPORU 2025
GİRİŞ
ANADOLU EFES DÜNYASI
• Kısac
a Anadolu Efes
• Değer Zincirimiz
• Tr
endler ve Faaliyet 
Ortamımız
KURUMSAL YÖNETİŞİM 
YAPIMIZ
GELECEĞE ARTI DEĞER
FİNANSAL DİSİPLİN İLE 
BÜYÜYORUZ
TOPLUMSAL FAYDA İ
```

**Retrieved sources (top-5):**
- [1] skor=`0.6776` — https://www.kap.org.tr/tr/Bildirim/1570140 — Faaliyet Raporu (Konsolide)
- [2] skor=`0.6770` — https://www.kap.org.tr/tr/Bildirim/1566777 — Özel Durum Açıklaması (Genel)
- [3] skor=`0.6762` — https://www.kap.org.tr/tr/Bildirim/1566777 — Özel Durum Açıklaması (Genel)
- [4] skor=`0.6683` — https://www.kap.org.tr/tr/Bildirim/1566777 — Özel Durum Açıklaması (Genel)
- [5] skor=`0.6622` — https://www.kap.org.tr/tr/Bildirim/1601483 — Faaliyet Raporu (Konsolide)

**Gold KAP#:** 1570140 | **Hit KAP#:** 1566777,1570140,1601483

---

## ✓ KAP_RAG_02 · THYAO · finansal_performans · easy

**Dönem:** 2026Q1  
**Kaynak belge:** THYAO Nisan 2026 Konsolide Trafik Sonuçları – KAP ODA #1603784, 08.05.2026  
**Top-1 skor:** 0.6795  |  **KAP match:** ✓  |  **Süre:** 0.06s  
**human_validation_required:** False  

### Soru
> Türk Hava Yolları'nın Nisan 2026 trafik sonuçlarına göre yolcu sayısı, yolcu doluluk oranı ve yıllık değişimleri nedir?

### Gold Answer
> Nisan 2026 yolcu sayısı 7,2 milyon olup bir önceki yılın aynı dönemine göre yüzde 2,9 gerilemiştir. Yolcu doluluk oranı yüzde 83,4 olup 2025 Nisan'ındaki yüzde 83,2'nin 0,2 puan üzerindedir. Kaynak: KAP ODA #1603784

### RAG Top-1 Retrieved Chunk  _(retrieval only — LLM generation yok)_

```
NİSAN 2026 TRAFİK
TÜRK HAVA YOLLARI YATIRIMCI İLİŞKİLERİ 
Telefon: +90 212 463 63 63| E-posta: ir@thy.com
2025 2026 Değişim (%)Arzedilen Koltuk Kilometre (milyar)
2025 2026 Değişim (%)Yolcu Doluluk Oranı (%)
2025 2026 Değişim (%)Yolcu Sayısı (milyon)
BÖLGESEL DAĞILIM

Uçulan Nokta 353 358 %1,4
Uçak Sayısı 476 536 %12,6
Arzedilen Koltuk Kilometre (milyar) 82,7 88,9 %7,5
Yolcu Doluluk Oranı (%) %81,2 %83,4 2,2 pt
Yolcu Sayısı (milyon) 26,3 28,5 %8,3
Konma Sayısı (Yolcu Seferleri) 167.407 177.339 %5,9
Kargo + Posta (bin ton) 653,7 747,0 %14,3
 
Arzedilen Koltuk Kilometre (milyar) 75,2 81,2 %7,9
Y
```

**Retrieved sources (top-5):**
- [1] skor=`0.6795` — https://www.kap.org.tr/tr/Bildirim/1603784 — Özel Durum Açıklaması (Genel)
- [2] skor=`0.6722` — https://www.kap.org.tr/tr/Bildirim/1603784 — Özel Durum Açıklaması (Genel)
- [3] skor=`0.6719` — https://www.kap.org.tr/tr/Bildirim/1566094 — Faaliyet Raporu (Konsolide)
- [4] skor=`0.6709` — https://www.kap.org.tr/tr/Bildirim/1569213 — Özel Durum Açıklaması (Genel)
- [5] skor=`0.6614` — https://www.kap.org.tr/tr/Bildirim/1569213 — Özel Durum Açıklaması (Genel)

**Gold KAP#:** 1603784 | **Hit KAP#:** 1566094,1569213,1603784

---

## ✓ KAP_RAG_03 · FROTO · finansal_performans · easy

**Dönem:** 2026Q1  
**Kaynak belge:** FROTO 1Q2026 Faaliyet Raporu – KAP #1601423, 05.05.2026  
**Top-1 skor:** 0.7284  |  **KAP match:** ✓  |  **Süre:** 0.079s  
**human_validation_required:** False  

### Soru
> Ford Otosan'ın 2026 birinci çeyrek yurt içi toplam perakende satışları, genel pazar payı ve bir önceki yılın aynı dönemine göre değişimi nedir?

### Gold Answer
> 2026Q1 yurt içi perakende satışlar 18.707 adet (-yüzde 20 yıllık). Toplam pazar payı yüzde 6,9 (2025Q1: yüzde 8,3). HTA payı yüzde 18,2 (2025Q1: yüzde 21,6), OTA payı yüzde 32,2 (2025Q1: yüzde 37,6). Kaynak: KAP #1601423

### RAG Top-1 Retrieved Chunk  _(retrieval only — LLM generation yok)_

```
Tüm rapor boyunca parantez içindeki rakamlar geçen yılın aynı dönemine ait olan değerleri göstermektedir. Ford Otosan 2026 1. Çeyrek Faaliyet Raporu 
 
 
Binek araçların toplam pazardaki payı geçen yılın aynı döneminde 
%78,8 iken
 , bu dönem 
%7
 7 olarak kaydedilmiştir
 . Hafif ticari araçların payı ise %20 
ile sabit kalmıştır. Binek 
araçların toplam pazardaki payı 
 (4) 
1Ç'26 
 2025 
 1Ç
'
 2024 
 2023 
 2022 
 2021 
%
 %
 %
 %
 %
 %
 %
Bu dönemde ithal araçların payı binek araçlarda %64 seviyesine gerilerken, hafif ticari 
araçlarda %77’e ulaşmış ve toplamda %67 olarak gerçekleşmiştir.
```

**Retrieved sources (top-5):**
- [1] skor=`0.7284` — https://www.kap.org.tr/tr/Bildirim/1601423 — Faaliyet Raporu (Konsolide)
- [2] skor=`0.7108` — https://www.kap.org.tr/tr/Bildirim/1601423 — Faaliyet Raporu (Konsolide)
- [3] skor=`0.7072` — https://www.kap.org.tr/tr/Bildirim/1601423 — Faaliyet Raporu (Konsolide)
- [4] skor=`0.6979` — https://www.kap.org.tr/tr/Bildirim/1558661 — Faaliyet Raporu (Konsolide)
- [5] skor=`0.6959` — https://www.kap.org.tr/tr/Bildirim/1601425 — Geleceğe Dönük Değerlendirmeler

**Gold KAP#:** 1601423 | **Hit KAP#:** 1558661,1601423,1601425

---

## ✓ KAP_RAG_04 · FROTO · finansal_performans · hard

**Dönem:** 2026Q1  
**Kaynak belge:** FROTO 1Q2026 Faaliyet Raporu – KAP #1601423, 05.05.2026  
**Top-1 skor:** 0.6952  |  **KAP match:** ✓  |  **Süre:** 0.056s  
**human_validation_required:** True  

### Soru
> Ford Otosan 2026 birinci çeyrek raporunda yurt içi satışlardaki düşüşün nedeni olarak hangi gelişmeleri belirtmektedir?

### Gold Answer
> Şirket, Focus modelinin üretiminin sonlanması ardından binek araç satışlarında zayıflama yaşandığını belirtmektedir. Ayrıca daha rekabetçi fiyatlama ortamının ve artan araç bulunabilirliğinin özellikle orta ticari araç satışları üzerinde baskı oluşturduğunu açıklamaktadır. Kaynak: KAP #1601423

### RAG Top-1 Retrieved Chunk  _(retrieval only — LLM generation yok)_

```
Ford Otosan 1Q’26 Interim Report 
 
 
7. Profitability 
In the first quarter of the year, the following factors led to a contraction in our profitability: 
 
i) 
 a more competitive pricing environment driven by increased vehicle availability, 
ii) 
 changes in the sales mix, 
iii) 
 the appreciation of the EUR/TRY remaining below CPI during the period and 
more limited exchange rate movements compared to the same period of the 
previous year (EUR/TRY ∆: 25% vs. CPI ∆: 31%), 
iv) 
 an increase in the share of export revenues within total revenues. Gross profit declined by 27% year‑on‑year to T
```

**Retrieved sources (top-5):**
- [1] skor=`0.6952` — https://www.kap.org.tr/tr/Bildirim/1601423 — Faaliyet Raporu (Konsolide)
- [2] skor=`0.6786` — https://www.kap.org.tr/tr/Bildirim/1601425 — Geleceğe Dönük Değerlendirmeler
- [3] skor=`0.6778` — https://www.kap.org.tr/tr/Bildirim/1601423 — Faaliyet Raporu (Konsolide)
- [4] skor=`0.6732` — https://www.kap.org.tr/tr/Bildirim/1601423 — Faaliyet Raporu (Konsolide)
- [5] skor=`0.6728` — https://www.kap.org.tr/tr/Bildirim/1558661 — Faaliyet Raporu (Konsolide)

**Gold KAP#:** 1601423 | **Hit KAP#:** 1558661,1601423,1601425

---

## ✗ KAP_RAG_05 · ENKAI · finansal_performans · easy

**Dönem:** 2026Q1  
**Kaynak belge:** ENKAI 1Q2026 Faaliyet Raporu (Konsolide) – KAP #1603547, 08.05.2026  
**Top-1 skor:** 0.6592  |  **KAP match:** ✗  |  **Süre:** 0.057s  
**human_validation_required:** False  

### Soru
> Enka İnşaat'ın 2026 birinci çeyrek aktif büyüklüğü, konsolide satış gelirleri ve ana ortaklık payına düşen net kârı nedir?

### Gold Answer
> 31 Mart 2026 itibarıyla aktif büyüklük 11,42 milyar ABD Doları (507,04 milyar TL). Konsolide satış gelirleri 821,82 milyon ABD Doları (35,83 milyar TL). Ana ortaklık payına düşen net kâr 78,3 milyon ABD Doları (3,41 milyar TL). Kaynak: KAP #1603547

### RAG Top-1 Retrieved Chunk  _(retrieval only — LLM generation yok)_

```
TL dışındaki para birimleri, aksi belirtilmedikçe bin olarak 
belirtilmiştir.) 
4. MÜŞTEREK FAALİYETLER 
 
 Grup’un müşterek faaliyetlerinin aktif ve pasifleri içindeki payı aşağıdaki gibidir: 
 
31 Aralık 31 Aralık
2025 2024
VARLIKLAR
Dönen Varlıklar
Nakit ve nakit benzeri değerler 7.429.701 11.361.774
Finansal yatırımlar 457.763 446.366
Ticari alacaklar 7.358.278 5.738.764
Diğer alacaklar 59.341 35.845
Stoklar 745.344 466.653
Devam eden inşaat,taahhüt veya hizmet sözleşmelerinden varlıklar 833.263 108.416
Diğer dönen varlıklar 1.482.247 980.545
Grup'un müşterek faaliyetlerinin
 dönen varlıkl
```

**Retrieved sources (top-5):**
- [1] skor=`0.6592` — https://www.kap.org.tr/tr/Bildirim/1566104 — Finansal Rapor
- [2] skor=`0.6581` — https://www.kap.org.tr/tr/Bildirim/1603543 — Finansal Rapor
- [3] skor=`0.6574` — https://www.kap.org.tr/tr/Bildirim/1566109 — TSRS Uyumlu Sürdürülebilirlik Raporu
- [4] skor=`0.6574` — https://www.kap.org.tr/tr/Bildirim/1566105 — Faaliyet Raporu (Konsolide)
- [5] skor=`0.6488` — https://www.kap.org.tr/tr/Bildirim/1566105 — Faaliyet Raporu (Konsolide)

**Gold KAP#:** 1603547 | **Hit KAP#:** 1566104,1566105,1566109,1603543

---

## ✗ KAP_RAG_06 · AEFES · temettu · easy

**Dönem:** 2025Y  
**Kaynak belge:** Hak Kullanımı Duyurusu – KAP #1606333, 12.05.2026 | MKK Pay Mali Hak Kullanım – KAP #1608029, 15.05.2026  
**Top-1 skor:** 0.6879  |  **KAP match:** ✗  |  **Süre:** 0.082s  
**human_validation_required:** False  

### Soru
> Anadolu Efes'in 2025 yılı kârından ödenen temettünün pay başına brüt ve net tutarları ile ödeme tarihi nedir?

### Gold Answer
> 1 TL nominal değerli pay başına brüt temettü 0,16975 TL, net temettü ise 0,1442875 TL. Ödeme tarihi 15 Mayıs 2026. Kaynak: KAP #1606333 ve KAP #1608029

### RAG Top-1 Retrieved Chunk  _(retrieval only — LLM generation yok)_

```
Anadolu Efes Biracılık ve Malt Sanayii A.Ş. 2025 Olağan Genel Kurul Bilgilendirme Dokümanı 
 
 
7. Yönetim Kurulu'nun kar dağıtımı ile ilgili teklifinin onaylanması, değiştirilerek 
onaylanması veya reddi 
 
Yönetim Kurulumuzun 5 Mart 2026 tarihli toplantısında, Şirketimizin, 2025 Ocak-Aralık dönemine 
ilişkin olarak çıkarılmış sermayesi 5 .921.052.630 TL üzerinden %33,95 brüt kâr dağıtımını teminen 
her 1 TL nominal bedelli hisseye tam mükellef kurum ile Türkiye’de bir işyeri veya daimi temsilcisi 
aracılığı ile kar payı elde eden dar mükellef kurum niteliğindeki pay sahiplerine net=brüt 0,33
```

**Retrieved sources (top-5):**
- [1] skor=`0.6879` — https://www.kap.org.tr/tr/Bildirim/1573698 — Genel Kurul İşlemlerine İlişkin Bildirim
- [2] skor=`0.6274` — https://www.kap.org.tr/tr/Bildirim/1566777 — Özel Durum Açıklaması (Genel)
- [3] skor=`0.6241` — https://www.kap.org.tr/tr/Bildirim/1592212 — Genel Kurul İşlemlerine İlişkin Bildirim
- [4] skor=`0.6241` — https://www.kap.org.tr/tr/Bildirim/1602713 — Genel Kurul İşlemlerine İlişkin Bildirim
- [5] skor=`0.6218` — https://www.kap.org.tr/tr/Bildirim/1601483 — Faaliyet Raporu (Konsolide)

**Gold KAP#:** 1606333,1608029 | **Hit KAP#:** 1566777,1573698,1592212,1601483,1602713

---

## ✗ KAP_RAG_07 · AEFES · temettu · medium

**Dönem:** 2025Y  
**Kaynak belge:** Hak Kullanımı Duyurusu – KAP #1606333, 12.05.2026  
**Top-1 skor:** 0.5923  |  **KAP match:** ✗  |  **Süre:** 0.055s  
**human_validation_required:** False  

### Soru
> Anadolu Efes 2025 temettüsünde pay başına stopaj kesintisi tutarı nedir ve brüt temettünün yüzde kaçına karşılık gelmektedir?

### Gold Answer
> Brüt temettü 0,16975 TL, net temettü 0,1442875 TL. Pay başı stopaj kesintisi 0,0254625 TL (= 0,16975 − 0,1442875). Bu tutar brüt temettünün yaklaşık yüzde 15'ine karşılık gelmektedir. Kaynak: KAP #1606333

### RAG Top-1 Retrieved Chunk  _(retrieval only — LLM generation yok)_

```
Proforma bazda: TMS 29 etkisi olmadan 2025 yılında, 
Anadolu Efes; 
• Net satış gelirleri %36,4 oranında artarak 234.278,0 milyon TL seviyesinde
• Brüt kar %34,6 oranında artarak 94.094,1 milyon TL, marj ise 55 baz puan azalarak %40,2 seviyesinde
• FAVÖK (BMKÖ) %28,5 oranında artarak 44.473,8 milyon TL, marj 116 baz puan düşüşle %19,0 seviyesinde
• Net kar/(zarar) (KÇFD(*) hariç) 4.914.9 milyon TL seviyesine gerilemiştir. Bira Grubu: 
• Net satış gelirleri %29,7 oranında artarak 52.640,5 milyon TL seviyesinde
• Brüt kar %25,8 oranında artarak 27.316,6 milyon TL, marj ise 161 baz puan azalarak 
```

**Retrieved sources (top-5):**
- [1] skor=`0.5923` — https://www.kap.org.tr/tr/Bildirim/1566777 — Özel Durum Açıklaması (Genel)
- [2] skor=`0.5922` — https://www.kap.org.tr/tr/Bildirim/1601483 — Faaliyet Raporu (Konsolide)
- [3] skor=`0.5885` — https://www.kap.org.tr/tr/Bildirim/1570140 — Faaliyet Raporu (Konsolide)
- [4] skor=`0.5885` — https://www.kap.org.tr/tr/Bildirim/1566777 — Özel Durum Açıklaması (Genel)
- [5] skor=`0.5860` — https://www.kap.org.tr/tr/Bildirim/1601483 — Faaliyet Raporu (Konsolide)

**Gold KAP#:** 1606333 | **Hit KAP#:** 1566777,1570140,1601483

---

## ✓ KAP_RAG_08 · BIMAS · temettu · medium

**Dönem:** 2026Q1  
**Kaynak belge:** BİM 31.03.2026 Konsolide Finansal Tablolar – KAP #1605794, 11.05.2026  
**Top-1 skor:** 0.6423  |  **KAP match:** ✓  |  **Süre:** 0.063s  
**human_validation_required:** True  

### Soru
> BİM Birleşik Mağazalar 2026 birinci çeyreğinde temettü ödemiş midir? Eğer ödemişse tutarı ve hangi nakit akış kalemi altında gösterildiği nedir?

### Gold Answer
> BİM, 2026 birinci çeyreğinde 22.000 bin TL temettü ödemiştir. Bu ödeme finansman faaliyetleri nakit akış tablosunda gösterilmekte olup azınlık hissedarlarına yapılan ödemeyi kapsamaktadır. Kaynak: KAP #1605794

### RAG Top-1 Retrieved Chunk  _(retrieval only — LLM generation yok)_

```
EK: BİM Birleşik Mağazalar A.Ş. 2025 Yılı Kâr Dağıtım Tablosu (TL) 
 1. Ödenmiş Sermaye 600.000.000 
 2. Genel Kanuni Yedek Akçe (Yasal Kayıtlara Göre) 4.996.896.210 
Esas sözleşme uyarınca kâr dağıtımında imtiyaz var ise söz konusu imtiyaza ilişkin bilgi Bulunmamaktadır. SPK’ya Göre Yasal Kayıtlara (YK) Göre 
3. Dönem Kârı 31.592.732.000 29.641.976.076 
4. Ödenecek Vergiler ( - ) 12.857.476.000 7.315.228.299 
5. Net Dönem Kârı ( = ) 18.735.256.000 22.326.747.778 
6. Geçmiş Yıllar Zararları ( - ) - - 
7. Genel Kanuni Yedek Akçe ( - ) - - 
8. NET DAĞITILABİLİR 
18.735.256.000 22.326.747.778 DÖN
```

**Retrieved sources (top-5):**
- [1] skor=`0.6423` — https://www.kap.org.tr/tr/Bildirim/1601470 — Kar Payı Dağıtım İşlemlerine İlişkin Bildirim
- [2] skor=`0.6423` — https://www.kap.org.tr/tr/Bildirim/1587323 — Kar Payı Dağıtım İşlemlerine İlişkin Bildirim
- [3] skor=`0.6397` — https://www.kap.org.tr/tr/Bildirim/1607901 — Kar Payı Dağıtım İşlemlerine İlişkin Bildirim
- [4] skor=`0.6194` — https://www.kap.org.tr/tr/Bildirim/1587322 — Genel Kurul İşlemlerine İlişkin Bildirim
- [5] skor=`0.6116` — https://www.kap.org.tr/tr/Bildirim/1605794 — Finansal Rapor

**Gold KAP#:** 1605794 | **Hit KAP#:** 1587322,1587323,1601470,1605794,1607901

---

## ✗ KAP_RAG_09 · AEFES · temettu · medium

**Dönem:** 2025Y  
**Kaynak belge:** MKK Pay Mali Hak Kullanım İşlemi – KAP #1608029, 15.05.2026  
**Top-1 skor:** 0.5693  |  **KAP match:** ✗  |  **Süre:** 0.08s  
**human_validation_required:** False  

### Soru
> 15 Mayıs 2026 tarihli MKK bildiriminde AEFES dışında hangi şirketlerin temettü ödemesi gerçekleştirilmiştir?

### Gold Answer
> BEYAZ, BRKVY, MCARD, MGROS ve TRCAS için de temettü ödemesi gerçekleştirilmiştir. Kaynak: KAP #1608029

### RAG Top-1 Retrieved Chunk  _(retrieval only — LLM generation yok)_

```
sayfadan ulaşabilirsiniz. Aksi 
belirtilmedikçe, bu duyuruda yer alan tüm finansal veriler TMS 29'a uygun olarak sunulmuştur. AEFES 
Konsolide (milyon TL)
4Ç2024 
Raporlanan
4Ç2024 
Proforma 4Ç2025 Proforma
% Değişim 
2024 
Raporlanan
2024 
Proforma 2025 Proforma
% Değişim 
Satış Hacmi (mhl) 24.2 18.1 18.9 4.6% 123.9 98.3 105.1 7.0%
Satış Gelirleri 53,091.0 39,628.7 47,010.2 18.6% 302,824.5 237,838.0 243,847.1 2.5%
Brüt Kar 20,226.5 14,092.6 18,493.3 31.2% 119,122.1 90,384.2 91,925.9 1.7%
Faaliyet Karı/(Zararı) (BMKÖ) 545.7 -519.9 2,334.7 a.d.
```

**Retrieved sources (top-5):**
- [1] skor=`0.5693` — https://www.kap.org.tr/tr/Bildirim/1566777 — Özel Durum Açıklaması (Genel)
- [2] skor=`0.5454` — https://www.kap.org.tr/tr/Bildirim/1601483 — Faaliyet Raporu (Konsolide)
- [3] skor=`0.5435` — https://www.kap.org.tr/tr/Bildirim/1573698 — Genel Kurul İşlemlerine İlişkin Bildirim
- [4] skor=`0.5386` — https://www.kap.org.tr/tr/Bildirim/1601482 — Finansal Rapor
- [5] skor=`0.5368` — https://www.kap.org.tr/tr/Bildirim/1601482 — Finansal Rapor

**Gold KAP#:** 1608029 | **Hit KAP#:** 1566777,1573698,1601482,1601483

---

## ✗ KAP_RAG_10 · MGROS · temettu · easy

**Dönem:** 2025Y  
**Kaynak belge:** MKK Pay Mali Hak Kullanım İşlemi – KAP #1608029, 15.05.2026  
**Top-1 skor:** 0.6814  |  **KAP match:** ✗  |  **Süre:** 0.057s  
**human_validation_required:** False  

### Soru
> Migros Ticaret'in 2025 yılı kârından ödenen temettünün pay başına brüt ve net tutarları ile ödeme tarihi nedir?

### Gold Answer
> 1 TL nominal değerli pay başına brüt temettü 4,5566457 TL, net temettü ise 3,8731488 TL. Ödeme tarihi 15 Mayıs 2026. Kaynak: KAP #1608029

### RAG Top-1 Retrieved Chunk  _(retrieval only — LLM generation yok)_

```
Şirket, 15 Nisan 2025 tarihli 2024 yılı olağan Genel Kurul toplantısında, dağıtılması öngörülen diğer 
kaynaklardan, Kasım 2024’te dağıtılan 676 milyon TL kar payı avansının mahsup edilerek, tam 
mükellef kurumlar ile Türkiye'de bir işyeri veya daimi temsilc i aracılığı ile kar payı elde eden dar 
mükellef kurum ortaklarına; 1,00 TL nominal değerli pay için %690,40087 oranında ve 6,9040087 TL 
brüt=net nakit kar payı ödenmesine, diğer hissedarlara 1,00 TL nominal değerli hisse için %690,40087 
oranında ve 6,9040087 TL brüt; %586,84074 oranında ve 5,8684074 TL net nakit kar payı ödenmesine 
ili
```

**Retrieved sources (top-5):**
- [1] skor=`0.6814` — https://www.kap.org.tr/tr/Bildirim/1566129 — Finansal Rapor
- [2] skor=`0.6767` — https://www.kap.org.tr/tr/Bildirim/1571174 — Faaliyet Raporu (Konsolide)
- [3] skor=`0.6654` — https://www.kap.org.tr/tr/Bildirim/1571174 — Faaliyet Raporu (Konsolide)
- [4] skor=`0.6636` — https://www.kap.org.tr/tr/Bildirim/1571174 — Faaliyet Raporu (Konsolide)
- [5] skor=`0.6526` — https://www.kap.org.tr/tr/Bildirim/1574285 — Kar Payı Dağıtım İşlemlerine İlişkin Bildirim

**Gold KAP#:** 1608029 | **Hit KAP#:** 1566129,1571174,1574285

---

## ✗ KAP_RAG_11 · YKBNK · banka_kredi_buyumesi · easy

**Dönem:** 2026Q1  
**Kaynak belge:** YKBNK NPL Portföy Satışı ODA Bildirimi – KAP #1603672, 08.05.2026  
**Top-1 skor:** 0.6159  |  **KAP match:** ✗  |  **Süre:** 0.058s  
**human_validation_required:** False  

### Soru
> Yapı Kredi Bankası'nın Mayıs 2026'da ihaleyle devrettiği NPL portföyünün anapara tutarı, portföy türü ve devralıcı şirket nedir?

### Gold Answer
> 517 milyon TL anapara değerindeki bireysel ve KOBİ nitelikli alacak portföyü, Arsan Varlık Yönetimi A.Ş. tarafından ihaleyle satın alınmıştır. Kaynak: KAP ODA #1603672

### RAG Top-1 Retrieved Chunk  _(retrieval only — LLM generation yok)_

```
Hayır (No)
Konuya İlişkin Daha Önce Yapılan Açıklamanın Tarihi 12.02.2026
Yapılan Açıklama Ertelenmiş Bir Açıklama mı? Hayır (No)
Bildirim İçeriği
Açıklamalar
12.02.2026  tarihinde yapmış olduğumuz Özel Durum Açıklamamızda,
Şirketimizin Yapı ve Kredi Bankası A.Ş.'nin gerçekleştirdiği tahsili gecikmiş alacak satışında, satışa çıkarılan   243,8 milyon 
 TL anaparaya sahip 1 bireysel nitelikli ve 280,6 milyon TL anaparaya sahip 1 KOBİ karma nitelikli portföylerin ihalesini
kazandığı duyurulmuştu. Anaparası, toplam  524,4 milyon TL olan ihaleye konu alacakların devir işlemleri ve sözleşmenin imza 
```

**Retrieved sources (top-5):**
- [1] skor=`0.6159` — https://www.kap.org.tr/tr/Bildirim/1561009 — Özel Durum Açıklaması (Genel)
- [2] skor=`0.5895` — https://www.kap.org.tr/tr/Bildirim/1603521 — Özel Durum Açıklaması (Genel)
- [3] skor=`0.5889` — https://www.kap.org.tr/tr/Bildirim/1558609 — Entegre Rapor
- [4] skor=`0.5889` — https://www.kap.org.tr/tr/Bildirim/1558607 — Faaliyet Raporu (Konsolide)
- [5] skor=`0.5813` — https://www.kap.org.tr/tr/Bildirim/1603528 — Özel Durum Açıklaması (Genel)

**Gold KAP#:** 1603672 | **Hit KAP#:** 1558607,1558609,1561009,1603521,1603528

---

## ✓ KAP_RAG_12 · ISCTR · banka_kredi_buyumesi · medium

**Dönem:** 2026Q1  
**Kaynak belge:** ISCTR 1Q2026 Banka Finansal Raporu (Konsolide) – KAP #1601308, 05.05.2026  
**Top-1 skor:** 0.7569  |  **KAP match:** ✓  |  **Süre:** 0.076s  
**human_validation_required:** False  

### Soru
> Türkiye İş Bankası'nın 31 Mart 2026 itibarıyla konsolide nakit ve nakit benzerleri toplamı ile 31 Aralık 2025'e göre değişimi nedir?

### Gold Answer
> 31.03.2026: TP 382.108.811 bin TL + YP 791.082.957 bin TL = Toplam 1.173.191.768 bin TL. 31.12.2025: TP 394.840.534 bin TL + YP 681.395.081 bin TL = Toplam 1.076.235.615 bin TL. Dönemsel artış yaklaşık 96,9 milyar TL. Kaynak: KAP #1601308

### RAG Top-1 Retrieved Chunk  _(retrieval only — LLM generation yok)_

```
31 Aralık 2025 Tarihli Konsolide Olmayan Finansal Rapor
Türkiye İş Bankası A.Ş. Dönem başındaki nakit ve nakde eşdeğer varlıklar:
31.12.2024 31.12.2023
Nakit 319.796.000 325.002.285
Kasa ve Efektif Deposu 35.294.459 30.724.839
T .C. Merkez Bankası ve Diğer 284.501.541 294.277.446
Nakde Eşdeğer Varlıklar 35.233.322 34.862.415
Vadesiz ve 3 Aya Kadar Vadeli Bankalar 35.233.322 34.862.415
Para Piyasalarından Alacaklar 
Toplam Nakit ve Nakde Eşdeğer Varlık 355.029.322 359.864.700
31.12.2025 31.12.2024
Nakit 390.946.740 319.796.000
Kasa ve Efektif Deposu 47.583.998 35.294.459
T .C.
```

**Retrieved sources (top-5):**
- [1] skor=`0.7569` — https://www.kap.org.tr/tr/Bildirim/1569176 — Faaliyet Raporu (Konsolide)
- [2] skor=`0.7250` — https://www.kap.org.tr/tr/Bildirim/1569176 — Faaliyet Raporu (Konsolide)
- [3] skor=`0.7201` — https://www.kap.org.tr/tr/Bildirim/1601308 — Finansal Rapor
- [4] skor=`0.7094` — https://www.kap.org.tr/tr/Bildirim/1569176 — Faaliyet Raporu (Konsolide)
- [5] skor=`0.7088` — https://www.kap.org.tr/tr/Bildirim/1601308 — Finansal Rapor

**Gold KAP#:** 1601308 | **Hit KAP#:** 1569176,1601308

---

## ✓ KAP_RAG_13 · AKBNK · banka_kredi_buyumesi · medium

**Dönem:** 2026Q2  
**Kaynak belge:** AKBNK Sermaye Benzeri Tahvil Bildirimi – KAP #1608065, 15.05.2026  
**Top-1 skor:** 0.6115  |  **KAP match:** ✓  |  **Süre:** 0.055s  
**human_validation_required:** False  

### Soru
> Akbank'ın Mayıs 2026'da erken itfa ettiği sermaye benzeri tahvilin başlangıç tutarı, ISIN kodu ve erken itfa yetkisi kimden alınmıştır?

### Gold Answer
> 2021 yılında ihraç edilen toplam 500 milyon ABD Doları tutarındaki sürdürülebilir sermaye benzeri tahvil (ISIN: XS2355183091 ve US00971YAJ91). 10 yıl vadeli, 5. yılda erken itfa opsiyonlu. Erken itfa için BDDK onayı alınmıştır. Kaynak: KAP #1608065

### RAG Top-1 Retrieved Chunk  _(retrieval only — LLM generation yok)_

```
AKBANK T.A.Ş. Pay Dışında Sermaye Piyasası Aracı İşlemlerine İlişkin 
Bildirim (Faiz İçeren)
KAMUYU AYDINLATMA PLATFORMU
KAP'ta yayınlanma tarihi ve saati: 15.05.2026 17:50:17
https://www.kap.org.tr/tr/Bildirim/1608066

Özet Bilgi
XS2355183091 ve US00971YAJ91 ISIN kodlu Sürdürülebilir Sermaye Benzeri Tahvillerin erken itfa opsiyonunun kullanılması 
hakkında
Yapılan Açıklama Güncelleme mi ? Hayır
Yapılan Açıklama Düzeltme mi ? Evet
Yapılan Açıklama Ertelenmiş Bir 
Açıklama mı ?
```

**Retrieved sources (top-5):**
- [1] skor=`0.6115` — https://www.kap.org.tr/tr/Bildirim/1608066 — Pay Dışında Sermaye Piyasası Aracı İşlemlerine İlişkin Bildi
- [2] skor=`0.6087` — https://www.kap.org.tr/tr/Bildirim/1608065 — Pay Dışında Sermaye Piyasası Aracı İşlemlerine İlişkin Bildi
- [3] skor=`0.5840` — https://www.kap.org.tr/tr/Bildirim/1602709 — Pay Dışında Sermaye Piyasası Aracı İşlemlerine İlişkin Bildi
- [4] skor=`0.5831` — https://www.kap.org.tr/tr/Bildirim/1598264 — Finansal Rapor
- [5] skor=`0.5822` — https://www.kap.org.tr/tr/Bildirim/1598259 — Finansal Rapor

**Gold KAP#:** 1608065 | **Hit KAP#:** 1598259,1598264,1602709,1608065,1608066

---

## ✓ KAP_RAG_14 · AKBNK · banka_kredi_buyumesi · medium

**Dönem:** 2025Y  
**Kaynak belge:** AKBNK 2025 Entegre Faaliyet Raporu – KAP #1564365, 02.03.2026  
**Top-1 skor:** 0.6965  |  **KAP match:** ✓  |  **Süre:** 0.055s  
**human_validation_required:** False  

### Soru
> Bankacılık sektöründe sorunlu kredi (TGA) oranı 2024 yıl sonu ile 2025 Aralık sonu arasında nasıl değişmiştir?

### Gold Answer
> Sektör TGA oranı 2024 sonundaki yüzde 1,8'den Aralık 2025 sonunda yüzde 2,5'e yükselmekle birlikte düşük seyrini sürdürmüştür. Kaynak: KAP #1564365

### RAG Top-1 Retrieved Chunk  _(retrieval only — LLM generation yok)_

```
Sektörde sorunlu kredi oranı 2024 sonunda %1,8 
iken aralık ayı itibarıyla %2,5’e yükselmekle birlikte 
düşük seyrini sürdürdü. Aktif kalitesinde tabana 
yaygın bir bozulma gözlenmemekle birlikte sektörel 
bazda bazı ayrışmalar gözlenmiştir. Bankacılık sektörü 2026 yılına yurt içi ve yurt 
dışına ilişkin belirsizliklerle girmektedir. Ancak, 
bankalar ihtiyatlı karşılık politikalarıyla bu riskleri 
yönetebilecek kapasiteye sahiptir. Belirsizliklerin 
hızlı şekilde giderilmesi ve risklerin azalması 
sektör açısından önem taşımaktadır.
```

**Retrieved sources (top-5):**
- [1] skor=`0.6965` — https://www.kap.org.tr/tr/Bildirim/1564365 — Faaliyet Raporu (Konsolide)
- [2] skor=`0.6567` — https://www.kap.org.tr/tr/Bildirim/1564365 — Faaliyet Raporu (Konsolide)
- [3] skor=`0.6380` — https://www.kap.org.tr/tr/Bildirim/1602720 — TSRS Uyumlu Sürdürülebilirlik Raporu
- [4] skor=`0.6302` — https://www.kap.org.tr/tr/Bildirim/1602720 — TSRS Uyumlu Sürdürülebilirlik Raporu
- [5] skor=`0.6060` — https://www.kap.org.tr/tr/Bildirim/1602720 — TSRS Uyumlu Sürdürülebilirlik Raporu

**Gold KAP#:** 1564365 | **Hit KAP#:** 1564365,1602720

---

## ✓ KAP_RAG_15 · VAKBN · banka_kredi_buyumesi · easy

**Dönem:** 2026Q2  
**Kaynak belge:** VAKBN Sendikasyon Kredisi ODA Bildirimi – KAP #1608322, 18.05.2026  
**Top-1 skor:** 0.6666  |  **KAP match:** ✓  |  **Süre:** 0.055s  
**human_validation_required:** False  

### Soru
> VakıfBank'ın Mayıs 2026'da sağladığı sendikasyon kredisinin toplam tutarı, para birimi bileşimi ve vadesi nedir?

### Gold Answer
> Toplam 1,2 milyar ABD Doları karşılığı; 484 milyon ABD Doları ve 574 milyon Euro olmak üzere iki dilimden oluşmaktadır. Vade 367 gündür. USD dilimi maliyeti SOFR + yüzde 1,25; Euro dilimi Euribor + yüzde 1,10. Kaynak: KAP ODA #1608322

### RAG Top-1 Retrieved Chunk  _(retrieval only — LLM generation yok)_

```
31 Aralık 2025 tarihi itibarıyla toplam seküritizasyon kredisi bakiyesi 2,677 milyon ABD Doları ve 847,750 
milyon AVRO eşdeğerindedir (31 Aralık 2024: 2,051 milyon ABD Doları ve 528,7 milyon AVRO). VakıfBank 2025 Entegre Faaliyet Raporu
(Tutarlar aksi belirtilmedikçe Bin Türk Lirası (“TL”) olarak ifade edilmiştir.)
TÜRKİYE VAKIFLAR BANKASI TÜRK ANONİM ORTAKLIĞI
31 ARALIK 2025 TARİHİ İTİBARIYLA HAZIRLANAN KONSOLİDE OLMAYAN FİNANSAL
TABLOLARA İLİŞKİN AÇIKLAMA VE DİPNOTLAR
TÜRKİYE VAKIFLAR BANKASI TÜRK ANONİM ORTAKLIĞI 
 
31 ARALIK 2025 TARİHİ İTİBARIYLA HAZIRLANAN KONSOLİDE OLMAYAN 
FİNANSAL TA
```

**Retrieved sources (top-5):**
- [1] skor=`0.6666` — https://www.kap.org.tr/tr/Bildirim/1565260 — Faaliyet Raporu (Konsolide)
- [2] skor=`0.6501` — https://www.kap.org.tr/tr/Bildirim/1565260 — Faaliyet Raporu (Konsolide)
- [3] skor=`0.6495` — https://www.kap.org.tr/tr/Bildirim/1608322 — Özel Durum Açıklaması (Genel)
- [4] skor=`0.6488` — https://www.kap.org.tr/tr/Bildirim/1565260 — Faaliyet Raporu (Konsolide)
- [5] skor=`0.6256` — https://www.kap.org.tr/tr/Bildirim/1602078 — Finansal Rapor

**Gold KAP#:** 1608322 | **Hit KAP#:** 1565260,1602078,1608322

---

## ✓ KAP_RAG_16 · AEFES · genel_finansal_durum · medium

**Dönem:** 2025Y  
**Kaynak belge:** AEFES 2025 Yıllık Faaliyet Raporu – KAP #1570140, 11.03.2026  
**Top-1 skor:** 0.6861  |  **KAP match:** ✓  |  **Süre:** 0.079s  
**human_validation_required:** False  

### Soru
> Anadolu Efes'in 2025 yıl sonu toplam varlıkları, ana ortaklığa ait özkaynakları ve toplam finansal borcu nedir?

### Gold Answer
> Toplam Varlıklar: 413.578 milyon TL (2024: 461.029 milyon TL; yüzde 10,3 azalma). Ana Ortaklığa ait Özkaynaklar: 108.611 milyon TL (2024: 110.003 milyon TL; yüzde 1,3 azalma). Toplam Finansal Borç (kiralama dahil): 92.987 milyon TL (2024: 103.258 milyon TL; yüzde 9,9 azalma). Kaynak: KAP #1570140

### RAG Top-1 Retrieved Chunk  _(retrieval only — LLM generation yok)_

```
10. Bağış ve Yardımlar, Sosyal 
Sorumluluk Projeleri Çerçevesinde 
Yapılan Harcamalar ve Yönetim 
Kurulu Üyeleri ile Üst Düzey 
Yöneticilere Sağlanan Haklara 
İlişkin Bilgiler
Anadolu Efes’in 2025 yılı toplam bağış rakamı 
91,2 milyon TL’dir. Yönetim Kurulu üyeleri ve üst düzey yöneticilere 
sağlanan huzur hakkı, ücret, prim, ikramiye, kâr 
payı gibi mali menfaatlerin toplam tutarları, mali 
tabloların ilgili dipnotlarında verilirken verilen 
ödenekler, yolculuk, konaklama ve temsil giderleri 
ve ayni ve nakdi imkânlar, sigortalar ve benzeri 
teminatların toplam tutarı 2025 yılında 1.625,7 bin
```

**Retrieved sources (top-5):**
- [1] skor=`0.6861` — https://www.kap.org.tr/tr/Bildirim/1570140 — Faaliyet Raporu (Konsolide)
- [2] skor=`0.6598` — https://www.kap.org.tr/tr/Bildirim/1570140 — Faaliyet Raporu (Konsolide)
- [3] skor=`0.6528` — https://www.kap.org.tr/tr/Bildirim/1601483 — Faaliyet Raporu (Konsolide)
- [4] skor=`0.6510` — https://www.kap.org.tr/tr/Bildirim/1566776 — Finansal Rapor
- [5] skor=`0.6501` — https://www.kap.org.tr/tr/Bildirim/1570140 — Faaliyet Raporu (Konsolide)

**Gold KAP#:** 1570140 | **Hit KAP#:** 1566776,1570140,1601483

---

## ✓ KAP_RAG_17 · AKBNK · genel_finansal_durum · easy

**Dönem:** 2025Y  
**Kaynak belge:** AKBNK 2025 Entegre Faaliyet Raporu – KAP #1564365, 02.03.2026  
**Top-1 skor:** 0.7498  |  **KAP match:** ✓  |  **Süre:** 0.056s  
**human_validation_required:** False  

### Soru
> TCMB, 2025 Temmuz'dan itibaren politika faizinde kaç toplantıda toplam kaç baz puan indirim gerçekleştirmiştir ve mevcut politika faizi nedir?

### Gold Answer
> TCMB Temmuz 2025'ten itibaren 5 toplantıda toplam 900 baz puan faiz indirimi gerçekleştirmiştir; politika faizi yüzde 37,0'ye çekilmiştir. Gecelik borç verme faizi yüzde 40,0, borç alma faizi yüzde 35,5. Kaynak: KAP #1564365

### RAG Top-1 Retrieved Chunk  _(retrieval only — LLM generation yok)_

```
TCMB temmuz ayı ile birlikte 
yeniden faiz indirim sürecine girmiş, beş toplantıda 
politika faizi 900 bp azalarak %37’ye gerilemiştir. Enflasyondaki katılık nedeniyle 2026 yılında bu 
sürecin ölçülü adımlarla, kademeli gerçekleşmesi 
beklenmektedir. 28 Akbank Entegre Faaliyet Raporu 2025
Bankacılık Sektörü
2025 yılı ikinci çeyreğinde yurt içi ve yurt dışı 
gelişmeler kaynaklı finansal koşullar sıkılaşırken, 
alınan tedbirler makro-finansal risklerin sınırlanmasını 
sağladı. Bu durum bankacılık sektöründe fonlama 
maliyetlerini artırırken, karlılık ve varlık kalitesi 
açısından şartların zorla
```

**Retrieved sources (top-5):**
- [1] skor=`0.7498` — https://www.kap.org.tr/tr/Bildirim/1564365 — Faaliyet Raporu (Konsolide)
- [2] skor=`0.7397` — https://www.kap.org.tr/tr/Bildirim/1564365 — Faaliyet Raporu (Konsolide)
- [3] skor=`0.7338` — https://www.kap.org.tr/tr/Bildirim/1564365 — Faaliyet Raporu (Konsolide)
- [4] skor=`0.6218` — https://www.kap.org.tr/tr/Bildirim/1564365 — Faaliyet Raporu (Konsolide)
- [5] skor=`0.6172` — https://www.kap.org.tr/tr/Bildirim/1564365 — Faaliyet Raporu (Konsolide)

**Gold KAP#:** 1564365 | **Hit KAP#:** 1564365

---

## ✓ KAP_RAG_18 · AKBNK · genel_finansal_durum · hard

**Dönem:** 2025Y  
**Kaynak belge:** AKBNK 2025 Entegre Faaliyet Raporu – KAP #1564365, 02.03.2026  
**Top-1 skor:** 0.6828  |  **KAP match:** ✓  |  **Süre:** 0.062s  
**human_validation_required:** False  

### Soru
> Türkiye'de kur korumalı mevduatın (KKM) bakiyesi 23 Ocak 2026 itibarıyla ne düzeydedir ve döviz tevdiat hesabı (DTH) bakiyesi 2025 yılında nasıl değişmiştir?

### Gold Answer
> KKM bakiyesi 23 Ocak 2026 itibarıyla 0,1 milyar ABD Dolarına gerilemiştir. DTH bakiyesi 18 Mart 2025'ten 2025 sonuna kadar yaklaşık 44 milyar ABD Doları artarak 249 milyar ABD Dolarına yükselmiştir. Altın ve parite etkisi hariç artış yaklaşık 14 milyar ABD Doları düzeyindedir. Kaynak: KAP #1564365

### RAG Top-1 Retrieved Chunk  _(retrieval only — LLM generation yok)_

```
Sermaye yeterlilik oranı (SYR) aralıkta %19,7 ile 
yasal sınırın üstünde kalmaya devam etmiştir. Çekirdek SYR de %15,1 ile güçlü seyretmektedir. TCMB’nin sadeleşme adımlarına kapsamında kur 
korumalı mevduat (KKM) ilişkin tüm işlemlerin 
sonlandırılmasına yönelik kararın ardından, KKM 
bakiyesi 23 Ocak itibarıyla 0,1 milyar ABD Doları’na 
gerilemiştir. DTH 18 Mart’tan 2025 sonuna kadar 
olan dönemde yaklaşık 44 milyar ABD Doları 
artışla 249 milyar ABD Doları’na yükselirken, bu 
artışta özellikle altın fiyatlarında görülen artış 
etkili olmuştur. Altın fiyatı ve parite etkisi hariç 
baktığımız
```

**Retrieved sources (top-5):**
- [1] skor=`0.6828` — https://www.kap.org.tr/tr/Bildirim/1564365 — Faaliyet Raporu (Konsolide)
- [2] skor=`0.6629` — https://www.kap.org.tr/tr/Bildirim/1564365 — Faaliyet Raporu (Konsolide)
- [3] skor=`0.6624` — https://www.kap.org.tr/tr/Bildirim/1564365 — Faaliyet Raporu (Konsolide)
- [4] skor=`0.6560` — https://www.kap.org.tr/tr/Bildirim/1564365 — Faaliyet Raporu (Konsolide)
- [5] skor=`0.6495` — https://www.kap.org.tr/tr/Bildirim/1564365 — Faaliyet Raporu (Konsolide)

**Gold KAP#:** 1564365 | **Hit KAP#:** 1564365

---

## ✓ KAP_RAG_19 · BIMAS · genel_finansal_durum · medium

**Dönem:** 2026Q1  
**Kaynak belge:** BİM 31.03.2026 Konsolide Finansal Tablolar – KAP #1605794, 11.05.2026  
**Top-1 skor:** 0.6779  |  **KAP match:** ✓  |  **Süre:** 0.086s  
**human_validation_required:** False  

### Soru
> BİM'in 31 Mart 2026 itibarıyla bilanço nakit ve nakit benzerleri ile finansal yatırımlar toplamı, 31 Aralık 2025 ile karşılaştırıldığında nasıl değişmiştir?

### Gold Answer
> 31.03.2026: Nakit 4.980.275 bin TL + Finansal Yatırımlar 24.977.581 bin TL = Toplam 29.957.856 bin TL. 31.12.2025: Nakit 3.808.085 bin TL + Finansal Yatırımlar 11.764.683 bin TL = Toplam 15.572.768 bin TL. Artış yaklaşık 14,4 milyar TL. Kaynak: KAP #1605794

### RAG Top-1 Retrieved Chunk  _(retrieval only — LLM generation yok)_

```
BIST100 Endeksi’nin performansı
BİM’in performansı
**BİM hisse performans değişimleri düzeltilmiş hisse değerleri baz alınarak hesaplanmıştır. Nakit Kâr Payı Grafiği*
BİM ve BIST 100’ün Hisse Performansı Karşılaştırması**
Dağıtılan Kâr Payı (Bin TL) Kâr Payı Verimi (%)
2025
2023 2024 2025
2025
7.800.000
%125 %79
%3
2,4
2024
2023 2024 2025
20242023 20232022 2022
6.072.000
%36 %32
%15
2,03.036.000
2,23.643.200
2,9
En Kıymetli Anlayış: Kurumsal Yönetim134
BİM 2025 Entegre Faaliyet Raporu

BİM Birleşik Mağazalar A.Ş., tüm faaliyetlerini, maruz kaldığı riskleri ve bunlardan korunma yöntemlerini de 
```

**Retrieved sources (top-5):**
- [1] skor=`0.6779` — https://www.kap.org.tr/tr/Bildirim/1570151 — Faaliyet Raporu (Konsolide)
- [2] skor=`0.6711` — https://www.kap.org.tr/tr/Bildirim/1605794 — Finansal Rapor
- [3] skor=`0.6592` — https://www.kap.org.tr/tr/Bildirim/1570150 — Finansal Rapor
- [4] skor=`0.6570` — https://www.kap.org.tr/tr/Bildirim/1605794 — Finansal Rapor
- [5] skor=`0.6563` — https://www.kap.org.tr/tr/Bildirim/1605794 — Finansal Rapor

**Gold KAP#:** 1605794 | **Hit KAP#:** 1570150,1570151,1605794

---

## ✗ KAP_RAG_20 · ENKAI · genel_finansal_durum · medium

**Dönem:** 2026Q1  
**Kaynak belge:** ENKAI 1Q2026 Faaliyet Raporu (Konsolide) – KAP #1603547, 08.05.2026  
**Top-1 skor:** 0.6879  |  **KAP match:** ✗  |  **Süre:** 0.062s  
**human_validation_required:** False  

### Soru
> Enka İnşaat'ın 2026 birinci çeyrek toplam finansal borcu ve net nakit pozisyonu nedir?

### Gold Answer
> Kısa ve uzun vadeli finansal borçlar toplamı 156,87 milyon ABD Doları (6,96 milyar TL). Nakit ve benzerleri ile kısa ve uzun vadeli finansal yatırımlar toplamı 5,47 milyar ABD Doları (243 milyar TL). Net nakit pozisyonu 5,32 milyar ABD Doları (236 milyar TL). Kaynak: KAP #1603547

### RAG Top-1 Retrieved Chunk  _(retrieval only — LLM generation yok)_

```
TL dışındaki para birimleri, aksi belirtilmedikçe bin olarak 
belirtilmiştir.) 
4. MÜŞTEREK FAALİYETLER 
 
 Grup’un müşterek faaliyetlerinin aktif ve pasifleri içindeki payı aşağıdaki gibidir: 
 
31 Aralık 31 Aralık
2025 2024
VARLIKLAR
Dönen Varlıklar
Nakit ve nakit benzeri değerler 7.429.701 11.361.774
Finansal yatırımlar 457.763 446.366
Ticari alacaklar 7.358.278 5.738.764
Diğer alacaklar 59.341 35.845
Stoklar 745.344 466.653
Devam eden inşaat,taahhüt veya hizmet sözleşmelerinden varlıklar 833.263 108.416
Diğer dönen varlıklar 1.482.247 980.545
Grup'un müşterek faaliyetlerinin
 dönen varlıkl
```

**Retrieved sources (top-5):**
- [1] skor=`0.6879` — https://www.kap.org.tr/tr/Bildirim/1566104 — Finansal Rapor
- [2] skor=`0.6811` — https://www.kap.org.tr/tr/Bildirim/1566105 — Faaliyet Raporu (Konsolide)
- [3] skor=`0.6806` — https://www.kap.org.tr/tr/Bildirim/1566105 — Faaliyet Raporu (Konsolide)
- [4] skor=`0.6609` — https://www.kap.org.tr/tr/Bildirim/1566105 — Faaliyet Raporu (Konsolide)
- [5] skor=`0.6567` — https://www.kap.org.tr/tr/Bildirim/1566104 — Finansal Rapor

**Gold KAP#:** 1603547 | **Hit KAP#:** 1566104,1566105

---
