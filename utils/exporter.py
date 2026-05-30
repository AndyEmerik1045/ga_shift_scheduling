import json
import csv
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from config import NAMA_HARI, NAMA_KARYAWAN, JUMLAH_HARI, SHIFT_LABEL


def ke_dict(kromosom, fitness, meta=None):
    jadwal = []
    for k, nama in enumerate(NAMA_KARYAWAN):
        hari_data = []
        jml_kerja = 0
        for hari in range(JUMLAH_HARI):
            s = kromosom[k][hari]
            hari_data.append({
                "hari"        : NAMA_HARI[hari],
                "kode_shift"  : s,
                "label_shift" : SHIFT_LABEL[s],
            })
            if s != 0:
                jml_kerja += 1
        jadwal.append({
            "karyawan"  : nama,
            "jml_kerja" : jml_kerja,
            "hari"      : hari_data,
        })
    return {"fitness": fitness, "meta": meta or {}, "jadwal": jadwal}


def simpan_json(kromosom, fitness, path="results/jadwal_terbaik.json", meta=None):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    data = ke_dict(kromosom, fitness, meta)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  Jadwal disimpan (JSON) : {path}")
    return path


def simpan_csv(kromosom, fitness, path="results/jadwal_terbaik.csv"):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Karyawan"] + NAMA_HARI + ["Jml_Kerja", "Fitness"])
        for k, nama in enumerate(NAMA_KARYAWAN):
            row       = [nama]
            jml_kerja = 0
            for hari in range(JUMLAH_HARI):
                s = kromosom[k][hari]
                row.append(SHIFT_LABEL.get(s, "?"))
                if s != 0:
                    jml_kerja += 1
            row.extend([jml_kerja, f"{fitness:.1f}"])
            writer.writerow(row)
    print(f"  Jadwal disimpan (CSV)  : {path}")
    return path
