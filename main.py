import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from ga.engine      import jalankan_ga
from utils.reporter import cetak_jadwal, cetak_durasi_kerja, cetak_rekap_staf, cetak_ringkasan
from utils.plotter  import plot_konvergensi
from utils.exporter import simpan_json, simpan_csv
from utils.export_history import simpan_history_generasi

HASIL_DIR = os.path.join(os.path.dirname(__file__), "results")


def main() -> None:
    hasil    = jalankan_ga(verbose=True)
    kromosom = hasil["kromosom_terbaik"]
    fitness  = hasil["fitness_terbaik"]

    cetak_jadwal(kromosom, fitness)
    cetak_durasi_kerja(kromosom)
    cetak_rekap_staf(kromosom)
    cetak_ringkasan(hasil)

    plot_konvergensi(
        hasil["riwayat_terbaik"],
        hasil["riwayat_rata2"],
        simpan_ke=os.path.join(HASIL_DIR, "konvergensi_ga.png"),
    )

    meta = {
        "generasi_terbaik" : hasil["generasi_terbaik"],
        "total_generasi"   : hasil["total_generasi"],
        "waktu_komputasi"  : round(hasil["waktu_komputasi"], 4),
        "alasan_berhenti"  : hasil["alasan_berhenti"],
    }
    simpan_json(kromosom, fitness, os.path.join(HASIL_DIR, "jadwal_terbaik.json"), meta)
    simpan_csv (kromosom, fitness, os.path.join(HASIL_DIR, "jadwal_terbaik.csv"))
    simpan_history_generasi(hasil["history_generasi"], os.path.join(HASIL_DIR, "history_generasi.csv"))
    print("\n  Semua output tersimpan di folder results/\n")


if __name__ == "__main__":
    main()
