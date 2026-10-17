import csv
import os
from datetime import datetime

# ============================================
#   MONITORING HISTORY OTOMATIS
#   Mencatat setiap perubahan status perangkat
# ============================================

FILE_HISTORY = "history.csv"
INTERVAL_CEK = 10  # detik (ganti ke 60 untuk cek tiap 1 menit)

# Daftar perangkat yang dimonitor
# status awal: "UP" (anggap semua normal saat mulai)
perangkat_list = {
    "Server-01": "UP",
    "Router-01": "UP",
    "CCTV-01":   "UP",
    "Printer-01":"UP",
}

# Fungsi: baca status nyata perangkat
# GANTI bagian ini dengan pengecekan asli nanti
def cek_status(perangkat):
    # === SIMULASI ===
    # Di sini kamu bisa ganti dengan ping, API, atau sensor asli
    import random
    # 95% kemungkinan UP, 5% DOWN
    return "UP" if random.random() > 0.05 else "DOWN"

# Fungsi: pastikan file history ada + header
def siapkan_file():
    if not os.path.exists(FILE_HISTORY):
        with open(FILE_HISTORY, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                "Waktu", "Perangkat",
                "Status Lama", "Status Baru", "Keterangan"
            ])
        print(f"[INFO] File {FILE_HISTORY} dibuat.")
    else:
        print(f"[INFO] File {FILE_HISTORY} sudah ada.")

# Fungsi: catat perubahan ke CSV
def catat(perangkat, lama, baru, ket=""):
    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(FILE_HISTORY, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([waktu, perangkat, lama, baru, ket])
    print(f"[CATAT] {waktu} | {perangkat} | {lama} -> {baru} | {ket}")

# ============================================
#   PROGRAM UTAMA
# ============================================
print("=" * 60)
print("   MONITORING HISTORY OTOMATIS")
print("=" * 60)

siapkan_file()

print(f"\nMemantau {len(perangkat_list)} perangkat setiap {INTERVAL_CEK} detik...")
print("Tekan Ctrl+C untuk berhenti.\n")

try:
    while True:
        for nama, status_lama in list(perangkat_list.items()):
            status_baru = cek_status(nama)

            if status_baru != status_lama:
                # Status berubah! Catat.
                ket = "Perubahan terdeteksi otomatis"
                catat(nama, status_lama, status_baru, ket)
                perangkat_list[nama] = status_baru

        import time
        time.sleep(INTERVAL_CEK)

except KeyboardInterrupt:
    print("\n[STOP] Monitoring dihentikan.")
    print(f"[INFO] Semua histori tersimpan di {FILE_HISTORY}")