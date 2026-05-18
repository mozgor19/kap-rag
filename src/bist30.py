BIST30_TICKERS: list[str] = [
    "AKBNK",   # Akbank
    "AKSEN",   # Aksa Enerji
    "ALARK",   # Alarko Holding
    "ASELS",   # Aselsan
    "ASTOR",   # Astor Enerji
    "BIMAS",   # BİM Mağazalar
    "DOAS",    # Doğuş Otomotiv
    "EKGYO",   # Emlak Konut GYO
    "ENKAI",   # Enka İnşaat
    "EREGL",   # Ereğli Demir Çelik
    "FROTO",   # Ford Otosan
    "GARAN",   # Garanti BBVA
    "HEKTS",   # Hektaş
    "ISCTR",   # İş Bankası C
    "KCHOL",   # Koç Holding
    "KOZAL",   # Koza Altın
    "KRDMD",   # Kardemir D
    "MGROS",   # Migros
    "OYAKC",   # Oyak Çimento
    "PETKM",   # Petkim
    "PGSUS",   # Pegasus
    "SAHOL",   # Sabancı Holding
    "SASA",    # Sasa Polyester
    "SISE",    # Şişe Cam
    "TCELL",   # Turkcell
    "THYAO",   # Türk Hava Yolları
    "TOASO",   # Tofaş
    "TUPRS",   # Tüpraş
    "YKBNK",   # Yapı Kredi
    "ZRGYO",   # Ziraat GYO
]

if __name__ == "__main__":
    print(f"Toplam {len(BIST30_TICKERS)} hisse:")
    for t in BIST30_TICKERS:
        print(f"  - {t}")
