import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from config import (
    JUMLAH_KARYAWAN,
    JUMLAH_HARI,
    MIN_STAF_PER_SHIFT,
    MAKS_JAM_KERJA_MGGN,
    MIN_JAM_KERJA_MGGN,
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

    # Hard Constraint 1
    for hari in range(JUMLAH_HARI):
        for shift in (1, 2, 3):
            jumlah = sum(
                1 for k in range(JUMLAH_KARYAWAN)
                if kromosom[k][hari] == shift
            )
            if jumlah < MIN_STAF_PER_SHIFT:
                penalti += W_MIN_STAF * (MIN_STAF_PER_SHIFT - jumlah)

    # Hard Constraint 2 & 3
    hari_kerja_semua = []

    for k in range(JUMLAH_KARYAWAN):
        hari_kerja = sum(
            1 for hari in range(JUMLAH_HARI)
            if kromosom[k][hari] != 0
        )

        hari_kerja_semua.append(hari_kerja)

        if hari_kerja > MAKS_JAM_KERJA_MGGN:
            penalti += W_MAKS_JAM * (hari_kerja - MAKS_JAM_KERJA_MGGN)

        if hari_kerja < MIN_JAM_KERJA_MGGN:
            penalti += W_MIN_JAM * (MIN_JAM_KERJA_MGGN - hari_kerja)

    # Soft Constraint Baru:
    # Pemerataan beban kerja antar karyawan
    rata = sum(hari_kerja_semua) / JUMLAH_KARYAWAN

    for hk in hari_kerja_semua:
        penalti += abs(hk - rata)

    # Soft Constraint:
    # Distribusi shift merata
    total_shift = [0, 0, 0]

    for k in range(JUMLAH_KARYAWAN):
        for hari in range(JUMLAH_HARI):
            s = kromosom[k][hari]
            if s > 0:
                total_shift[s - 1] += 1

    rata2 = sum(total_shift) / 3 if sum(total_shift) > 0 else 0

    for ts in total_shift:
        penalti += W_DISTRIBUSI * abs(ts - rata2)

    # Soft Constraint:
    # Preferensi karyawan
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
