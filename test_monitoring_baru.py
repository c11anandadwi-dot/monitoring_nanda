"""
==================================================
 NETWORK MONITORING TEST
 T-AIMS - Teknolab Asset & Infrastructure Monitoring System
 Penguji: Ananda Dwi Susanti
==================================================
File ini menguji fungsi check_device() dari monitoring_engine.py
untuk 5 skenario pengujian.
==================================================
"""

from datetime import datetime
from monitoring_engine import check_device


# ==========================================
# DAFTAR SKENARIO PENGUJIAN
# ==========================================
TEST_CASES = [
    {
        "no": 1,
        "nama": "Device ONLINE Normal",
        "target": "192.168.0.1",
        "expected": "ONLINE",
        "deskripsi": "Ping gateway yang aktif -> harus ONLINE"
    },
    {
        "no": 2,
        "nama": "Device OFFLINE",
        "target": "192.168.1.99",
        "expected": "OFFLINE",
        "deskripsi": "Ping IP kosong -> harus OFFLINE setelah retry"
    },
    {
        "no": 3,
        "nama": "Retry Logic",
        "target": "192.168.1.99",
        "expected": "OFFLINE",
        "deskripsi": "Cek apakah muncul Percobaan 1, 2, 3 di terminal"
    },
    {
        "no": 4,
        "nama": "Timeout Handling",
        "target": "10.255.255.1",
        "expected": "OFFLINE",
        "deskripsi": "Ping IP tidak dikenal -> timeout -> OFFLINE"
    },
    {
        "no": 5,
        "nama": "Public DNS Online",
        "target": "8.8.8.8",
        "expected": "ONLINE",
        "deskripsi": "Ping DNS publik -> harus ONLINE dengan response time"
    },
]


# ==========================================
# FUNGSI JALANKAN SATU TEST
# ==========================================
def jalankan_test(case):
    print("\n" + "=" * 60)
    print(f"[TEST {case['no']}] {case['nama']}")
    print("=" * 60)
    print(f"Deskripsi : {case['deskripsi']}")
    print(f"Target    : {case['target']}")
    print(f"Expected  : {case['expected']}")
    print("-" * 60)
    print("Output dari check_device():")
    print("-" * 60)

    status, response_time_ms = check_device(case["target"])

    print("-" * 60)
    print(f"Actual    : {status}")
    if response_time_ms is not None:
        print(f"Response  : {response_time_ms} ms")
    else:
        print(f"Response  : -")

    if status == case["expected"]:
        hasil = "PASS"
    else:
        hasil = "FAIL"

    print(f"Hasil     : {hasil}")

    return {
        "no": case["no"],
        "nama": case["nama"],
        "target": case["target"],
        "expected": case["expected"],
        "actual": status,
        "response_ms": response_time_ms,
        "hasil": hasil
    }


# ==========================================
# PROGRAM UTAMA
# ==========================================
def main():
    print("\n" + "#" * 60)
    print("#  NETWORK MONITORING TEST - T-AIMS")
    print("#  Penguji: Ananda Dwi Susanti")
    print("#" * 60)

    print(f"\nWaktu pengujian: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Jumlah skenario: {len(TEST_CASES)}")

    hasil_semua = []

    for case in TEST_CASES:
        hasil = jalankan_test(case)
        hasil_semua.append(hasil)

    # ==========================================
    # RINGKASAN HASIL
    # ==========================================
    print("\n\n" + "=" * 60)
    print("  RINGKASAN HASIL PENGUJIAN")
    print("=" * 60)
    print(f"{'No':<4} {'Nama Test':<28} {'Expected':<12} {'Actual':<12} {'Hasil'}")
    print("-" * 60)

    for h in hasil_semua:
        print(
            f"{h['no']:<4} "
            f"{h['nama']:<28} "
            f"{h['expected']:<12} "
            f"{h['actual']:<12} "
            f"{h['hasil']}"
        )

    total_pass = sum(1 for h in hasil_semua if h["hasil"] == "PASS")
    total = len(hasil_semua)

    print("-" * 60)
    print(f"TOTAL: {total_pass}/{total} PASS")
    print("=" * 60)

    if total_pass == total:
        print("SEMUA TEST BERHASIL!")
    else:
        print("Ada test yang belum lulus, cek kembali.")


if __name__ == "__main__":
    main() -