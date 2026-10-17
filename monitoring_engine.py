import subprocess
import time
import csv
import os
from datetime import datetime

# ==========================================
# KONFIGURASI MONITORING ENGINE
# ==========================================

# Daftar 9 perangkat menggunakan IP dummy.
# IP ini belum merupakan hasil survei fisik.
DEVICES = {
    "Router 1 (DUMMY)": "192.168.1.1",
    "Router 2 (DUMMY)": "192.168.1.2",
    "Router 3 (DUMMY)": "192.168.1.3",
    "PC Kantor (DUMMY)": "192.168.1.10",
    "TV (DUMMY)": "192.168.1.20",
    "CCTV (DUMMY)": "192.168.1.30",
    "Server (DUMMY)": "192.168.1.40",
    "Access Point (DUMMY)": "192.168.1.50",
    "Printer Jaringan (DUMMY)": "192.168.1.60",
}

# Jeda sebelum pemeriksaan berikutnya (detik)
INTERVAL = 10

# Nama file untuk menyimpan hasil monitoring
LOG_FILE = "monitoring_logs.csv"


# ==========================================
# FUNGSI PING
# ==========================================

def check_device(ip):
    start_time = time.perf_counter()

    try:
        result = subprocess.run(
            ["ping", "-n", "1", "-w", "2000", ip],
            capture_output=True,
            text=True,
            timeout=4
        )

        elapsed_ms = round(
            (time.perf_counter() - start_time) * 1000,
            2
        )

        # Di Windows, balasan ping biasanya memuat TTL=
        if result.returncode == 0 and "TTL=" in result.stdout.upper():
            status = "ONLINE"
            response_time_ms = elapsed_ms
        else:
            status = "OFFLINE"
            response_time_ms = None

    except subprocess.TimeoutExpired:
        status = "OFFLINE"
        response_time_ms = None

    except Exception as error:
        status = "ERROR"
        response_time_ms = None
        print(f"Kesalahan saat memeriksa {ip}: {error}")

    return status, response_time_ms


# ==========================================
# FUNGSI MENYIMPAN LOG
# ==========================================

def save_log(timestamp, device_name, ip, status, response_time_ms):
    file_exists = os.path.exists(LOG_FILE)

    with open(LOG_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        # Buat header hanya ketika file belum ada
        if not file_exists or os.path.getsize(LOG_FILE) == 0:
            writer.writerow([
                "timestamp",
                "device_name",
                "ip_address",
                "status",
                "response_time_ms"
            ])

        writer.writerow([
            timestamp,
            device_name,
            ip,
            status,
            response_time_ms if response_time_ms is not None else ""
        ])


# ==========================================
# PROGRAM UTAMA
# ==========================================

def main():
    print("=" * 65)
    print("       NETWORK & DEVICE MONITORING ENGINE")
    print("=" * 65)
    print("Tekan CTRL + C untuk menghentikan monitoring.\n")

    try:
        while True:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            print(f"\nWaktu pemeriksaan: {timestamp}")
            print("-" * 65)
            print(f"{'NAMA PERANGKAT':25} {'IP ADDRESS':18} {'STATUS':10} {'RESPONSE'}")
            print("-" * 65)

            for device_name, ip in DEVICES.items():
                status, response_time_ms = check_device(ip)

                if response_time_ms is not None:
                    response = f"{response_time_ms} ms"
                else:
                    response = "-"

                print(
                    f"{device_name:25} "
                    f"{ip:18} "
                    f"{status:10} "
                    f"{response}"
                )

                save_log(
                    timestamp,
                    device_name,
                    ip,
                    status,
                    response_time_ms
                )

            print("-" * 65)
            print(f"Log tersimpan di: {os.path.abspath(LOG_FILE)}")
            print(f"Pemeriksaan berikutnya dalam {INTERVAL} detik.")

            time.sleep(INTERVAL)

    except KeyboardInterrupt:
        print("\nMonitoring dihentikan oleh pengguna.")
        print("Data hasil pemeriksaan tetap tersimpan di file log.")


if __name__ == "__main__":
    main()