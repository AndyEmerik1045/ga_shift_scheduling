import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from tabulate import tabulate
from config import JUMLAH_KARYAWAN, JUMLAH_HARI, NAMA_HARI, NAMA_KARYAWAN


def cetak_jadwal(kromosom: list[list[int]], fitness: float) -> None:
    print("\n" + "=" * 74)
    print("  JADWAL SHIFT TERBAIK")
    print("=" * 74)

    header = ["Karyawan"] + NAMA_HARI + ["Jml Kerja"]
    rows   = []

    for k, nama in enumerate(NAMA_KARYAWAN):
        row        = [nama]
        hari_kerja = 0
        for hari in range(JUMLAH_HARI):
            s = kromosom[k][hari]
            if   s == 0: row.append("Libur")
            elif s == 1: row.append("Pagi");  hari_kerja += 1
            elif s == 2: row.append("Siang"); hari_kerja += 1
            elif s == 3: row.append("Malam"); hari_kerja += 1
        row.append(hari_kerja)
        rows.append(row)

    print(tabulate(rows, headers=header, tablefmt="grid"))
    print(f"\n  Fitness: {fitness:.1f} / 1000  ({(fitness / 1000) * 100:.1f}%)")


def cetak_rekap_staf(kromosom: list[list[int]]) -> None:
    print("\n" + "=" * 74)
    print("  REKAP JUMLAH STAF PER SHIFT PER HARI")
    print("=" * 74)

    header = ["Shift"] + NAMA_HARI
    rows   = []

    for shift, label in [
        (1, "Pagi  (06-14)"),
        (2, "Siang (14-22)"),
        (3, "Malam (22-06)"),
    ]:
        row = [label]
        for hari in range(JUMLAH_HARI):
            jml = sum(1 for k in range(JUMLAH_KARYAWAN) if kromosom[k][hari] == shift)
            row.append(jml)
        rows.append(row)

    print(tabulate(rows, headers=header, tablefmt="grid"))


def cetak_ringkasan(hasil: dict) -> None:
    print("\n" + "=" * 52)
    print("  RINGKASAN EKSEKUSI GA")
    print("=" * 52)
    pct = (hasil["fitness_terbaik"] / 1000) * 100
    rows = [
        ["Fitness Terbaik",  f"{hasil['fitness_terbaik']:.1f} / 1000  ({pct:.1f}%)"],
        ["Generasi Terbaik", hasil["generasi_terbaik"]],
        ["Total Generasi",   hasil["total_generasi"]],
        ["Waktu Komputasi",  f"{hasil['waktu_komputasi']:.4f} detik"],
        ["Alasan Berhenti",  hasil["alasan_berhenti"]],
    ]
    print(tabulate(rows, tablefmt="simple"))
