import random
import copy
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from config import PROB_CROSSOVER, JUMLAH_KARYAWAN


def two_point_crossover(
    parent1 : list[list[int]],
    parent2 : list[list[int]],
    pc      : float = PROB_CROSSOVER,
) -> tuple[list, list]:
    if random.random() > pc:
        return copy.deepcopy(parent1), copy.deepcopy(parent2)

    titik1, titik2 = sorted(random.sample(range(1, JUMLAH_KARYAWAN), 2))

    child1 = parent1[:titik1] + parent2[titik1:titik2] + parent1[titik2:]
    child2 = parent2[:titik1] + parent1[titik1:titik2] + parent2[titik2:]

    return (
        [copy.deepcopy(baris) for baris in child1],
        [copy.deepcopy(baris) for baris in child2],
    )
