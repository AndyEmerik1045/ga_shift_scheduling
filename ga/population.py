import random
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from config import (
    JUMLAH_KARYAWAN,
    JUMLAH_HARI,
    MIN_HARI_KERJA_MGGN,
    MAKS_HARI_KERJA_MGGN,
    UKURAN_POPULASI,
)


# ── ID karyawan tetap (ditambahkan sesuai permintaan dosen) ───
ID_KARYAWAN = [f"K{i+1:02d}" for i in range(JUMLAH_KARYAWAN)]
# Hasil: ["K01", "K02", ..., "K12"]


def buat_kromosom() -> list[list[int]]:
    kromosom = []
    for _ in range(JUMLAH_KARYAWAN):
        # HC2 & HC3: jumlah hari kerja antara MIN (3) dan MAKS (6)
        jumlah_hari_kerja = random.randint(MIN_HARI_KERJA_MGGN, MAKS_HARI_KERJA_MGGN)

        # Pilih hari kerja secara acak tanpa pengulangan
        hari_aktif = set(random.sample(range(JUMLAH_HARI), jumlah_hari_kerja))

        # Bentuk gen: shift acak untuk hari kerja, 0 untuk hari libur
        gen = [
            random.randint(1, 3) if hari in hari_aktif else 0
            for hari in range(JUMLAH_HARI)
        ]
        kromosom.append(gen)

    return kromosom


def inisialisasi_populasi() -> list[list[list[int]]]:
    return [buat_kromosom() for _ in range(UKURAN_POPULASI)]


def get_id_karyawan() -> list[str]:
    return ID_KARYAWAN.copy()


def kromosom_ke_label(kromosom: list[list[int]]) -> dict:
    return {ID_KARYAWAN[i]: kromosom[i] for i in range(JUMLAH_KARYAWAN)}