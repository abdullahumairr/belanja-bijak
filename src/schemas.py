from typing import List, Literal
from pydantic import BaseModel, Field


class AuditKlaimItem(BaseModel):
    teks_atau_visual_klaim: str = Field(
        description="Klaim teks atau elemen visual pada kemasan yang diaudit."
    )
    status_klaim: Literal["Terbukti", "Klaim Samar", "Menyesatkan"] = Field(
        description="Penilaian kejujuran klaim berdasarkan bukti nyata di kemasan."
    )
    penjelasan_bukti: str = Field(
        description="Alasan singkat 1-2 kalimat berdasarkan sertifikasi, bahan aktif, atau kode kemasan."
    )


class BuktiPendukung(BaseModel):
    sertifikasi_ekolabel: str = Field(
        description="Sertifikasi lingkungan pihak ketiga (misal: 'Tidak tercantum ekolabel' atau 'FSC / Ekolabel Indonesia')."
    )
    izin_edar_dan_halal: str = Field(
        description="Nomor izin edar resmi (KEMENKES PKD / BPOM / SNI) dan status Halal."
    )
    bahan_aktif_utama: str = Field(
        description="Bahan aktif utama yang tercantum beserta catatan dampaknya secara ringkas."
    )
    kode_kemasan: str = Field(
        description="Kode daur ulang plastik (misal: '1 - PET' atau '7 - OTHER') dan evaluasi daur ulangnya."
    )


class ProdukAlternatif(BaseModel):
    nama_produk: str = Field(
        description="Nama merek & produk alternatif lokal Indonesia yang lebih ramah lingkungan."
    )
    kata_kunci_gambar: str = Field(
        description="Kata kunci pencarian foto kemasan produk yang spesifik tanpa tanda kurung."
    )
    keunggulan_lingkungan: str = Field(
        description="Mengapa formula produk ini lebih ramah lingkungan dibanding produk yang dipindai."
    )
    jenis_kemasan: str = Field(
        description="Keunggulan kemasan produk alternatif (misal: botol HDPE daur ulang, jerigen isi ulang)."
    )


class AuditGreenwashing(BaseModel):
    nama_produk: str = Field(
        description="Nama singkat produk, merek, dan ukuran netto."
    )
    status_keamanan: Literal[
        "AMAN DARI GREENWASHING",
        "WASPADA KLAIM SAMAR",
        "TERINDIKASI GREENWASHING",
    ] = Field(
        description="Vonis utama apakah produk aman dari praktik greenwashing atau tidak."
    )
    sub_kategori: Literal[
        "Ramah Lingkungan Terverifikasi",
        "Produk Konvensional Jujur",
        "Klaim Hijau Tanpa Bukti Cukup",
        "Greenwashing Aktif",
    ] = Field(
        description="Klasifikasi spesifik posisi produk."
    )
    skor_kejujuran_hijau: int = Field(
        ge=0,
        le=100,
        description="Skor kejujuran & keamanan dari greenwashing (0-100).",
    )
    kesimpulan_utama: str = Field(
        description="Penjelasan tegas 2 kalimat yang langsung menjawab apakah produk ini menyesatkan dengan klaim hijau atau tidak."
    )
    daftar_audit_klaim: List[AuditKlaimItem] = Field(
        description="Daftar 2-4 poin audit klaim teks maupun visual pada kemasan."
    )
    bukti_pendukung: BuktiPendukung
    saran_alternatif: List[ProdukAlternatif] = Field(
        description="Berikan 2-3 alternatif lokal yang terbukti ramah lingkungan jika produk belum terverifikasi ramah lingkungan. Kosongkan [] HANYA jika sub_kategori adalah 'Ramah Lingkungan Terverifikasi'."
    )