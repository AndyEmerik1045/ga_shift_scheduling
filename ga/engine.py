import copy
import time
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from config import (
    UKURAN_POPULASI,
    GENERASI_MAKS,
    PROB_CROSSOVER,
    PROB_MUTASI,
    JUMLAH_ELITE,
    TOURNAMENT_K,
    KONVERGENSI_GEN,
    THRESHOLD_FITNESS,
)
from ga.population import inisialisasi_populasi
from ga.fitness    import hitung_fitness_populasi
from ga.selection  import tournament_selection, ambil_elite
from ga.crossover  import two_point_crossover
from ga.mutation   import mutasi


def jalankan_ga(verbose: bool = True) -> dict:
    if verbose:
        print("=" * 62)
        print("  ALGORITMA GENETIKA — PENJADWALAN SHIFT KARYAWAN")
        print("=" * 62)
        print(f"  Populasi : {UKURAN_POPULASI:<5}  |  Generasi Maks : {GENERASI_MAKS}")
        print(f"  Pc       : {PROB_CROSSOVER:<5}  |  Pm             : {PROB_MUTASI}")
        print(f"  Elitisme : {JUMLAH_ELITE} ind    |  Tournament k   : {TOURNAMENT_K}")
        print("=" * 62)

    waktu_mulai            = time.time()
    populasi               = inisialisasi_populasi()
    riwayat_terbaik        = []
    riwayat_rata2          = []
    fitness_terbaik_global = -1.0
    kromosom_terbaik       = None
    generasi_terbaik       = 0
    tidak_ada_perbaikan    = 0
    alasan_berhenti        = f"Generasi maks ({GENERASI_MAKS}) tercapai"

    for gen in range(GENERASI_MAKS):
        fitness_list = hitung_fitness_populasi(populasi)
        ft = max(fitness_list)
        fr = sum(fitness_list) / len(fitness_list)
        riwayat_terbaik.append(ft)
        riwayat_rata2.append(fr)

        idx_terbaik = fitness_list.index(ft)
        if ft > fitness_terbaik_global:
            fitness_terbaik_global = ft
            kromosom_terbaik       = copy.deepcopy(populasi[idx_terbaik])
            generasi_terbaik       = gen + 1
            tidak_ada_perbaikan    = 0
        else:
            tidak_ada_perbaikan += 1

        if verbose and ((gen + 1) % 50 == 0 or gen == 0):
            print(
                f"  Gen {gen+1:>3d}  |  "
                f"Fitness Terbaik: {ft:>6.1f}  |  "
                f"Rata-rata: {fr:>6.1f}  |  "
                f"Tanpa Perbaikan: {tidak_ada_perbaikan}"
            )

        if tidak_ada_perbaikan >= KONVERGENSI_GEN:
            alasan_berhenti = f"Konvergensi ({tidak_ada_perbaikan} gen tanpa perbaikan)"
            if verbose:
                print(f"\n  TERMINASI: {alasan_berhenti}")
            break

        if (fitness_terbaik_global / 1000) * 100 >= THRESHOLD_FITNESS:
            alasan_berhenti = f"Threshold fitness {THRESHOLD_FITNESS}% tercapai"
            if verbose:
                print(f"\n  TERMINASI: {alasan_berhenti}")
            break

        elite         = ambil_elite(populasi, fitness_list)
        populasi_baru = elite[:]

        while len(populasi_baru) < UKURAN_POPULASI:
            p1 = tournament_selection(populasi, fitness_list)
            p2 = tournament_selection(populasi, fitness_list)
            c1, c2 = two_point_crossover(p1, p2)
            populasi_baru.append(mutasi(c1))
            if len(populasi_baru) < UKURAN_POPULASI:
                populasi_baru.append(mutasi(c2))

        populasi = populasi_baru

    waktu_komputasi = time.time() - waktu_mulai
    total_gen       = len(riwayat_terbaik)

    if verbose:
        print(f"\n{'='*62}")
        print(f"  HASIL AKHIR")
        print(f"{'='*62}")
        print(f"  Fitness Terbaik  : {fitness_terbaik_global} / 1000"
              f"  ({(fitness_terbaik_global / 1000) * 100:.1f}%)")
        print(f"  Ditemukan di     : Generasi {generasi_terbaik}")
        print(f"  Total Generasi   : {total_gen}")
        print(f"  Alasan Berhenti  : {alasan_berhenti}")
        print(f"  Waktu Komputasi  : {waktu_komputasi:.4f} detik")
        print(f"{'='*62}\n")

    return {
        "kromosom_terbaik" : kromosom_terbaik,
        "fitness_terbaik"  : fitness_terbaik_global,
        "generasi_terbaik" : generasi_terbaik,
        "total_generasi"   : total_gen,
        "waktu_komputasi"  : waktu_komputasi,
        "alasan_berhenti"  : alasan_berhenti,
        "riwayat_terbaik"  : riwayat_terbaik,
        "riwayat_rata2"    : riwayat_rata2,
    }
