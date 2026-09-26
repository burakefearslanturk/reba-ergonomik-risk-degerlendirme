"""
İş İstasyonu Senaryoları — REBA Toplu Değerlendirme
======================================================
Bir üretim tesisindeki 6 farklı iş istasyonunda gözlemlenen duruşları
tanımlar ve her biri için REBA skorunu hesaplar. Ayrıca en riskli
istasyon için "iyileştirme sonrası" (improved) senaryo ile karşılaştırma
sunar.
"""

from reba_skorlama import Durus, reba_hesapla, sonucu_yazdir, RebaSonucu


def senaryolari_olustur() -> list[Durus]:
    return [
        Durus(
            isci_adi="Ahmet Yılmaz", istasyon="1. Kalite Kontrol Masası (Oturarak)",
            govde_aci=15, boyun_aci=25, boyun_burkulmus=False,
            ust_kol_aci=15, alt_kol_aci=90, bilek_aci=10,
            bacak_bilateral=True, yuk_kg=0.5, kavrama="iyi",
        ),
        Durus(
            isci_adi="Elif Kara", istasyon="2. Kaynak İstasyonu (Ayakta, Eğilerek)",
            govde_aci=55, govde_burkulmus=True, boyun_aci=30,
            ust_kol_aci=80, omuz_kalkik=True, alt_kol_aci=100,
            bilek_aci=25, bilek_orta_hattan_sapmis=True,
            bacak_bilateral=False, diz_flexion_aci=40,
            yuk_kg=3, kavrama="orta", statik_durus=True,
        ),
        Durus(
            isci_adi="Mehmet Demir", istasyon="3. Manuel Malzeme Taşıma (Kaldırma)",
            govde_aci=70, govde_burkulmus=True, boyun_aci=35,
            ust_kol_aci=60, kol_abduksiyon=True, alt_kol_aci=115,
            bilek_aci=30, bilek_burkulmus=True,
            bacak_bilateral=False, diz_flexion_aci=65,
            yuk_kg=22, ani_kuvvet=True, kavrama="kotu",
            statik_durus=False, tekrarli_hareket=True,
        ),
        Durus(
            isci_adi="Zeynep Aydın", istasyon="4. Montaj Hattı (Ayakta, Hafif İş)",
            govde_aci=10, boyun_aci=15,
            ust_kol_aci=25, alt_kol_aci=95, bilek_aci=12,
            bacak_bilateral=True, yuk_kg=1.5, kavrama="iyi",
            tekrarli_hareket=True,
        ),
        Durus(
            isci_adi="Can Öztürk", istasyon="5. Forklift Operatörü (Oturarak, Dönerek)",
            govde_aci=20, govde_burkulmus=True, boyun_aci=40,
            boyun_burkulmus=True, ust_kol_aci=30, alt_kol_aci=85,
            bilek_aci=15, bacak_bilateral=True, yuk_kg=0,
            kavrama="iyi", statik_durus=True,
        ),
        Durus(
            isci_adi="Ayşe Şahin", istasyon="6. Bilgisayar Destekli Tasarım (Ofis)",
            govde_aci=5, boyun_aci=20, ust_kol_aci=18,
            alt_kol_aci=95, bilek_aci=18, bilek_orta_hattan_sapmis=True,
            bacak_bilateral=True, yuk_kg=0, kavrama="iyi",
            statik_durus=True, tekrarli_hareket=True,
        ),
    ]


def iyilestirme_senaryosu() -> Durus:
    """
    En riskli istasyon (3. Manuel Malzeme Taşıma) için önerilen
    iyileştirmeler uygulanmış hali: yükseklik ayarlı platform (gövde
    eğilmesi azaltılır), takım/kanca kullanımı (kavrama iyileştirilir),
    yük ikiye bölünür, mekanik yardım (ani kuvvet ortadan kalkar).
    """
    return Durus(
        isci_adi="Mehmet Demir (İyileştirilmiş)",
        istasyon="3. Manuel Malzeme Taşıma (İYİLEŞTİRİLMİŞ)",
        govde_aci=20, govde_burkulmus=False, boyun_aci=15,
        ust_kol_aci=30, alt_kol_aci=95, bilek_aci=10,
        bacak_bilateral=True, yuk_kg=11, ani_kuvvet=False,
        kavrama="iyi", statik_durus=False, tekrarli_hareket=True,
    )


def toplu_degerlendir(senaryolar: list[Durus]) -> list[RebaSonucu]:
    return [reba_hesapla(d) for d in senaryolar]


if __name__ == "__main__":
    senaryolar = senaryolari_olustur()
    sonuclar = toplu_degerlendir(senaryolar)

    print("=" * 60)
    print("REBA TOPLU DEĞERLENDİRME — 6 İŞ İSTASYONU")
    print("=" * 60)

    for s in sonuclar:
        sonucu_yazdir(s)

    print("\n" + "=" * 60)
    print("ÖZET TABLO (Riske göre sıralı)")
    print("=" * 60)
    for s in sorted(sonuclar, key=lambda x: -x.reba_skoru):
        print(f"  {s.istasyon:45} REBA={s.reba_skoru:2d}  [{s.risk_seviyesi}]")

    print("\n" + "=" * 60)
    print("İYİLEŞTİRME ÖNCESİ / SONRASI KARŞILAŞTIRMA")
    print("=" * 60)
    onceki = sonuclar[2]  # Mehmet Demir - en riskli
    sonraki = reba_hesapla(iyilestirme_senaryosu())
    print(f"  Öncesi : REBA={onceki.reba_skoru}  [{onceki.risk_seviyesi}]")
    print(f"  Sonrası: REBA={sonraki.reba_skoru}  [{sonraki.risk_seviyesi}]")
    print(f"  İyileşme: {onceki.reba_skoru - sonraki.reba_skoru} puan düşüş")
