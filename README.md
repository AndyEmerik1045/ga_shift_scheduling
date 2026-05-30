# Optimasi Penjadwalan Shift Karyawan Minimarket 24 Jam
### Implementasi Algoritma Genetika — Python 3.12

> Studi kasus: Penjadwalan shift mingguan 12 karyawan minimarket 24 jam (Indomaret/Alfamart) menggunakan Algoritma Genetika dengan representasi kromosom integer, tournament selection, two-point crossover, dan value-change mutation.

---

## Daftar Isi

- [Hasil Algoritma](#hasil-algoritma)
- [Cara Setup (untuk yang clone)](#cara-setup-untuk-yang-clone)
- [Cara Menjalankan](#cara-menjalankan)
- [Eksperimen Parameter](#eksperimen-parameter)
- [Cara Kerja Algoritma](#cara-kerja-algoritma)
- [Kamus File](#kamus-file)
- [Struktur Folder](#struktur-folder)

---

## Hasil Algoritma

| Parameter | Nilai |
|---|---|
| Fitness terbaik | 990 / 1000 (99.0%) |
| Representasi kromosom | Integer — matriks 12×7 |
| Ukuran populasi | 100 individu |
| Probabilitas crossover (Pc) | 0.8 |
| Probabilitas mutasi (Pm) | 0.05 |
| Jumlah generasi maks | 300 |
| Kriteria terminasi | Kombinasi (konvergensi + threshold + generasi maks) |

---

## Cara Setup (untuk yang clone)

### Prasyarat

- Python 3.10 atau lebih baru
- Git

Cek versi Python:

```bash
python --version
# atau
python3 --version
```

### 1 — Clone repositori

```bash
git clone https://github.com/AndyEmerik1045/ga_shift_scheduling.git
cd ga_shift_scheduling
```

### 2 — Buat virtual environment (opsional, direkomendasikan)

```bash
# Buat venv
python -m venv venv

# Aktifkan — Windows (Command Prompt)
venv\Scripts\activate

# Aktifkan — Windows (PowerShell)
.\venv\Scripts\Activate.ps1

# Aktifkan — Mac / Linux
source venv/bin/activate
```

> Jika menggunakan GitHub Codespaces, lewati langkah ini — tidak perlu venv.

### 3 — Install dependensi

```bash
pip install -r requirements.txt
```

Library yang akan terinstal:

| Library | Versi minimal | Kegunaan |
|---|---|---|
| numpy | 1.26.0 | Komputasi numerik |
| matplotlib | 3.8.0 | Grafik konvergensi |
| tabulate | 0.9.0 | Tabel terminal |
| pytest | 8.0.0 | Unit testing |
| pytest-cov | 5.0.0 | Laporan coverage |

### 4 — Buat folder results

```bash
mkdir results
```

> Folder ini dibuat otomatis saat program dijalankan. Langkah ini hanya diperlukan jika folder belum ada.

---

## Cara Menjalankan

Pastikan berada di folder root proyek, lalu jalankan:

```bash
python main.py
```

### Contoh output terminal

```
==============================================================
  ALGORITMA GENETIKA — PENJADWALAN SHIFT KARYAWAN
==============================================================
  Populasi : 100   |  Generasi Maks : 300
  Pc       : 0.8   |  Pm             : 0.05
  Elitisme : 5 ind |  Tournament k   : 3
==============================================================
  Gen   1  |  Fitness Terbaik:  968.0  |  Rata-rata:  891.2  |  Tanpa Perbaikan: 0
  Gen  50  |  Fitness Terbaik:  990.0  |  Rata-rata:  942.7  |  Tanpa Perbaikan: 45
  ...
  TERMINASI: Konvergensi (50 gen tanpa perbaikan)

==============================================================
  HASIL AKHIR
==============================================================
  Fitness Terbaik  : 990.0 / 1000  (99.0%)
  Ditemukan di     : Generasi 3
  Total Generasi   : 53
  Alasan Berhenti  : Konvergensi (50 gen tanpa perbaikan)
  Waktu Komputasi  : 2.4821 detik
==============================================================
```

### Output yang dihasilkan

Setelah selesai, tiga file tersimpan di folder `results/`:

| File | Format | Isi |
|---|---|---|
| `konvergensi_ga.png` | Gambar PNG | Grafik fitness terbaik dan rata-rata per generasi |
| `jadwal_terbaik.json` | JSON | Data jadwal terstruktur, siap digunakan di API/frontend |
| `jadwal_terbaik.csv` | CSV | Tabel jadwal, langsung bisa dibuka di Excel/Google Sheets |

---

## Eksperimen Parameter

Untuk keperluan pengujian laporan, ubah nilai di `config.py` lalu jalankan ulang `python main.py`. Ubah **satu parameter per eksperimen** agar hasil bisa dibandingkan.

```python
# config.py — parameter yang bisa diubah untuk eksperimen

UKURAN_POPULASI = 100   # coba: 50, 100, 150, 200
GENERASI_MAKS   = 300   # coba: 100, 200, 300, 500
PROB_CROSSOVER  = 0.8   # coba: 0.6, 0.7, 0.8, 0.9
PROB_MUTASI     = 0.05  # coba: 0.01, 0.05, 0.10
```

### Tabel pengujian (template)

| Populasi | Pc | Pm | Generasi | Fitness Terbaik | Waktu (detik) | Alasan Berhenti |
|---|---|---|---|---|---|---|
| 50 | 0.8 | 0.05 | - | - | - | - |
| 100 | 0.8 | 0.05 | - | - | - | - |
| 150 | 0.8 | 0.05 | - | - | - | - |
| 200 | 0.8 | 0.05 | - | - | - | - |
| 100 | 0.6 | 0.05 | - | - | - | - |
| 100 | 0.7 | 0.05 | - | - | - | - |
| 100 | 0.9 | 0.05 | - | - | - | - |
| 100 | 0.8 | 0.01 | - | - | - | - |
| 100 | 0.8 | 0.10 | - | - | - | - |

---

## Cara Kerja Algoritma

### Representasi Kromosom

Satu kromosom merepresentasikan satu skenario jadwal kerja seluruh karyawan selama 7 hari. Kromosom berupa matriks integer berukuran **12 × 7**, di mana setiap elemen merupakan kode shift:

```
         Senin  Selasa  Rabu  Kamis  Jumat  Sabtu  Minggu
Kar. 01 [  2,     0,     1,    0,     0,     3,     2  ]
Kar. 02 [  1,     0,     1,    1,     0,     3,     0  ]
...
Kar. 12 [  1,     1,     0,    0,     3,     0,     1  ]

Kode: 0 = Libur | 1 = Pagi (06-14) | 2 = Siang (14-22) | 3 = Malam (22-06)
```

### Fungsi Fitness

Fitness dihitung dengan pendekatan berbasis penalti:

```
f(x) = 1000 - Σ(wᵢ × pᵢ)
```

| Constraint | Tipe | Bobot (w) | Penalti jika... |
|---|---|---|---|
| Minimum 2 staf per shift per hari | Hard | 10 | Kurang dari 2 staf di satu shift |
| Maks 6 hari kerja per minggu | Hard | 15 | Karyawan bekerja lebih dari 6 hari |
| Min 3 hari kerja per minggu | Hard | 8 | Karyawan bekerja kurang dari 3 hari |
| Distribusi shift merata | Soft | 3 | Selisih jumlah shift antar tipe terlalu besar |
| Preferensi shift karyawan | Soft | 2 | Shift preferensi tidak terpenuhi sama sekali |

### Alur Evolusi (per generasi)

```
Inisialisasi 100 kromosom acak
        ↓
Evaluasi fitness seluruh populasi
        ↓
Simpan 5 elite terbaik (elitisme 5%)
        ↓
Tournament selection (k=3) → pilih orang tua
        ↓
Two-point crossover (Pc = 0.8) → anak baru
        ↓
Value-change mutation (Pm = 0.05) → variasi
        ↓
Cek terminasi ──→ [Ya] → output jadwal terbaik
        ↓ [Tidak]
Kembali ke evaluasi fitness
```

### Kriteria Terminasi (kombinasi)

Algoritma berhenti jika **salah satu** kondisi terpenuhi:

1. Jumlah generasi mencapai **300**
2. Tidak ada peningkatan fitness selama **50 generasi** berturut-turut (konvergensi)
3. Fitness terbaik mencapai **99%** dari nilai maksimum (threshold)

---

## Kamus File

| File | Fungsi | Deskripsi |
|---|---|---|
| `config.py` | Pusat konfigurasi GA | Menyimpan semua konstanta dan parameter algoritma. Ubah nilai di sini untuk eksperimen tanpa menyentuh logika GA. |
| `main.py` | Entry point utama | Mengintegrasikan seluruh modul — menjalankan GA, mencetak hasil ke terminal, menyimpan grafik dan file output. |
| `requirements.txt` | Daftar dependensi | Daftar library Python yang dibutuhkan beserta versi minimalnya. |
| `ga/__init__.py` | Penanda package | File kosong yang menandai folder `ga/` sebagai Python package agar bisa diimport. |
| `ga/population.py` | Inisialisasi populasi | Membuat 100 kromosom acak berukuran 12×7. Setiap karyawan mendapat 3–6 hari kerja dengan shift dipilih secara acak. |
| `ga/fitness.py` | Evaluasi kromosom | Menghitung nilai fitness setiap kromosom menggunakan fungsi penalti berdasarkan 3 hard constraint dan 2 soft constraint. |
| `ga/selection.py` | Seleksi orang tua | Mengimplementasikan tournament selection (k=3) untuk memilih orang tua dan elitisme 5% untuk mempertahankan individu terbaik. |
| `ga/crossover.py` | Rekombinasi genetik | Melakukan two-point crossover antar dua kromosom orang tua dengan probabilitas Pc=0.8 untuk menghasilkan dua kromosom anak. |
| `ga/mutation.py` | Mutasi gen | Menerapkan value-change mutation pada setiap gen dengan probabilitas Pm=0.05, mengganti nilai shift dengan nilai acak yang valid. |
| `ga/engine.py` | Mesin utama GA | Mengintegrasikan semua operator dan menjalankan loop evolusi hingga kriteria terminasi terpenuhi. Mengembalikan hasil lengkap sebagai dictionary. |
| `utils/__init__.py` | Penanda package | File kosong yang menandai folder `utils/` sebagai Python package. |
| `utils/reporter.py` | Tampilan terminal | Mencetak tabel jadwal shift, rekap jumlah staf per shift per hari, dan ringkasan statistik eksekusi GA ke terminal. |
| `utils/plotter.py` | Grafik konvergensi | Membuat dan menyimpan grafik perbandingan fitness terbaik dan rata-rata per generasi sebagai file PNG menggunakan Matplotlib. |
| `utils/exporter.py` | Ekspor hasil | Menyimpan jadwal terbaik ke dalam dua format: JSON (terstruktur, siap API) dan CSV (tabel, siap Excel). |

---

## Struktur Folder

```
ga_shift_scheduling/
│
├── config.py              ← parameter GA, ubah di sini untuk eksperimen
├── main.py                ← entry point, jalankan: python main.py
├── requirements.txt       ← pip install -r requirements.txt
├── .gitignore
│
├── ga/                    ← logika inti algoritma genetika
│   ├── __init__.py
│   ├── population.py      ← inisialisasi 100 kromosom acak (12×7)
│   ├── fitness.py         ← f(x) = 1000 − Σpenalti
│   ├── selection.py       ← tournament k=3 + elitisme 5%
│   ├── crossover.py       ← two-point crossover (Pc=0.8)
│   ├── mutation.py        ← value-change mutation (Pm=0.05)
│   └── engine.py          ← loop evolusi + kriteria terminasi
│
├── utils/                 ← output, visualisasi, ekspor
│   ├── __init__.py
│   ├── reporter.py        ← tabel jadwal di terminal
│   ├── plotter.py         ← grafik konvergensi PNG
│   └── exporter.py        ← ekspor JSON dan CSV
│
└── results/               ← output program (auto-dibuat saat run)
    ├── jadwal_terbaik.json
    ├── jadwal_terbaik.csv
    └── konvergensi_ga.png
```

---

## Dependensi

```
numpy>=1.26.0
matplotlib>=3.8.0
tabulate>=0.9.0
pytest>=8.0.0
pytest-cov>=5.0.0
```

---

*Dibuat untuk keperluan tugas implementasi Algoritma Genetika — Optimasi Penjadwalan Shift Karyawan Minimarket 24 Jam.*
