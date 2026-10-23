# Kalkulator BMI Indonesia — Desktop Application (Windows)

Aplikasi desktop GUI untuk menghitung Indeks Massa Tubuh (IMT / BMI) dan rentang berat badan ideal untuk penduduk dewasa berdasarkan standar resmi **Kementerian Kesehatan Republik Indonesia (Survei Kesehatan Indonesia - SKI 2023)**.

Aplikasi ini dikembangkan untuk keperluan tugas praktikum mata kuliah **Arsitektur dan Karakteristik Platform Desktop**, dengan fokus pada antarmuka modern, pemisahan arsitektur logika dan GUI, validasi input yang andal, pengujian otomatis, serta distribusi standalone executable (.EXE).

---

## 1. Tujuan Aplikasi

1. **Edukasi & Skrining Mandiri**: Membantu pengguna dewasa (> 18 tahun) mengetahui status gizi serta indeks massa tubuh secara cepat dan akurat.
2. **Kesesuaian Standar Lokal**: Mengimplementasikan klasifikasi batas IMT khusus populasi Indonesia menurut Kemenkes RI (SKI 2023), bukan standar internasional/WHO yang kurang sesuai dengan karakteristik epidemiologi Asia.
3. **Studi Karakteristik Desktop**: Mendemonstrasikan bagaimana aplikasi desktop modern berjalan mandiri secara offline, efisien dalam penggunaan sumber daya, serta dapat didistribusikan tanpa dependensi runtime pihak ketiga.

---

## 2. Fitur Utama

- **Input Sederhana & Intuitif**: Masukan berat badan (kg) dan tinggi badan (cm) dengan satuan di sisi kanan serta placeholder pemandu.
- **Validasi Input Real-Time**:
  - Penolakan input kosong atau non-numerik.
  - Penolakan nilai 0 atau negatif.
  - Pembatasan rentang fisiologis wajar (Berat: 1 - 350 kg, Tinggi: 30 - 260 cm).
  - Pesan error deskriptif dalam Bahasa Indonesia tepat di bawah kolom input dengan perubahan visual border merah.
- **Hasil Indeks Presisi**:
  - Tampilan angka IMT dengan dua desimal (contoh: `16.53 kg/m²`).
  - Badge kategori berwarna informatif (Sangat Kurus, Normal / Ideal, Gemuk Ringan, Obesitas).
  - Penjelasan edukatif dan saran pola hidup sehat sesuai kategori hasil.
- **Rentang Berat Badan Ideal**: Menghitung estimasi batas bawah dan atas berat badan normal (IMT 18.5 – 25.0) yang sesuai dengan tinggi badan pengguna.
- **Tabel Batas Kategori Interaktif**: Accordion klik ("Lihat Batas Kategori Kemenkes") untuk menampilkan atau menyembunyikan tabel acuan resmi Kemenkes RI.
- **Tombol Reset**: Mengembalikan form input, menyembunyikan hasil, dan menghapus seluruh status error.
- **Responsif & Mandiri**: Dilengkapi scrollbar vertikal dan dukungan mousewheel sehingga nyaman digunakan di berbagai resolusi layar desktop.

---

## 3. Teknologi yang Digunakan

| Komponen | Teknologi | Keterangan |
| :--- | :--- | :--- |
| **Bahasa Pemrograman** | Python 3.15+ | Bahasa utama pengembangan |
| **GUI Framework** | Tkinter & ttk | Modul bawaan (Standard Library) Python, ringan & native |
| **Testing** | unittest | Framework pengujian unit bawaan Python |
| **Packaging / Build** | PyInstaller 6.x | Mengemas aplikasi menjadi file tunggal `.exe` mandiri |
| **Target Platform** | Windows 10 & 11 (64-bit) | Tidak memerlukan instalasi Python di PC klien |

---

## 4. Rumus Perhitungan & Batas Kategori

### 4.1 Rumus Indeks Massa Tubuh (IMT / BMI)
$$\text{IMT} = \frac{\text{Berat Badan (kg)}}{(\text{Tinggi Badan (m)})^2}$$
*Catatan: Tinggi badan dalam sentimeter (cm) dikonversi ke meter (m) terlebih dahulu sebelum dikuadratkan.*

**Contoh Kasus:**
- Berat: $45\text{ kg}$
- Tinggi: $165\text{ cm} = 1.65\text{ m}$
- $\text{IMT} = \frac{45}{1.65^2} = \frac{45}{2.7225} \approx 16.5289 \rightarrow \mathbf{16.53\text{ kg/m}^2}$
- Kategori: **Berat badan kurang (wasting)**

### 4.2 Batas Kategori Kemenkes RI (SKI 2023)
Berdasarkan Survei Kesehatan Indonesia (SKI) 2023 Kementerian Kesehatan RI untuk penduduk dewasa:

| Kategori Status Gizi | Batas IMT | Badge / Warna UI | Rekomendasi |
| :--- | :---: | :---: | :--- |
| **Berat badan kurang (wasting)** | $< 18.5$ | Biru (`#0284C7`) | Peningkatan asupan padat gizi seimbang |
| **Normal** | $18.5 – 24.9$ | Hijau (`#16A34A`) | Pertahankan pola gizi seimbang & olahraga |
| **Berat badan lebih (overweight)** | $25.0 – 26.9$ | Oranye (`#EA580C`) | Batasi gula, garam, lemak & tingkatkan aktivitas |
| **Obesitas** | $\ge 27.0$ | Merah (`#DC2626`) | Konsultasi medis / ahli gizi untuk tata laksana |

