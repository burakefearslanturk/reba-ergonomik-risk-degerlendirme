"""
REBA Görselleştirme
======================
- Risk bölgeli (renk kodlu) istasyon karşılaştırma çubuk grafiği
- Her istasyon için Grup A / Grup B kırılım grafiği (hangi bölge riski
  sürüklüyor)
- İyileştirme öncesi/sonrası karşılaştırma
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from senaryolar import senaryolari_olustur, toplu_degerlendir, iyilestirme_senaryosu
from reba_skorlama import reba_hesapla


RISK_RENKLERI = {
    "İhmal Edilebilir": "#2E8B57",
    "Düşük": "#8FBC8F",
    "Orta": "#F4A259",
    "Yüksek": "#E07A5F",
    "Çok Yüksek": "#C1272D",
}


def risk_karsilastirma_ciz(ax, sonuclar):
    sonuclar_sirali = sorted(sonuclar, key=lambda x: -x.reba_skoru)
    isimler = [s.istasyon.split(".")[0] + "." for s in sonuclar_sirali]
    skorlar = [s.reba_skoru for s in sonuclar_sirali]
    renkler = [RISK_RENKLERI[s.risk_seviyesi] for s in sonuclar_sirali]

    cubuklar = ax.barh(isimler, skorlar, color=renkler, edgecolor="black")
    for cubuk, s in zip(cubuklar, sonuclar_sirali):
        ax.text(s.reba_skoru + 0.2, cubuk.get_y() + cubuk.get_height() / 2,
                f"{s.reba_skoru}  ({s.risk_seviyesi})", va="center", fontsize=8.5)

    # Risk bölgesi arka plan şeritleri
    bolgeler = [(0, 1, "#2E8B57"), (1, 3, "#8FBC8F"), (3, 7, "#F4A259"),
                (7, 10, "#E07A5F"), (10, 15, "#C1272D")]
    for baslangic, bitis, renk in bolgeler:
        ax.axvspan(baslangic, bitis, color=renk, alpha=0.08)

    ax.set_xlabel("REBA Skoru")
    ax.set_xlim(0, 15)
    ax.set_title("İş İstasyonlarına Göre Ergonomik Risk Sıralaması")
    ax.invert_yaxis()
    ax.grid(axis="x", alpha=0.3)


def kirilim_ciz(ax, sonuclar):
    isimler = [s.istasyon.split(".")[0] + "." for s in sonuclar]
    skor_a = [s.skor_a for s in sonuclar]
    skor_b = [s.skor_b for s in sonuclar]

    x = range(len(sonuclar))
    genislik = 0.35
    ax.bar([i - genislik/2 for i in x], skor_a, genislik,
           label="Skor A (Gövde+Boyun+Bacak+Yük)", color="#2E86AB")
    ax.bar([i + genislik/2 for i in x], skor_b, genislik,
           label="Skor B (Kol+Bilek+Kavrama)", color="#F4A259")

    ax.set_xticks(list(x))
    ax.set_xticklabels(isimler)
    ax.set_ylabel("Alt Grup Skoru")
    ax.set_title("Hangi Vücut Bölgesi Riski Sürüklüyor? (Grup A vs Grup B)")
    ax.legend(fontsize=8)
    ax.grid(axis="y", alpha=0.3)


def iyilestirme_ciz(ax, onceki, sonraki):
    kategoriler = ["Öncesi\n(Manuel Taşıma)", "Sonrası\n(İyileştirilmiş)"]
    skorlar = [onceki.reba_skoru, sonraki.reba_skoru]
    renkler = [RISK_RENKLERI[onceki.risk_seviyesi], RISK_RENKLERI[sonraki.risk_seviyesi]]

    cubuklar = ax.bar(kategoriler, skorlar, color=renkler, edgecolor="black", width=0.5)
    for cubuk, skor, sonuc in zip(cubuklar, skorlar, [onceki, sonraki]):
        ax.text(cubuk.get_x() + cubuk.get_width()/2, skor + 0.3,
                f"{skor}\n[{sonuc.risk_seviyesi}]", ha="center", fontweight="bold", fontsize=9)

    ax.annotate(
        f"−{onceki.reba_skoru - sonraki.reba_skoru} puan",
        xy=(0.5, (onceki.reba_skoru + sonraki.reba_skoru) / 2),
        xytext=(0.5, (onceki.reba_skoru + sonraki.reba_skoru) / 2 + 2),
        ha="center", fontsize=11, fontweight="bold", color="darkgreen",
        arrowprops=dict(arrowstyle="->", color="darkgreen"),
    )

    ax.set_ylabel("REBA Skoru")
    ax.set_ylim(0, 15)
    ax.set_title("İyileştirme Öncesi / Sonrası: Manuel Malzeme Taşıma İstasyonu")
    ax.grid(axis="y", alpha=0.3)


def main():
    senaryolar = senaryolari_olustur()
    sonuclar = toplu_degerlendir(senaryolar)

    onceki = sonuclar[2]
    sonraki = reba_hesapla(iyilestirme_senaryosu())

    fig1, ax1 = plt.subplots(figsize=(10, 5.5))
    risk_karsilastirma_ciz(ax1, sonuclar)
    plt.tight_layout()
    plt.savefig("risk_siralamasi.png", dpi=150)
    plt.close(fig1)

    fig2, ax2 = plt.subplots(figsize=(10, 5))
    kirilim_ciz(ax2, sonuclar)
    plt.tight_layout()
    plt.savefig("grup_kirilimi.png", dpi=150)
    plt.close(fig2)

    fig3, ax3 = plt.subplots(figsize=(7, 6))
    iyilestirme_ciz(ax3, onceki, sonraki)
    plt.tight_layout()
    plt.savefig("iyilestirme_karsilastirma.png", dpi=150)
    plt.close(fig3)

    print("Görseller kaydedildi:")
    print("  - risk_siralamasi.png")
    print("  - grup_kirilimi.png")
    print("  - iyilestirme_karsilastirma.png")


if __name__ == "__main__":
    main()
