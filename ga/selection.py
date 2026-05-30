import random
import copy
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from config import TOURNAMENT_K, JUMLAH_ELITE


def tournament_selection(
    populasi     : list,
    fitness_list : list[float],
    k            : int = TOURNAMENT_K,
) -> list:
    kandidat_idx = random.sample(range(len(populasi)), k)
    terbaik_idx  = max(kandidat_idx, key=lambda i: fitness_list[i])
    return copy.deepcopy(populasi[terbaik_idx])


def ambil_elite(
    populasi     : list,
    fitness_list : list[float],
    n            : int = JUMLAH_ELITE,
) -> list:
    sorted_idx = sorted(range(len(populasi)), key=lambda i: fitness_list[i], reverse=True)
    return [copy.deepcopy(populasi[i]) for i in sorted_idx[:n]]
