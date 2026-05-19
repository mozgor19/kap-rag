BIST30_TICKERS: list[str] = [
    "AEFES",   # Anadolu Efes
    "AKBNK",   # Akbank
    "ASELS",   # Aselsan
    "ASTOR",   # Astor Enerji
    "BIMAS",   # BİM Mağazalar
    "CIMSA",   # Çimsa
    "DSTKF",   # Destek Finans Faktoring
    "EKGYO",   # Emlak Konut GYO
    "ENKAI",   # Enka İnşaat
    "EREGL",   # Ereğli Demir Çelik
    "FROTO",   # Ford Otosan
    "GARAN",   # Garanti BBVA
    "GUBRF",   # Gübre Fabrikaları
    "ISCTR",   # İş Bankası C
    "KCHOL",   # Koç Holding
    "KRDMD",   # Kardemir D
    "MGROS",   # Migros
    "PETKM",   # Petkim
    "PGSUS",   # Pegasus
    "SAHOL",   # Sabancı Holding
    "SASA",    # Sasa Polyester
    "SISE",    # Şişe Cam
    "TAVHL",   # TAV Havalimanları
    "TCELL",   # Turkcell
    "THYAO",   # Türk Hava Yolları
    "TOASO",   # Tofaş
    "TRALT",   # Türk Altın İşletmeleri
    "TTKOM",   # Türk Telekom
    "TUPRS",   # Tüpraş
    "VAKBN",   # Vakıflar Bankası
]

if __name__ == "__main__":
    print(f"Toplam {len(BIST30_TICKERS)} hisse:")
    for t in BIST30_TICKERS:
        print(f"  - {t}")
