import io
import json
import urllib.parse
import urllib.request
from typing import Optional
import streamlit as st
from PIL import Image, ImageOps


def preprocess_image(uploaded_file, max_size: int = 1024) -> Image.Image:
    """Memperbaiki orientasi EXIF dan mengecilkan resolusi gambar agar hemat kuota."""
    img = Image.open(uploaded_file)
    img = ImageOps.exif_transpose(img)
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
    img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
    return img


def _download_valid_image(url: str, timeout: int = 5) -> Optional[bytes]:
    """Mengunduh gambar dan memvalidasi keutuhannya menggunakan Pillow."""
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"},
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            if resp.status != 200:
                return None
            raw = resp.read()
            if len(raw) < 800:
                return None
            with Image.open(io.BytesIO(raw)) as im:
                im = im.convert("RGB")
                buf = io.BytesIO()
                im.save(buf, format="PNG")
                return buf.getvalue()
    except Exception:
        return None


@st.cache_data(ttl=3600, show_spinner=False)
def fetch_product_image(query: str) -> Optional[bytes]:
    """Mencari foto kemasan produk alternatif dari katalog terbuka & thumbnail web."""
    clean_q = query.strip()
    if not clean_q:
        return None

    encoded_q = urllib.parse.quote_plus(clean_q)
    open_endpoints = [
        f"https://world.openproductsfacts.org/cgi/search.pl?search_terms={encoded_q}&search_simple=1&action=process&json=1&page_size=3",
        f"https://world.openbeautyfacts.org/cgi/search.pl?search_terms={encoded_q}&search_simple=1&action=process&json=1&page_size=3",
        f"https://world.openfoodfacts.org/cgi/search.pl?search_terms={encoded_q}&search_simple=1&action=process&json=1&page_size=3",
    ]
    for api_url in open_endpoints:
        try:
            req = urllib.request.Request(api_url, headers={"User-Agent": "BelanjaBijakApp/1.0"})
            with urllib.request.urlopen(req, timeout=3) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                for prod in data.get("products", []):
                    img_url = prod.get("image_front_small_url") or prod.get("image_front_url")
                    if img_url:
                        img_bytes = _download_valid_image(img_url, timeout=4)
                        if img_bytes:
                            return img_bytes
        except Exception:
            continue

    thumb_query = urllib.parse.quote_plus(f"{clean_q} produk kemasan")
    thumb_url = f"https://tse2.mm.bing.net/th?q={thumb_query}&w=360&h=360&c=7&rs=1&p=0"
    return _download_valid_image(thumb_url, timeout=5)