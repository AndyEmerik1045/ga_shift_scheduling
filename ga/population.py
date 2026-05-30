import random
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from config import (
    JUMLAH_KARYAWAN,
    JUMLAH_HARI,
    MIN_JAM_KERJA_MGGN,
    MAKS_JAM_KERJA_MGGN,
    UKURAN_POPULASI,
)


def buat_kromosom() -> list[list[int]]:
    kromosom = []
    for _ in range(JUMLAH_KARYAWAN):
        hari_kerja = random.randint(MIN_JAM_KERJA_MGGN, MAKS_JAM_KERJA_MGGN)
        hari_aktif = set(random.sample(range(JUMLAH_HARI), hari_kerja))
        gen = [
            random.randint(1, 3) if hari in hari_aktif else 0
            for hari in range(JUMLAH_HARI)
        ]
        kromosom.append(gen)
    return kromosom


def inisialisasi_populasi() -> list[list[list[int]]]:
    return [buat_kromosom() for _ in range(UKURAN_POPULASI)]
