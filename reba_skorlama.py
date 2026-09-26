"""
REBA (Rapid Entire Body Assessment) ile Ergonomik Risk Değerlendirmesi
==========================================================================

Endüstri Mühendisliği - İş Sağlığı ve Güvenliği / Ergonomi

Kaynak: Hignett, S., McAtamney, L. (2000). Rapid Entire Body Assessment
(REBA). Applied Ergonomics, 31(2), 201-205.

Neden REBA (RULA değil)?
--------------------------
RULA (Rapid Upper Limb Assessment) sadece üst uzuvlara (kol, bilek,
boyun) odaklanır ve masa başı/hafif montaj işleri için tasarlanmıştır.
REBA ise TÜM VÜCUDU (gövde, boyun, bacaklar dahil) değerlendirir ve
malzeme taşıma, kaldırma, itme-çekme gibi ağır fiziksel işler için daha
uygundur — bu yüzden üretim/depo/hastane ortamlarında daha sık kullanılır.

Yöntem
------
REBA, gözlemlenen bir duruşu, standart LOOKUP TABLE'lar (Tablo A, B, C)
üzerinden 1-15 arası tek bir risk skoruna indirger:

    GRUP A: Gövde (Trunk) + Boyun (Neck) + Bacaklar (Legs)
            -> Tablo A'dan Duruş Skoru A
            -> + Kuvvet/Yük Skoru = SKOR A

    GRUP B: Üst Kol (Upper Arm) + Alt Kol (Lower Arm) + Bilek (Wrist)
            -> Tablo B'den Duruş Skoru B
            -> + Kavrama (Coupling) Skoru = SKOR B

    SKOR A ve SKOR B, Tablo C'de kesiştirilerek TEMEL REBA SKORU bulunur.

    NİHAİ REBA SKORU = Temel Skor + Aktivite Skoru (statik duruş, tekrarlı
                        hareket, ani/dengesiz hareket gibi ek faktörler)

Risk Seviyeleri
---------------
    1       : İhmal edilebilir risk       -> Aksiyon gerekmez
    2-3     : Düşük risk                  -> Değişiklik gerekebilir
    4-7     : Orta risk                   -> Araştırılmalı, yakında değişiklik
    8-10    : Yüksek risk                 -> Araştırılmalı, değişiklik uygulanmalı
    11-15   : Çok yüksek risk             -> ACİL değişiklik gerekli

NOT (şeffaflık): Tablo A/B/C değerleri, yayınlanmış REBA metodolojisinden
(Hignett & McAtamney, 2000) elde edilmiştir. Bu proje eğitim/portföy
amaçlıdır; gerçek bir İSG değerlendirmesinde kullanılmadan önce
değerlerin orijinal makale veya sertifikalı bir REBA formu ile
karşılaştırılması önerilir.
"""

from dataclasses import dataclass, field


# --------------------------------------------------------------------------
# TABLO A: Gövde x Boyun x Bacak -> Duruş Skoru A
# Anahtar: (govde_skoru, boyun_skoru) -> [bacak=1, bacak=2, bacak=3, bacak=4]
# --------------------------------------------------------------------------
TABLO_A = {
    (1, 1): [1, 2, 3, 4],
    (2, 1): [2, 3, 4, 5],
    (3, 1): [2, 4, 5, 6],
    (4, 1): [3, 5, 6, 7],
    (5, 1): [4, 6, 7, 8],
    (1, 2): [1, 2, 3, 4],
    (2, 2): [3, 4, 5, 6],
    (3, 2): [4, 5, 6, 7],
    (4, 2): [5, 6, 7, 8],
    (5, 2): [6, 7, 8, 9],
    (1, 3): [3, 3, 5, 6],
    (2, 3): [4, 5, 6, 7],
    (3, 3): [5, 6, 7, 8],
    (4, 3): [6, 7, 8, 9],
    (5, 3): [7, 8, 9, 9],
}

# --------------------------------------------------------------------------
# TABLO B: Üst Kol x Alt Kol x Bilek -> Duruş Skoru B
# Anahtar: (ust_kol_skoru, alt_kol_skoru) -> [bilek=1, bilek=2, bilek=3]
# --------------------------------------------------------------------------
TABLO_B = {
    (1, 1): [1, 2, 2],
    (1, 2): [1, 2, 3],
    (2, 1): [1, 2, 3],
    (2, 2): [2, 3, 4],
    (3, 1): [3, 4, 5],
    (3, 2): [4, 5, 5],
    (4, 1): [4, 5, 5],
    (4, 2): [5, 6, 7],
    (5, 1): [6, 7, 8],
    (5, 2): [7, 8, 8],
    (6, 1): [7, 8, 8],
    (6, 2): [8, 9, 9],
}