### 4.3 Rumus Rentang Berat Badan Normal / Ideal
Dihitung berdasarkan batas bawah IMT normal ($18.5$) dan batas atas normal ($25.0$):
$$\text{Batas Berat Bawah} = 18.5 \times (\text{Tinggi (m)})^2$$
$$\text{Batas Berat Atas} = 25.0 \times (\text{Tinggi (m)})^2$$

Contoh tinggi 165 cm ($1.65\text{ m}$):
- Bawah: $18.5 \times 2.7225 \approx \mathbf{50.4\text{ kg}}$
- Atas: $25.0 \times 2.7225 \approx \mathbf{68.1\text{ kg}}$
- Rentang: **50.4 kg – 68.1 kg**

---

## 5. Struktur Folder Proyek

```text
BMI-Calculator-Desktop/
├── main.py              # Entry point GUI desktop Tkinter
├── bmi_logic.py         # Modul murni logika bisnis, rumus, dan validasi
├── tests/
│   └── test_bmi.py      # Pengujian unit otomatis (unittest)
├── assets/
│   └── icon.ico         # Ikon aplikasi desktop
├── dist/
│   └── BMI-Calculator.exe # File executable hasil build
├── requirements.txt     # Daftar pustaka (PyInstaller)
├── .gitignore           # Konfigurasi pengabaian Git
└── README.md            # Dokumentasi lengkap proyek
```

---

## 6. Cara Menjalankan Source Code

### Prasyarat
- Komputer dengan sistem operasi Windows 10/11.
- Python 3.10 ke atas terpasang di sistem.

### Langkah-langkah
1. Buka PowerShell atau Command Prompt pada direktori proyek:
   ```powershell
   cd c:\AntiGravity\BMI-Calculator-Desktop
   ```
2. Jalankan aplikasi langsung menggunakan Python:
   ```powershell
   python main.py
   ```
3. Jendela aplikasi akan terbuka dengan antarmuka grafis yang bersih dan siap digunakan.

---

## 7. Cara Menjalankan Pengujian Otomatis (Unit Test)

Pengujian mencakup pengujian perhitungan matematis, batas-batas kategori kritis ($18.5, 25.0, 27.0$), validasi input salah/kosong/negatif, serta fungsionalitas GUI (tombol Reset dan toggle tabel kategori).

Jalankan perintah berikut:
```powershell
python -m unittest tests/test_bmi.py -v
```

Hasil uji yang diharapkan:
```text
test_category_boundary_18_5 (tests.test_bmi.TestBMILogic) ... ok
test_category_boundary_25_0 (tests.test_bmi.TestBMILogic) ... ok
test_category_boundary_27_0 (tests.test_bmi.TestBMILogic) ... ok
test_empty_inputs (tests.test_bmi.TestBMILogic) ... ok
test_ideal_weight_range (tests.test_bmi.TestBMILogic) ... ok
test_non_numeric_inputs (tests.test_bmi.TestBMILogic) ... ok
test_normal_bmi_calculation (tests.test_bmi.TestBMILogic) ... ok
test_process_bmi_full_workflow (tests.test_bmi.TestBMILogic) ... ok
test_zero_and_negative_inputs (tests.test_bmi.TestBMILogic) ... ok
test_reset_button (tests.test_bmi.TestGUIComponents) ... ok
test_toggle_kategori_table (tests.test_bmi.TestGUIComponents) ... ok

----------------------------------------------------------------------
Ran 11 tests in 0.968s

OK
```

---

## 8. Cara Melakukan Build Ulang EXE

Jika Anda memodifikasi kode program dan ingin memperbarui file executable:

1. Pastikan PyInstaller terpasang:
   ```powershell
   pip install -r requirements.txt
   ```
2. Jalankan perintah kompilasi:
   ```powershell
   python -m PyInstaller --noconfirm --clean --onefile --windowed --name BMI-Calculator --icon assets/icon.ico --add-data "assets;assets" main.py
   ```
3. File executable baru akan otomatis dihasilkan di direktori:
   `dist/BMI-Calculator.exe`

---

## 9. Cara Menguji Aplikasi pada Komputer Windows Lain

1. **Salin File Executable**:
   - Ambil file `dist/BMI-Calculator.exe` (ukuran sekitar 12.6 MB).
   - Salin file tersebut ke flashdisk atau kirimkan via Google Drive / email ke PC target.
2. **Jalankan di PC Target**:
   - Di PC Windows 10 atau 11 lain, cukup klik ganda (double click) file `BMI-Calculator.exe`.
   - **Catatan Portabilitas**: Komputer tujuan **TIDAK memerlukan Python**, tidak memerlukan instalasi library tambahan, dan tidak memerlukan koneksi internet (berjalan 100% offline).
   - Aplikasi akan langsung terbuka tanpa memunculkan jendela command prompt/terminal hitam di latar belakang.
