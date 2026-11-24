# 🌿 BelanjaBijak — Verifikasi Klaim Greenwashing & Kemasan Produk Berbasis AI

Aplikasi web berbasis **Streamlit** dan **Google Gemini Multimodal Vision** untuk memindai label kemasan produk konsumen secara langsung—mendeteksi indikasi _greenwashing_, memverifikasi izin edar serta sertifikasi di Indonesia, menilai keterbukaan komposisi dan kode daur ulang kemasan, serta merekomendasikan alternatif lokal yang lebih ramah lingkungan.

---

## ✨ Fitur Utama

- **Pemindaian Kemasan End-to-End Multimodal Vision**  
  Membaca teks kecil pada kemasan, klaim pemasaran, ikon visual, nomor izin edar, hingga simbol daur ulang langsung dari foto unggahan maupun kamera perangkat tanpa _pipeline_ OCR/Regex manual yang rentan salah baca.
- **Audit Berbasis Rubrik Terukur (Skor 0–100)**  
  Penilaian dihitung secara konsisten dari 4 komponen objektif:
  1. **Kejujuran Klaim vs Bukti (0–40):** Membedakan produk konvensional yang jujur dari klaim hijau samar maupun _greenwashing_ aktif.
  2. **Legalitas & Sertifikasi (0–25):** Deteksi nomor izin edar **BPOM**, **KEMENKES RI PKD**, **SNI**, **Halal Indonesia (BPJPH)**, serta sertifikasi ekolabel resmi (_Ekolabel Indonesia, FSC, RSPO_).
  3. **Transparansi Bahan Aktif (0–20):** Evaluasi keterbukaan komposisi dan dampak lingkungan bahan aktif sesuai regulasi pelabelan Indonesia.
  4. **Material & Kode Daur Ulang Kemasan (0–15):** Identifikasi simbol resin plastik (`#1 PET` hingga `#7 OTHER`), kemasan guna ulang (_returnable_), maupun kemasan _multilayer_ sulit daur ulang.
- **Rekomendasi Alternatif Lokal Kondisional**  
  Menampilkan 2–3 saran produk alternatif lokal Indonesia lengkap dengan pratinjau foto kemasan (diambil secara paralel) khusus untuk produk dengan skor di bawah **75**.
- **Arsitektur Cepat & Auto-Fallback Model**  
  Menggunakan `gemini-3.5-flash-lite` sebagai model utama berlatensi rendah dengan cadangan otomatis (`gemini-3.6-flash`, `gemini-3.1-flash-lite`, `gemini-3.8-flash`) serta validasi skema terstruktur menggunakan **Pydantic**.

---

## 📊 Klasifikasi Vonis & Skor

| Rentang Skor | Status Keamanan              | Sub-Kategori                                                                       |  Rekomendasi Alternatif  |
| :----------: | :--------------------------- | :--------------------------------------------------------------------------------- | :----------------------: |
| **75 – 100** | **AMAN DARI GREENWASHING**   | _Ramah Lingkungan Terverifikasi_ (86–100) atau _Produk Konvensional Jujur_ (75–85) |    Tidak ditampilkan     |
| **50 – 74**  | **WASPADA KLAIM SAMAR**      | _Klaim Hijau Tanpa Bukti Cukup_                                                    | Ditampilkan (2–3 produk) |
|  **0 – 49**  | **TERINDIKASI GREENWASHING** | _Greenwashing Aktif_                                                               | Ditampilkan (2–3 produk) |

---

## 📁 Struktur Proyek

```text
BelanjaBijak_FullAI_v2/
├── .streamlit/
│   ├── config.toml          # Konfigurasi tema & server Streamlit
│   └── secrets.toml         # Penyimpanan lokal GEMINI_API_KEY (diabaikan Git)
├── src/
│   ├── ai_service.py        # Integrasi Gemini API, optimasi latensi & auto-fallback
│   ├── image_utils.py       # Pra-pemrosesan gambar (EXIF/resize) & fetch gambar paralel
│   ├── prompts.py           # System instruction & rubrik audit greenwashing
│   ├── schemas.py           # Skema Pydantic & kalkulasi skor deterministik
│   └── styles.py            # Komponen antarmuka HTML/CSS kustom
├── app.py                   # Entry point utama aplikasi Streamlit
├── requirements.txt         # Daftar dependensi Python
└── README.md                # Dokumentasi proyek
```

---

## 🚀 Cara Menjalankan di Komputer Lokal

### 1. Kloning atau Ekstrak Proyek

Buka terminal di dalam direktori proyek `BelanjaBijak_FullAI_v2`:

```bash
git clone [https://github.com/abdullahumairr/belanja-bijak.git](https://github.com/abdullahumairr/belanja-bijak.git)
cd belanja-bijak
```

### 2. Buat Virtual Environment & Install Dependensi

```bash
python -m venv venv
# Windows (Git Bash / PowerShell):
source venv/Scripts/activate
# macOS / Linux:
# source venv/bin/activate

pip install -r requirements.txt
```

### 3. Konfigurasi Gemini API Key

Dapatkan API key gratis melalui [Google AI Studio](https://aistudio.google.com/), lalu pilih salah satu cara berikut:

- **Cara A — File Secrets Lokal (Direkomendasikan):**  
  Buat file `.streamlit/secrets.toml` dan isi dengan:
  ```toml
  GEMINI_API_KEY = "AIzaSy..."
  ```
- **Cara B — Input Langsung di Aplikasi:**  
  Buka panel sidebar kiri saat aplikasi berjalan dan tempelkan kunci API pada kolom **Kunci API Layanan**.

### 4. Jalankan Aplikasi

```bash
streamlit run app.py
```

Aplikasi akan terbuka otomatis di browser pada alamat `http://localhost:8501`.

---

## 🔒 Catatan Keamanan

Pastikan file `.streamlit/secrets.toml` selalu terdaftar di dalam `.gitignore` agar kunci API tidak ikut terunggah ke repositori publik. Untuk _deployment_ di **Streamlit Community Cloud**, masukkan `GEMINI_API_KEY` melalui menu **App Settings → Secrets**.
