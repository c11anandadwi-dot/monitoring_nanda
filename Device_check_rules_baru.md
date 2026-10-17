# Device Check Rules

## 1. Tujuan

Device Check Rules digunakan untuk menentukan aturan
pemeriksaan perangkat jaringan pada Monitoring Engine.

Pemeriksaan dilakukan menggunakan metode Ping untuk
mengetahui apakah perangkat dapat dijangkau melalui jaringan.

## 2. Metode Pemeriksaan

Metode pemeriksaan yang digunakan adalah **ICMP Ping dengan mekanisme retry**.
Setiap perangkat diperiksa berdasarkan IP address yang terdaftar dalam konfigurasi
Monitoring Engine.
Program melakukan ping minimal 3x percobaan sebelum menetapkan status perangkat.
## 3. Aturan Pemeriksaan

### DCR-01: Mekanisme Pengecekan Konektivitas
- Program mengirim permintaan Ping ke device target.
- Setiap pengecekan dilakukan **minimal 3x percobaan (retry)** dengan jeda 2 detik antar percobaan.
- Device dinyatakan **ONLINE** jika minimal 1 dari 3 percobaan mendapat balasan.
- Device dinyatakan **OFFLINE** hanya jika **seluruh 3 percobaan gagal**.
- Tujuan: menghindari false alarm akibat packet loss sesaat. 

### DCR-02: Status ONLINE

Perangkat diberi status ONLINE apabila perintah Ping
mendapatkan balasan yang valid.

### DCR-03: Status OFFLINE

Perangkat diberi status OFFLINE apabila pemeriksaan Ping
tidak mendapatkan balasan yang valid atau melewati
batas waktu pemeriksaan.

Status OFFLINE berarti perangkat tidak merespons Ping.
Hal ini tidak selalu berarti perangkat benar-benar mati.

### DCR-04: Status ERROR

Program memberi status ERROR apabila terjadi kesalahan
lain ketika pemeriksaan perangkat dijalankan.

### DCR-05: Response Time

Program mencatat durasi proses pemeriksaan dalam
milidetik apabila perangkat memberikan balasan.

Nilai ini merupakan durasi proses Ping yang diukur
oleh program, bukan pengukuran waktu jaringan yang
sepenuhnya akurat.

### DCR-06: Penyimpanan Hasil

Hasil pemeriksaan disimpan ke file monitoring_logs.csv.

Informasi yang dicatat meliputi:
- Timestamp
- Nama perangkat
- IP address
- Status
- Response time jika tersedia

## 4. Kriteria Pengujian

Pengujian dinyatakan sesuai apabila:

1. Program dapat menjalankan pemeriksaan Ping.
2. Program menentukan status berdasarkan hasil pemeriksaan.
3. Program menangani timeout dan kesalahan.
4. Program menyimpan hasil pemeriksaan ke file CSV.

Hasil pengujian harus dicatat berdasarkan hasil
yang benar-benar muncul ketika program dijalankan.

## 5. Batasan

Pemeriksaan menggunakan Ping hanya menunjukkan apakah
perangkat memberikan respons terhadap pemeriksaan tersebut.

Perangkat yang memblokir ICMP dapat tidak merespons
meskipun perangkat masih aktif. 