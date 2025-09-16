# tools/bulk_inject_lang.py
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]  # root repo
PAGES = ROOT / "pages"

def _norm(stem: str) -> str:
    return re.sub(r'[^a-zA-Z0-9_]', '_', stem)

def _insert_after(pattern, text, insert, flags=re.M):
    m = re.search(pattern, text, flags)
    if not m:
        return insert + text
    return text[:m.end()] + insert + text[m.end():]

def process(fp: Path, dry=False):
    src = fp.read_text(encoding="utf-8")
    original = src
    changed = False

    # 1) Import lang_selector
    if "from lib.ui import lang_selector" not in src:
        # posle 'import streamlit as st' ako postoji, inače na vrh
        m = re.search(r"^import streamlit as st[^\n]*\n", src, re.M)
        insert_at = m.end() if m else 0
        src = src[:insert_at] + "from lib.ui import lang_selector\n" + src[insert_at:]
        changed = True

    # 2) Import t()
    if "from lib.i18n import t" not in src:
        m = re.search(r"^from lib.ui import lang_selector[^\n]*\n", src, re.M)
        insert_at = m.end() if m else 0
        src = src[:insert_at] + "from lib.i18n import t\n" + src[insert_at:]
        changed = True

    # 3) Poziv lang_selector("<page_id>")
    if "lang_selector(" not in src:
        page_id = _norm(fp.stem)
        # posle st.set_page_config(...), ako ga ima; inače posle importova
        m_cfg = re.search(r"st\.set_page_config\(.*?\)\s*\n", src, re.S)
        if m_cfg:
            insert_at = m_cfg.end()
            src = src[:insert_at] + f'lang_selector("{page_id}")\n' + src[insert_at:]
        else:
            # posle bloka importova
            m_imp = re.search(r"(?:^|\n)(?:from .*|import .*)+\n", src, re.M)
            insert_at = m_imp.end() if m_imp else 0
            src = src[:insert_at] + f'lang_selector("{page_id}")\n' + src[insert_at:]
        changed = True

    if not changed:
        return False

    if dry:
        print(f"[DRY] would update: {fp.name}")
        return True

    # backup
    bak = fp.with_suffix(fp.suffix + ".bak")
    bak.write_text(original, encoding="utf-8")
    fp.write_text(src, encoding="utf-8")
    print(f"Updated: {fp.name} (backup: {bak.name})")
    return True

def main():
    dry = "--dry-run" in sys.argv
    files = sorted(PAGES.glob("*.py"))
    if not files:
        print("No *.py files in pages/.")
        return
    n = 0
    for f in files:
        if process(f, dry=dry):
            n += 1
    print(f"Done. Files changed: {n}")

if __name__ == "__main__":
    main()
