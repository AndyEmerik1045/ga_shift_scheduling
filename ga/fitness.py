import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from config import (
    JUMLAH_KARYAWAN,
    JUMLAH_HARI,
    MIN_STAF_PER_SHIFT,
    MAKS_HARI_KERJA_MGGN,
    MIN_HARI_KERJA_MGGN,
    W_MIN_STAF,
    W_MAKS_JAM,
    W_MIN_JAM,
    W_DISTRIBUSI,
    W_PREFERENSI,
    PREFERENSI_KARYAWAN,
)

F_MAX = 1000


def hitung_fitness(kromosom: list[list[int]]) -> float:
    penalti = 0.0

    # ── Hard Constraint 1 ─────────────────────────────────────
    # Min 2 staf per shift per hari (w=10)
    for hari in range(JUMLAH_HARI):
        for shift in (1, 2, 3):
            jumlah = sum(
                1 for k in range(JUMLAH_KARYAWAN)
                if kromosom[k][hari] == shift
            )
            if jumlah < MIN_STAF_PER_SHIFT:
                penalti += W_MIN_STAF * (MIN_STAF_PER_SHIFT - jumlah)

    # ── Hard Constraint 2 & 3 ─────────────────────────────────
    # Maks 6 hari kerja (w=15) dan Min 3 hari kerja (w=8)
    hari_kerja_semua = []

    for k in range(JUMLAH_KARYAWAN):
        hari_kerja = sum(
            1 for hari in range(JUMLAH_HARI)
            if kromosom[k][hari] != 0
        )
        hari_kerja_semua.append(hari_kerja)

        if hari_kerja > MAKS_HARI_KERJA_MGGN:                        
            penalti += W_MAKS_JAM * (hari_kerja - MAKS_HARI_KERJA_MGGN) 

        if hari_kerja < MIN_HARI_KERJA_MGGN:                        
            penalti += W_MIN_JAM * (MIN_HARI_KERJA_MGGN - hari_kerja)    

    # ── Soft Constraint 1 ─────────────────────────────────────
    # Distribusi shift merata (w=3)
    total_shift = [0, 0, 0]

    for k in range(JUMLAH_KARYAWAN):
        for hari in range(JUMLAH_HARI):
            s = kromosom[k][hari]
            if s > 0:
                total_shift[s - 1] += 1

    rata2 = sum(total_shift) / 3 if sum(total_shift) > 0 else 0

    for ts in total_shift:
        penalti += W_DISTRIBUSI * abs(ts - rata2)

    # ── Soft Constraint 2 ─────────────────────────────────────
    # Preferensi shift karyawan (w=2)
    for k in range(JUMLAH_KARYAWAN):
        pref = PREFERENSI_KARYAWAN[k]

        if pref == 0:
            continue

        jumlah_pref = sum(
            1 for hari in range(JUMLAH_HARI)
            if kromosom[k][hari] == pref
        )

        if jumlah_pref < 2:
            penalti += W_PREFERENSI * (2 - jumlah_pref)

    return max(0.0, F_MAX - penalti)


def hitung_fitness_populasi(populasi: list) -> list[float]:
    return [hitung_fitness(ind) for ind in populasi]
