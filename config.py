import random

JUMLAH_KARYAWAN = 12
JUMLAH_HARI     = 7
NAMA_HARI       = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
NAMA_KARYAWAN   = [f"Karyawan {i+1:02d}" for i in range(JUMLAH_KARYAWAN)]

SHIFT_LABEL = {
    0: "Libur",
    1: "Pagi  (06-14)",
    2: "Siang (14-22)",
    3: "Malam (22-06)",
}

UKURAN_POPULASI  = 100
GENERASI_MAKS    = 300
PROB_CROSSOVER   = 0.8
PROB_MUTASI      = 0.05
ELITISME_PCT     = 0.05
JUMLAH_ELITE     = max(1, int(UKURAN_POPULASI * ELITISME_PCT))
TOURNAMENT_K     = 3

KONVERGENSI_GEN   = 50
THRESHOLD_FITNESS = 99.0

MIN_STAF_PER_SHIFT  = 2
MAKS_JAM_KERJA_MGGN = 6
MIN_JAM_KERJA_MGGN  = 3

W_MIN_STAF   = 10
W_MAKS_JAM   = 15
W_MIN_JAM    = 8
W_DISTRIBUSI = 3
W_PREFERENSI = 2

random.seed(42)
PREFERENSI_KARYAWAN = [random.choice([0, 1, 2, 3]) for _ in range(JUMLAH_KARYAWAN)]
