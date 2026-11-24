import os
import time
from typing import List, Optional
import streamlit as st
from PIL import Image
from google import genai
from google.genai import types

from src.schemas import AuditGreenwashing
from src.prompts import SYSTEM_INSTRUCTION, USER_AUDIT_PROMPT


def get_api_key() -> str:
    """Mengambil API Key dari Streamlit Secrets, Environment Variable, atau Sidebar."""
    try:
        if "GEMINI_API_KEY" in st.secrets and st.secrets["GEMINI_API_KEY"]:
            return st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass

    env_key = os.environ.get("GEMINI_API_KEY", "")
    if env_key:
        return env_key

    return st.session_state.get("user_api_key", "")


def get_candidate_models(client: genai.Client) -> List[str]:
    """Menyusun urutan model Gemini multimodal yang aktif untuk akun ini."""
    preferred = [
        "gemini-3.8-flash",
        "gemini-3.8-flash-lite",
        "gemini-3-flash-preview",
        "gemini-2.5-flash",
        "gemini-2.5-flash-lite",
    ]
    try:
        discovered = []
        for m in client.models.list():
            name = getattr(m, "name", "")
            short_name = name.replace("models/", "")
            methods = getattr(m, "supported_generation_methods", []) or []
            is_gemini = short_name.startswith("gemini-")
            is_excluded = any(
                x in short_name
                for x in ("embedding", "imagen", "veo", "tts", "audio", "robotics", "computer-use")
            )
            if is_gemini and not is_excluded:
                if not methods or "generateContent" in methods:
                    discovered.append(short_name)
        for m_name in reversed(discovered):
            if m_name not in preferred:
                preferred.append(m_name)
    except Exception:
        pass
    return preferred


def analyze_product_label(api_key: str, image: Image.Image) -> AuditGreenwashing:
    """Mengirim foto kemasan ke Gemini Vision dengan auto-retry & fallback."""
    client = genai.Client(api_key=api_key)
    candidates = get_candidate_models(client)
    last_error: Optional[Exception] = None

    transient_keywords = (
        "503",
        "UNAVAILABLE",
        "429",
        "RESOURCE_EXHAUSTED",
        "high demand",
        "overloaded",
    )

    for model_name in candidates:
        for attempt in range(2):
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=[image, USER_AUDIT_PROMPT],
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_INSTRUCTION,
                        response_mime_type="application/json",
                        response_schema=AuditGreenwashing,
                        temperature=0.2,
                    ),
                )
                if response.parsed is not None:
                    return response.parsed
                return AuditGreenwashing.model_validate_json(response.text)
            except Exception as e:
                last_error = e
                err_msg = str(e)
                if "404" in err_msg or "NOT_FOUND" in err_msg:
                    break
                if any(k in err_msg for k in transient_keywords):
                    if attempt == 0:
                        time.sleep(1.5)
                        continue
                    break
                raise e

    raise RuntimeError(
        f"Server sedang sibuk. Silakan klik tombol pemeriksaan kembali beberapa saat lagi. ({last_error})"
    )