# --------------------------------------------------------------------------
# TABLO C: Skor A (satır, 1-12) x Skor B (sütun, 1-12) -> Temel REBA Skoru
# --------------------------------------------------------------------------
TABLO_C = [
    [1, 1, 1, 2, 3, 3, 4, 5, 6, 7, 7, 7],
    [1, 2, 2, 3, 4, 4, 5, 6, 6, 7, 7, 8],
    [2, 3, 3, 3, 4, 5, 6, 7, 7, 8, 8, 8],
    [3, 4, 4, 4, 5, 6, 7, 8, 8, 9, 9, 9],
    [4, 4, 4, 5, 6, 7, 8, 8, 9, 9, 9, 9],
    [6, 6, 6, 7, 8, 8, 9, 9, 10, 10, 10, 10],
    [7, 7, 7, 8, 9, 9, 9, 10, 10, 11, 11, 11],
    [8, 8, 8, 9, 10, 10, 10, 10, 10, 11, 11, 11],
    [9, 9, 9, 10, 10, 10, 11, 11, 11, 12, 12, 12],
    [10, 10, 10, 11, 11, 11, 11, 12, 12, 12, 12, 12],
    [11, 11, 11, 11, 12, 12, 12, 12, 12, 12, 12, 12],
    [12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12],
]


@dataclass
class Durus:
    """Bir çalışanın gözlemlenen anlık duruşunu tanımlar."""
    isci_adi: str
    istasyon: str

    # --- Grup A: Gövde, Boyun, Bacak ---
    govde_aci: float        # gövde eğilme açısı (derece); 0 = dik
    govde_burkulmus: bool = False
    govde_yana_egik: bool = False
    boyun_aci: float = 10.0  # boyun eğilme açısı (derece)
    boyun_burkulmus: bool = False
    boyun_yana_egik: bool = False
    bacak_bilateral: bool = True   # True: iki ayak yere basıyor / oturuyor
    diz_flexion_aci: float = 0.0   # diz bükülme açısı (bilateral değilse)

    # --- Grup B: Üst kol, Alt kol, Bilek ---
    ust_kol_aci: float = 20.0      # omuz fleksiyon açısı (derece)
    omuz_kalkik: bool = False
    kol_abduksiyon: bool = False
    kol_desteklenmis: bool = False  # -1 puan (kol desteklenmiş/yaslanmış)
    alt_kol_aci: float = 80.0       # dirsek açısı (derece)
    bilek_aci: float = 5.0          # bilek fleksiyon/ekstansiyon açısı
    bilek_orta_hattan_sapmis: bool = False
    bilek_burkulmus: bool = False

    # --- Ek faktörler ---
    yuk_kg: float = 0.0
    ani_kuvvet: bool = False       # ani/şok kuvvet var mı
    kavrama: str = "iyi"           # "iyi", "orta", "kotu", "kabul_edilemez"
    statik_durus: bool = False     # >1 dakika sabit tutulan duruş
    tekrarli_hareket: bool = False  # dakikada 4'ten fazla tekrar
    dengesiz_taban: bool = False   # ani/dengesiz büyük hareket


# --------------------------------------------------------------------------
# Alt-skor hesaplama fonksiyonları (açıdan REBA puanına çevirme)
# --------------------------------------------------------------------------

def govde_skoru(d: Durus) -> int:
    aci = abs(d.govde_aci)
    if aci <= 0:
        skor = 1
    elif aci <= 20:
        skor = 2
    elif aci <= 60:
        skor = 3
    else:
        skor = 4
    if d.govde_burkulmus:
        skor += 1
    if d.govde_yana_egik:
        skor += 1
    return skor


def boyun_skoru(d: Durus) -> int:
    skor = 1 if 0 <= d.boyun_aci <= 20 else 2
    if d.boyun_burkulmus:
        skor += 1
    if d.boyun_yana_egik:
        skor += 1
    return skor


def bacak_skoru(d: Durus) -> int:
    skor = 1 if d.bacak_bilateral else 2
    if not d.bacak_bilateral:
        if d.diz_flexion_aci > 60:
            skor += 2
        elif d.diz_flexion_aci >= 30:
            skor += 1
    return skor


def ust_kol_skoru(d: Durus) -> int:
    aci = d.ust_kol_aci
    if -20 <= aci <= 20:
        skor = 1
    elif aci < -20 or 20 < aci <= 45:
        skor = 2
    elif 45 < aci <= 90:
        skor = 3
    else:
        skor = 4
    if d.omuz_kalkik:
        skor += 1
    if d.kol_abduksiyon:
        skor += 1
    if d.kol_desteklenmis:
        skor -= 1
    return max(1, skor)


def alt_kol_skoru(d: Durus) -> int:
    return 1 if 60 <= d.alt_kol_aci <= 100 else 2


def bilek_skoru(d: Durus) -> int:
    skor = 1 if abs(d.bilek_aci) <= 15 else 2
    if d.bilek_orta_hattan_sapmis:
        skor += 1
    if d.bilek_burkulmus:
        skor += 1
    return skor


