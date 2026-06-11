import random
import copy
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from config import PROB_MUTASI, JUMLAH_KARYAWAN, JUMLAH_HARI
def mutasi(
    kromosom: list[list[int]],
    pm: float = PROB_MUTASI,
) -> list[list[int]]:
    kromosom_baru = copy.deepcopy(kromosom)

    for k in range(JUMLAH_KARYAWAN):
        for hari in range(JUMLAH_HARI):
            # Bangkitkan bilangan acak [0.0, 1.0) untuk gen ini
            if random.random() < pm:
                # Ganti nilai gen dengan shift acak dari {0, 1, 2, 3}
                kromosom_baru[k][hari] = random.randint(0, 3)

    return kromosom_baru