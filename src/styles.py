from src.schemas import AuditGreenwashing, AuditKlaimItem, BuktiPendukung, ProdukAlternatif

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@500;600&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
}
.stApp {
    background-color: #F6F7F5;
    color: #18181B;
}
[data-testid="stToolbar"] { visibility: hidden; }
footer { visibility: hidden; }
[data-testid="stHeader"] { background: transparent; }

[data-testid="stSidebar"] {
    background-color: #FFFFFF;
    border-right: 1px solid #E4E4E7;
}
[data-testid="stSidebar"] * { color: #18181B; }

.brand-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-bottom: 1.1rem;
    margin-bottom: 1.5rem;
    border-bottom: 1px solid #E4E4E7;
}
.brand-left {
    display: flex;
    align-items: center;
    gap: 0.75rem;
}
.brand-mark {
    width: 38px;
    height: 38px;
    border-radius: 10px;
    background-color: #1B4332;
    color: #FFFFFF;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 800;
    font-size: 1.05rem;
    letter-spacing: -0.03em;
}
.brand-name {
    font-size: 1.45rem;
    font-weight: 800;
    color: #18181B;
    letter-spacing: -0.02em;
    line-height: 1.1;
}
.brand-tagline {
    font-size: 0.88rem;
    color: #52525B;
    margin-top: 0.15rem;
}

.stButton > button[kind="primary"] {
    background-color: #1B4332;
    color: #FFFFFF;
    border: none;
    border-radius: 10px;
    padding: 0.65rem 1.2rem;
    font-weight: 600;
    font-size: 0.95rem;
}
.stButton > button[kind="primary"]:hover {
    background-color: #2D6A4F;
    color: #FFFFFF;
}

[data-testid="stFileUploader"] section {
    background-color: #FFFFFF;
    border: 1.5px dashed #D4D4D8;
    border-radius: 12px;
}

