import hashlib
import io
import streamlit as st

from src.schemas import AuditGreenwashing
from src.ai_service import get_api_key, analyze_product_label
from src.image_utils import preprocess_image, fetch_product_image
from src.styles import (
    CUSTOM_CSS,
    brand_header_html,
    ready_placeholder_html,
    verdict_card_html,
    claim_item_html,
    evidence_grid_html,
    alternative_card_html,
)

# 1. Konfigurasi Halaman & Gaya Visual
st.set_page_config(
    page_title="BelanjaBijak — Verifikasi Klaim & Kemasan Produk",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed",
)
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# 2. Sidebar Pengaturan
with st.sidebar:
    st.subheader("Pengaturan Layanan")
    saved_key = get_api_key()

    if saved_key and "user_api_key" not in st.session_state:
        st.success("Kunci akses terhubung.")
    else:
        api_input = st.text_input(
            "Kunci API Layanan",
            type="password",
            placeholder="AIzaSy...",
        )
        if api_input:
            st.session_state["user_api_key"] = api_input.strip()

    st.markdown("---")
    st.markdown("**Panduan Kategori**")
    st.markdown(
        """
        - **Aman dari Greenwashing:** Klaim sesuai bukti atau produk konvensional tanpa klaim hijau palsu.
        - **Waspada Klaim Samar:** Menggunakan istilah atau nuansa hijau tanpa sertifikasi pendukung.
        - **Terindikasi Greenwashing:** Klaim ramah lingkungan menyesatkan yang bertentangan dengan komposisi atau kemasan.
        """
    )

# 3. Header Utama & Input Foto
st.markdown(brand_header_html(), unsafe_allow_html=True)

use_camera = st.toggle("Gunakan kamera perangkat", value=False)
if use_camera:
    image_source = st.camera_input("Ambil foto label kemasan")
else:
    image_source = st.file_uploader(
        "Unggah foto kemasan produk (bagian klaim, komposisi, atau kode daur ulang)",
        type=["jpg", "jpeg", "png", "webp"],
    )

# 4. Alur Pemindaian & Penampilan Hasil
if image_source is not None:
    file_bytes = image_source.getvalue()
    file_hash = hashlib.md5(file_bytes).hexdigest()
    if st.session_state.get("current_file_hash") != file_hash:
        st.session_state["current_file_hash"] = file_hash
        st.session_state.pop("last_result", None)

    active_api_key = get_api_key()
    col_img, col_res = st.columns([1, 1.6], gap="large")

    with col_img:
        processed_img = preprocess_image(io.BytesIO(file_bytes))
        st.image(processed_img, caption="Pratinjau kemasan", width="stretch")
        scan_btn = st.button("Periksa Produk", type="primary", width="stretch")

    with col_res:
        if not active_api_key:
            st.warning("Buka panel kiri (ikon panah di pojok kiri atas) untuk memasukkan kunci akses terlebih dahulu.")
        elif scan_btn:
            error_message = None
            with st.spinner("Memeriksa klaim kemasan dan sertifikasi..."):
                try:
                    st.session_state["last_result"] = analyze_product_label(active_api_key, processed_img)
                except Exception as e:
                    error_message = str(e)

            if error_message:
                st.error(error_message)
                st.stop()

        if "last_result" in st.session_state:
            hasil: AuditGreenwashing = st.session_state["last_result"]

            # Kartu Vonis Utama
            st.markdown(verdict_card_html(hasil), unsafe_allow_html=True)

            # Navigasi Tab Rincian
            alt_count = len(hasil.saran_alternatif)
            tab_alt_label = f"Alternatif Lebih Baik ({alt_count})" if alt_count > 0 else "Alternatif"
            tab1, tab2, tab3 = st.tabs(
                ["Audit Klaim Kemasan", "Sertifikasi & Kemasan", tab_alt_label]
            )

            with tab1:
                for item in hasil.daftar_audit_klaim:
                    st.markdown(claim_item_html(item), unsafe_allow_html=True)

            with tab2:
                st.markdown(evidence_grid_html(hasil.bukti_pendukung), unsafe_allow_html=True)

            with tab3:
                if hasil.saran_alternatif:
                    for alt in hasil.saran_alternatif:
                        col_alt_img, col_alt_info = st.columns([1, 3.3], gap="medium")
                        with col_alt_img:
                            img_bytes = fetch_product_image(alt.kata_kunci_gambar or alt.nama_produk)
                            if img_bytes:
                                st.image(img_bytes, width="stretch")
                            else:
                                st.markdown(
                                    '<div class="img-fallback">Foto kemasan<br/>belum tersedia</div>',
                                    unsafe_allow_html=True,
                                )
                        with col_alt_info:
                            st.markdown(alternative_card_html(alt), unsafe_allow_html=True)
                else:
                    st.info("Produk ini sudah memenuhi kriteria ramah lingkungan yang terverifikasi.")
        else:
            st.markdown(ready_placeholder_html(), unsafe_allow_html=True)