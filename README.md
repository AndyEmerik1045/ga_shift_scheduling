# Optimasi Penjadwalan Shift Karyawan Minimarket 24 Jam

### Implementasi Algoritma Genetika — Python 3.12

> Studi kasus: Penjadwalan shift mingguan 12 karyawan minimarket 24 jam (Indomaret/Alfamart) menggunakan Algoritma Genetika dengan representasi kromosom integer, tournament selection, two-point crossover, dan value-change mutation.

---

## Daftar Isi

- [Hasil Algoritma](#hasil-algoritma)
- [Cara Setup](#cara-setup)
- [Cara Menjalankan](#cara-menjalankan)
- [Output Program](#output-program)
- [Eksperimen Parameter](#eksperimen-parameter)
- [Cara Kerja Algoritma](#cara-kerja-algoritma)
- [Kamus File](#kamus-file)
- [Struktur Folder](#struktur-folder)
- [Dependensi](#dependensi)

---

# Hasil Algoritma

| Parameter | Nilai |
|------------|--------|
| Fitness terbaik | **992 / 1000 (99.2%)** |
| Representasi kromosom | Integer Matrix (12 × 7) |
| Ukuran populasi | 100 |
| Probabilitas crossover (Pc) | 0.8 |
| Probabilitas mutasi (Pm) | 0.05 |
| Generasi maksimum | 300 |
| Kriteria terminasi | Konvergensi + Threshold + Max Generation |

---

# Cara Setup

## 1. Clone Repository

```bash
git clone https://github.com/AndyEmerik1045/ga_shift_scheduling.git
cd ga_shift_scheduling
```

## 2. Buat Virtual Environment (Opsional)

### Windows (CMD)

```bash
python -m venv venv
venv\Scripts\activate
```

### Windows (PowerShell)

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

> Jika menggunakan GitHub Codespaces, langkah ini dapat dilewati.

---

## 3. Install Dependensi

```bash
pip install -r requirements.txt
```

---

## 4. Verifikasi Python

```bash
python --version
```

Output yang direkomendasikan:

```text
Python 3.10+
```

---

# Cara Menjalankan

Pastikan berada pada root project:

```bash
python main.py
```

---

## Contoh Output Terminal

```text
==============================================================
  ALGORITMA GENETIKA — PENJADWALAN SHIFT KARYAWAN
==============================================================
  Populasi : 100    |  Generasi Maks : 300
  Pc       : 0.8    |  Pm             : 0.05
  Elitisme : 5 ind  |  Tournament k   : 3
==============================================================

Gen 1
Fitness Terbaik : 937.0
Fitness Rata-rata : 873.9

TERMINASI: Threshold fitness 99.0% tercapai

==============================================================
HASIL AKHIR
==============================================================
Fitness Terbaik : 992.0 / 1000 (99.2%)
Ditemukan pada Generasi : 27
Total Generasi : 27
Waktu Komputasi : 0.5011 detik
==============================================================
```

---

# Output Program

Setelah proses evolusi selesai, folder `results/` akan dibuat otomatis.

```text
results/
├── jadwal_terbaik.json
├── jadwal_terbaik.csv
└── konvergensi_ga.png
```

## Deskripsi Output

| File | Format | Keterangan |
|--------|--------|------------|
| konvergensi_ga.png | PNG | Grafik fitness terbaik dan rata-rata |
| jadwal_terbaik.json | JSON | Data jadwal terstruktur |
| jadwal_terbaik.csv | CSV | Jadwal siap dibuka di Excel / Google Sheets |

---

# Eksperimen Parameter

Seluruh parameter GA dapat diubah melalui file:

```python
# config.py

UKURAN_POPULASI = 100
GENERASI_MAKS = 300
PROB_CROSSOVER = 0.8
PROB_MUTASI = 0.05
```

Contoh variasi pengujian:

| Parameter | Nilai Uji |
|------------|------------|
| Populasi | 50, 100, 150, 200 |
| Generasi | 100, 200, 300, 500 |
| Pc | 0.6, 0.7, 0.8, 0.9 |
| Pm | 0.01, 0.05, 0.10 |

---

## Template Hasil Pengujian

| Populasi | Pc | Pm | Generasi | Fitness | Waktu |
|-----------|----|----|----------|----------|--------|
| 50 | 0.8 | 0.05 | - | - | - |
| 100 | 0.8 | 0.05 | 27 | 992 | 0.5011 |
| 150 | 0.8 | 0.05 | - | - | - |
| 200 | 0.8 | 0.05 | - | - | - |

---

# Cara Kerja Algoritma

## Representasi Kromosom

Satu kromosom mewakili satu jadwal kerja selama 7 hari untuk 12 karyawan.

Ukuran kromosom:

```text
12 x 7
```

Contoh:

```text
        Sen Sel Rab Kam Jum Sab Min
Kar01   2   0   1   0   0   3   2
Kar02   1   0   1   1   0   3   0
...
Kar12   1   1   0   0   3   0   1
```

Keterangan:

| Kode | Shift |
|--------|--------|
| 0 | Libur |
| 1 | Pagi (06.00–14.00) |
| 2 | Siang (14.00–22.00) |
| 3 | Malam (22.00–06.00) |

---

## Fungsi Fitness

Fitness dihitung menggunakan pendekatan penalti:

```math
f(x) = 1000 - \sum (w_i \times p_i)
```

### Hard Constraint

| Constraint | Bobot |
|------------|--------|
| Minimal 2 staf per shift | 10 |
| Maksimal 6 hari kerja | 15 |
| Minimal 3 hari kerja | 8 |

### Soft Constraint

| Constraint | Bobot |
|------------|--------|
| Distribusi shift merata | 3 |
| Preferensi shift terpenuhi | 2 |

---

## Alur Evolusi

```text
Inisialisasi Populasi
        ↓
Evaluasi Fitness
        ↓
Elitisme (Top 5%)
        ↓
Tournament Selection
        ↓
Two-Point Crossover
        ↓
Mutation
        ↓
Evaluasi Fitness Baru
        ↓
Cek Terminasi
```

---

## Kriteria Terminasi

Algoritma berhenti apabila salah satu kondisi berikut terpenuhi:

1. Generasi mencapai 300.
2. Tidak ada peningkatan fitness selama 50 generasi.
3. Fitness mencapai 99% dari nilai maksimum.

Pada eksperimen ini:

```text
Fitness = 992 / 1000 = 99.2%
```

Sehingga terminasi terjadi pada generasi ke-27.

---

# Kamus File

| File | Fungsi |
|--------|--------|
| config.py | Konfigurasi parameter GA |
| main.py | Entry point aplikasi |
| requirements.txt | Daftar dependensi |
| ga/population.py | Inisialisasi populasi |
| ga/fitness.py | Evaluasi fitness |
| ga/selection.py | Tournament selection & elitisme |
| ga/crossover.py | Two-point crossover |
| ga/mutation.py | Value-change mutation |
| ga/engine.py | Mesin utama algoritma |
| utils/reporter.py | Output terminal |
| utils/plotter.py | Grafik konvergensi |
| utils/exporter.py | Ekspor JSON & CSV |

---

# Struktur Folder

```text
ga_shift_scheduling/
│
├── config.py
├── main.py
├── requirements.txt
├── .gitignore
│
├── ga/
│   ├── __init__.py
│   ├── population.py
│   ├── fitness.py
│   ├── selection.py
│   ├── crossover.py
│   ├── mutation.py
│   └── engine.py
│
├── utils/
│   ├── __init__.py
│   ├── reporter.py
│   ├── plotter.py
│   └── exporter.py
│
└── results/
    ├── jadwal_terbaik.json
    ├── jadwal_terbaik.csv
    └── konvergensi_ga.png
```

---

# Dependensi

```text
numpy>=1.26.0
matplotlib>=3.8.0
tabulate>=0.9.0
pytest>=8.0.0
pytest-cov>=5.0.0
```

Install seluruh dependensi dengan:

```bash
pip install -r requirements.txt
```

---

# Tentang Proyek

Proyek ini dibuat untuk memenuhi tugas implementasi **Algoritma Genetika (Genetic Algorithm)** pada kasus optimasi penjadwalan shift karyawan minimarket 24 jam.

Metode yang digunakan:

- Tournament Selection
- Elitism
- Two-Point Crossover
- Value-Change Mutation
- Fitness Penalty Function

Dengan konfigurasi terbaik yang diuji, algoritma berhasil memperoleh:

```text
Fitness = 992 / 1000 (99.2%)
```

dalam **27 generasi** dengan waktu komputasi sekitar **0.5 detik**.