.verdict-card {
    background-color: #FFFFFF;
    border: 1px solid #E4E4E7;
    border-radius: 14px;
    padding: 1.4rem 1.5rem;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
    margin-bottom: 1.2rem;
}
.verdict-top {
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-bottom: 0.65rem;
}
.product-meta {
    font-size: 0.8rem;
    font-weight: 600;
    color: #71717A;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}
.status-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.3rem 0.75rem;
    border-radius: 999px;
    font-size: 0.78rem;
    font-weight: 700;
}
.pill-safe { background-color: #DCFCE7; color: #166534; border: 1px solid #BBF7D0; }
.pill-warn { background-color: #FEF3C7; color: #92400E; border: 1px solid #FDE68A; }
.pill-danger { background-color: #FEE2E2; color: #991B1B; border: 1px solid #FECACA; }

.product-heading {
    font-size: 1.35rem;
    font-weight: 700;
    color: #18181B;
    margin-bottom: 0.45rem;
    line-height: 1.3;
}
.verdict-summary {
    font-size: 0.94rem;
    color: #3F3F46;
    line-height: 1.55;
    margin-bottom: 1.1rem;
}

.score-row {
    background-color: #FAFAFA;
    border: 1px solid #F4F4F5;
    border-radius: 10px;
    padding: 0.8rem 1rem;
}
.score-header {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 0.45rem;
}
.score-label { font-size: 0.83rem; font-weight: 600; color: #52525B; }
.score-value {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1rem;
    font-weight: 600;
    color: #18181B;
}
.score-track {
    width: 100%;
    height: 8px;
    background-color: #E4E4E7;
    border-radius: 999px;
    overflow: hidden;
}
.score-fill { height: 100%; border-radius: 999px; }

.audit-item {
    background-color: #FFFFFF;
    border: 1px solid #E4E4E7;
    border-radius: 11px;
    padding: 0.95rem 1.15rem;
    margin-bottom: 0.65rem;
}
.audit-item-top {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 0.75rem;
    margin-bottom: 0.35rem;
}
.audit-claim-title { font-weight: 600; font-size: 0.94rem; color: #18181B; }
.audit-claim-desc { font-size: 0.88rem; color: #52525B; line-height: 1.5; }

.tag-jujur, .tag-samar, .tag-menyesatkan {
    white-space: nowrap;
    font-size: 0.75rem;
    font-weight: 600;
    padding: 0.18rem 0.6rem;
    border-radius: 6px;
}
.tag-jujur { background-color: #F0FDF4; color: #15803D; border: 1px solid #BBF7D0; }
.tag-samar { background-color: #FFFBEB; color: #B45309; border: 1px solid #FDE68A; }
.tag-menyesatkan { background-color: #FEF2F2; color: #B91C1C; border: 1px solid #FECACA; }

.evidence-grid {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 0.75rem;
}
@media (max-width: 768px) {
    .evidence-grid { grid-template-columns: 1fr; }
}
.evidence-box {
    background-color: #FFFFFF;
    border: 1px solid #E4E4E7;
    border-radius: 11px;
    padding: 0.95rem 1.05rem;
}
.evidence-title {
    font-size: 0.76rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    color: #71717A;
    margin-bottom: 0.35rem;
}
.evidence-text { font-size: 0.89rem; color: #27272A; line-height: 1.45; }

.alt-box {
    background-color: #FFFFFF;
    border: 1px solid #E4E4E7;
    border-radius: 11px;
    padding: 0.95rem 1.1rem;
    margin-bottom: 0.5rem;
}
.alt-name { font-weight: 700; font-size: 0.96rem; color: #1B4332; margin-bottom: 0.35rem; }
.alt-detail { font-size: 0.87rem; color: #3F3F46; line-height: 1.45; margin-bottom: 0.2rem; }

.img-fallback {
    background-color: #F4F4F5;
    border: 1px solid #E4E4E7;
    border-radius: 10px;
    height: 115px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #71717A;
    font-size: 0.78rem;
    font-weight: 500;
    text-align: center;
    padding: 0.5rem;
}

.stTabs [data-baseweb="tab-list"] { gap: 0.5rem; border-bottom: 1px solid #E4E4E7; }
.stTabs [data-baseweb="tab"] {
    font-weight: 600;
    font-size: 0.9rem;
    color: #52525B;
    padding-top: 0.5rem;
    padding-bottom: 0.6rem;
}
.stTabs [aria-selected="true"] { color: #1B4332 !important; }
</style>
"""


def brand_header_html() -> str:
    return """
    <div class="brand-bar">
        <div class="brand-left">
            <div class="brand-mark">BB</div>
            <div>
                <div class="brand-name">BelanjaBijak</div>
                <div class="brand-tagline">Verifikasi klaim ramah lingkungan, izin edar, dan kemasan produk sebelum membeli</div>
            </div>
        </div>
    </div>
    """


def ready_placeholder_html() -> str:
    return """
    <div class="verdict-card">
        <div class="product-meta">Siap Memeriksa</div>
        <div class="product-heading">Klik "Periksa Produk" di bawah foto</div>
        <div class="verdict-summary" style="margin-bottom:0;">
            Sistem akan mengevaluasi klaim pada label, mencocokkannya dengan izin edar serta komposisi, dan menampilkan rekomendasi alternatif jika diperlukan.
        </div>
    </div>
    """


def verdict_card_html(hasil: AuditGreenwashing) -> str:
    if hasil.status_keamanan == "AMAN DARI GREENWASHING":
        pill_cls, bar_color = "pill-safe", "#166534"
    elif hasil.status_keamanan == "WASPADA KLAIM SAMAR":
        pill_cls, bar_color = "pill-warn", "#D97706"
    else:
        pill_cls, bar_color = "pill-danger", "#DC2626"

    dot_svg = f'<svg width="10" height="10" viewBox="0 0 10 10"><circle cx="5" cy="5" r="5" fill="{bar_color}"/></svg>'
    skor = min(max(hasil.skor_kejujuran_hijau, 0), 100)

    return f"""
    <div class="verdict-card">
        <div class="verdict-top">
            <span class="product-meta">{hasil.sub_kategori}</span>
            <span class="status-pill {pill_cls}">{dot_svg} {hasil.status_keamanan}</span>
        </div>
        <div class="product-heading">{hasil.nama_produk}</div>
        <div class="verdict-summary">{hasil.kesimpulan_utama}</div>
        <div class="score-row">
            <div class="score-header">
                <span class="score-label">Indeks Kejujuran Klaim</span>
                <span class="score-value">{skor} / 100</span>
            </div>
            <div class="score-track">
                <div class="score-fill" style="width: {skor}%; background-color: {bar_color};"></div>
            </div>
        </div>
    </div>
    """


def claim_item_html(item: AuditKlaimItem) -> str:
    if item.status_klaim == "Terbukti":
        tag_cls = "tag-jujur"
    elif item.status_klaim == "Klaim Samar":
        tag_cls = "tag-samar"
    else:
        tag_cls = "tag-menyesatkan"

    return f"""
    <div class="audit-item">
        <div class="audit-item-top">
            <div class="audit-claim-title">{item.teks_atau_visual_klaim}</div>
            <span class="{tag_cls}">{item.status_klaim}</span>
        </div>
        <div class="audit-claim-desc">{item.penjelasan_bukti}</div>
    </div>
    """


def evidence_grid_html(bukti: BuktiPendukung) -> str:
    return f"""
    <div class="evidence-grid">
        <div class="evidence-box">
            <div class="evidence-title">Sertifikasi Ekolabel</div>
            <div class="evidence-text">{bukti.sertifikasi_ekolabel}</div>
        </div>
        <div class="evidence-box">
            <div class="evidence-title">Izin Edar & Halal</div>
            <div class="evidence-text">{bukti.izin_edar_dan_halal}</div>
        </div>
        <div class="evidence-box">
            <div class="evidence-title">Bahan Aktif Utama</div>
            <div class="evidence-text">{bukti.bahan_aktif_utama}</div>
        </div>
        <div class="evidence-box">
            <div class="evidence-title">Material & Kode Daur Ulang</div>
            <div class="evidence-text">{bukti.kode_kemasan}</div>
        </div>
    </div>
    """


def alternative_card_html(alt: ProdukAlternatif) -> str:
    return f"""
    <div class="alt-box">
        <div class="alt-name">{alt.nama_produk}</div>
        <div class="alt-detail"><strong>Keunggulan bahan:</strong> {alt.keunggulan_lingkungan}</div>
        <div class="alt-detail"><strong>Kemasan:</strong> {alt.jenis_kemasan}</div>
    </div>
    """