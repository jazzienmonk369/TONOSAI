# lib/i18n.py
import json
from pathlib import Path

_CACHE, _MTIME = {}, {}

def _load(lang: str):
    fp = Path(f"i18n/{lang}.json")
    if not fp.exists():
        return {}
    mtime = fp.stat().st_mtime
    if _MTIME.get(lang) != mtime:
        _CACHE[lang] = json.loads(fp.read_text(encoding="utf-8"))
        _MTIME[lang] = mtime
    return _CACHE[lang]

def t(key: str, default: str | None = None):
    import streamlit as st
    lang = st.session_state.get("lang", "sr")
    return _load(lang).get(key, default if default is not None else key)