def yuk_skoru(d: Durus) -> int:
    if d.yuk_kg < 5:
        skor = 0
    elif d.yuk_kg <= 10:
        skor = 1
    else:
        skor = 2
    if d.ani_kuvvet:
        skor += 1
    return skor


KAVRAMA_SKORU = {"iyi": 0, "orta": 1, "kotu": 2, "kabul_edilemez": 3}


def aktivite_skoru(d: Durus) -> int:
    skor = 0
    if d.statik_durus:
        skor += 1
    if d.tekrarli_hareket:
        skor += 1
    if d.dengesiz_taban:
        skor += 1
    return skor


# --------------------------------------------------------------------------
# Ana REBA hesaplama fonksiyonu
# --------------------------------------------------------------------------

@dataclass
class RebaSonucu:
    isci_adi: str
    istasyon: str
    govde: int
    boyun: int
    bacak: int
    ust_kol: int
    alt_kol: int
    bilek: int
    duras_a: int
    duras_b: int
    skor_a: int
    skor_b: int
    temel_skor: int
    aktivite: int
    reba_skoru: int
    risk_seviyesi: str
    aksiyon: str


def risk_seviyesi_belirle(reba_skoru: int) -> tuple[str, str]:
    if reba_skoru == 1:
        return "İhmal Edilebilir", "Aksiyon gerekmez"
    elif reba_skoru <= 3:
        return "Düşük", "Değişiklik gerekebilir"
    elif reba_skoru <= 7:
        return "Orta", "Araştırılmalı, yakında değişiklik yapılmalı"
    elif reba_skoru <= 10:
        return "Yüksek", "Araştırılmalı, değişiklik uygulanmalı"
    else:
        return "Çok Yüksek", "ACİL değişiklik gerekli"


def reba_hesapla(d: Durus) -> RebaSonucu:
    govde = govde_skoru(d)
    boyun = boyun_skoru(d)
    bacak = bacak_skoru(d)
    ust_kol = ust_kol_skoru(d)
    alt_kol = alt_kol_skoru(d)
    bilek = bilek_skoru(d)

    govde_idx = min(govde, 5)
    boyun_idx = min(boyun, 3)
    bacak_idx = min(bacak, 4)
    duras_a = TABLO_A[(govde_idx, boyun_idx)][bacak_idx - 1]
    skor_a = duras_a + yuk_skoru(d)

    ust_kol_idx = min(ust_kol, 6)
    alt_kol_idx = min(alt_kol, 2)
    bilek_idx = min(bilek, 3)
    duras_b = TABLO_B[(ust_kol_idx, alt_kol_idx)][bilek_idx - 1]
    skor_b = duras_b + KAVRAMA_SKORU[d.kavrama]

    satir = min(skor_a, 12) - 1
    sutun = min(skor_b, 12) - 1
    temel_skor = TABLO_C[satir][sutun]

    aktivite = aktivite_skoru(d)
    reba_skoru = temel_skor + aktivite

    risk, aksiyon = risk_seviyesi_belirle(reba_skoru)

    return RebaSonucu(
        isci_adi=d.isci_adi, istasyon=d.istasyon,
        govde=govde, boyun=boyun, bacak=bacak,
        ust_kol=ust_kol, alt_kol=alt_kol, bilek=bilek,
        duras_a=duras_a, duras_b=duras_b,
        skor_a=skor_a, skor_b=skor_b,
        temel_skor=temel_skor, aktivite=aktivite,
        reba_skoru=reba_skoru, risk_seviyesi=risk, aksiyon=aksiyon,
    )


def sonucu_yazdir(s: RebaSonucu):
    print(f"\n{s.isci_adi} — {s.istasyon}")
    print("-" * 50)
    print(f"  Grup A: Gövde={s.govde} Boyun={s.boyun} Bacak={s.bacak}  "
          f"-> Duruş A={s.duras_a}  +Yük  -> Skor A={s.skor_a}")
    print(f"  Grup B: ÜstKol={s.ust_kol} AltKol={s.alt_kol} Bilek={s.bilek}  "
          f"-> Duruş B={s.duras_b}  +Kavrama -> Skor B={s.skor_b}")
    print(f"  Tablo C (Skor A x Skor B) -> Temel Skor = {s.temel_skor}")
    print(f"  + Aktivite Skoru ({s.aktivite}) -> REBA SKORU = {s.reba_skoru}")
    print(f"  Risk Seviyesi: {s.risk_seviyesi}  ({s.aksiyon})")


if __name__ == "__main__":
    ornek = Durus(
        isci_adi="Test Çalışanı", istasyon="Test İstasyonu",
        govde_aci=45, govde_burkulmus=True,
        boyun_aci=25, ust_kol_aci=70, omuz_kalkik=True,
        alt_kol_aci=110, bilek_aci=20, bilek_orta_hattan_sapmis=True,
        yuk_kg=12, kavrama="orta", statik_durus=True,
    )
    sonuc = reba_hesapla(ornek)
    sonucu_yazdir(sonuc)
