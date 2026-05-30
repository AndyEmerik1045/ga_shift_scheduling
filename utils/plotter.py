import os
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


def plot_konvergensi(
    riwayat_terbaik : list,
    riwayat_rata2   : list,
    simpan_ke       : str  = "results/konvergensi_ga.png",
    tampilkan       : bool = False,
) -> str:
    os.makedirs(os.path.dirname(os.path.abspath(simpan_ke)), exist_ok=True)

    n = len(riwayat_terbaik)

    satu_generasi = (n == 1)
    if satu_generasi:
        riwayat_terbaik = riwayat_terbaik * 2
        riwayat_rata2   = riwayat_rata2   * 2

    generasi = list(range(1, len(riwayat_terbaik) + 1))

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(generasi, riwayat_terbaik,
        color="#1a6fb5", linewidth=2, label="Fitness Terbaik", zorder=3)
    ax.plot(generasi, riwayat_rata2,
        color="#e07b39", linewidth=1.5, linestyle="--",
        label="Fitness Rata-rata", zorder=2)
    ax.fill_between(generasi, riwayat_rata2, riwayat_terbaik,
        alpha=0.12, color="#1a6fb5")

    ax.annotate(
        f"  {max(riwayat_terbaik):.0f}",
        xy=(generasi[-1], max(riwayat_terbaik)),
        fontsize=10, color="#1a6fb5", va="center",
    )

    judul = (
        "Konvergensi Algoritma Genetika\n"
        "Penjadwalan Shift Karyawan Minimarket 24 Jam"
    )
    if satu_generasi:
        judul += "\n(Threshold langsung tercapai di generasi pertama)"

    ax.set_title(judul, fontsize=12, fontweight="bold", pad=14)
    ax.set_xlabel("Generasi", fontsize=11)
    ax.set_ylabel("Nilai Fitness", fontsize=11)
    ax.set_xlim(max(0, generasi[0] - 0.5), generasi[-1] + 0.5)
    ax.set_ylim(0, 1050)
    ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(100))
    ax.grid(True, linestyle="--", alpha=0.5)
    ax.legend(fontsize=10)

    plt.tight_layout()
    plt.savefig(simpan_ke, dpi=150, bbox_inches="tight")
    if tampilkan:
        plt.show()
    plt.close()

    print(f"  Grafik konvergensi disimpan : {simpan_ke}")
    return simpan_ke
