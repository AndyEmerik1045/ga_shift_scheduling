import random
import copy
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from config import PROB_CROSSOVER, JUMLAH_KARYAWAN

def two_point_crossover(
    parent1: list[list[int]],
    parent2: list[list[int]],
    pc: float = PROB_CROSSOVER,
) -> tuple[list[list[int]], list[list[int]]]:
    # Jika tidak terjadi crossover, kembalikan salinan langsung
    if random.random() > pc:
        return copy.deepcopy(parent1), copy.deepcopy(parent2)

    # Pilih dua titik potong secara acak di level baris karyawan.
    # Range [1, JUMLAH_KARYAWAN-1] agar minimal ada satu baris dari setiap
    # sisi yang dipertukarkan (titik1 ≠ titik2 dijamin oleh random.sample).
    titik1, titik2 = sorted(random.sample(range(1, JUMLAH_KARYAWAN), 2))

    # Bentuk dua anak dengan mempertukarkan segmen di antara titik potong
    child1 = (
        [copy.deepcopy(baris) for baris in parent1[:titik1]]
        + [copy.deepcopy(baris) for baris in parent2[titik1:titik2]]
        + [copy.deepcopy(baris) for baris in parent1[titik2:]]
    )
    child2 = (
        [copy.deepcopy(baris) for baris in parent2[:titik1]]
        + [copy.deepcopy(baris) for baris in parent1[titik1:titik2]]
        + [copy.deepcopy(baris) for baris in parent2[titik2:]]
    )

    return child1, child2


# ---------------------------------------------------------------------------
# Versi verbose — mengembalikan metadata titik potong (untuk logging/debug)
# ---------------------------------------------------------------------------

def two_point_crossover_verbose(
    parent1: list[list[int]],
    parent2: list[list[int]],
    pc: float = PROB_CROSSOVER,
) -> tuple[list[list[int]], list[list[int]], dict]:
    """
    Sama seperti two_point_crossover, tetapi juga mengembalikan dict
    berisi informasi titik potong yang digunakan.
    """
    if random.random() > pc:
        return copy.deepcopy(parent1), copy.deepcopy(parent2), {
            "terjadi": False,
            "titik1": None,
            "titik2": None,
        }

    titik1, titik2 = sorted(random.sample(range(1, JUMLAH_KARYAWAN), 2))

    child1 = (
        [copy.deepcopy(baris) for baris in parent1[:titik1]]
        + [copy.deepcopy(baris) for baris in parent2[titik1:titik2]]
        + [copy.deepcopy(baris) for baris in parent1[titik2:]]
    )
    child2 = (
        [copy.deepcopy(baris) for baris in parent2[:titik1]]
        + [copy.deepcopy(baris) for baris in parent1[titik1:titik2]]
        + [copy.deepcopy(baris) for baris in parent2[titik2:]]
    )

    return child1, child2, {
        "terjadi": True,
        "titik1": titik1,   # indeks baris karyawan pertama yang dipotong
        "titik2": titik2,   # indeks baris karyawan kedua yang dipotong
    }