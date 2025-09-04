# pages/03_donacije.py — Donacije (kartice + kripto + banka)

from __future__ import annotations
from pathlib import Path
import urllib.parse
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="TONOSAI — Donacije", page_icon="💖", layout="wide")

st.title("💖 Donacije")
st.caption("Hvala što podržavaš TONOSAI. Tvoje donacije održavaju studio, eksperimente i otvorene alate.")

# --- Helper: copy-to-clipboard (radi za bilo koji text) ---
def copy_btn(text: str, label: str = "Copy"):
    components.html(f"""
    <button onclick="navigator.clipboard.writeText('{text}')"
            style="padding:6px 10px;border-radius:8px;border:1px solid rgba(255,255,255,.15);
                   background:rgba(255,255,255,.06);color:#fff;cursor:pointer;">
      {label}
    </button>
    """, height=36)

# --- Helper: QR (bez lokalnih dependencija; koristi quickchart) ---
def qr(url: str, size: int = 180):
    q = urllib.parse.quote(url)
    st.image(f"https://quickchart.io/qr?size={size}x{size}&text={q}", width=size)

tabs = st.tabs(["Kartica / PayPal", "Crypto", "Banka / Wire", "Ostalo"])

# 1) Stripe / PayPal
with tabs[0]:
    st.subheader("Kartica / PayPal")
    st.write("Najjednostavnije je platnom karticom (Stripe Payment Link) ili PayPal-om.")
    st.write("Dodaj ovde svoje URL-ove (Payment Link / PayPal.me), npr:")
    st.markdown("- **Stripe:** `https://checkout.stripe.com/pay/…`  \n- **PayPal.me:** `https://paypal.me/tonosai`")
    # st.link_button("Doniraj karticom (Stripe)", "https://…")
    # st.link_button("Doniraj preko PayPal-a", "https://…")

# 2) Kripto
with tabs[1]:
    st.subheader("Crypto")
    st.caption("Kopiraj adresu ili skeniraj QR. Obavezno izaberi tačnu mrežu.")

    # <<< UNESI SVOJE ADRESE >>>
    BTC_BECH32 = "bc1_your_btc_address_here"
    ETH_EVM    = "0xYourEvmAddressHere"  # ETH/USDC/USDT (EVM)
    SOL_ADDR   = ""  # opciono: Solana adresa

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**BTC (bech32, mreža: Bitcoin)**")
        st.code(BTC_BECH32, language="text")
        copy_btn(BTC_BECH32, "Copy BTC")
        qr(f"bitcoin:{BTC_BECH32}")
    with col2:
        st.markdown("**ETH (mreža: Ethereum)**")
        st.code(ETH_EVM, language="text")
        copy_btn(ETH_EVM, "Copy ETH")
        qr(f"ethereum:{ETH_EVM}")
        st.markdown("**USDC / USDT (EVM)** — koristi **istu** adresu, ali izaberi pravu mrežu u svom wallet-u.")
    with col3:
        st.markdown("**USDC (Polygon)**")
        st.code(ETH_EVM, language="text")
        copy_btn(ETH_EVM, "Copy Polygon USDC")
        qr(f"ethereum:{ETH_EVM}")  # EVM URI; mreža je na tebi da je izabereš u wallet-u
        if SOL_ADDR:
            st.markdown("---\n**SOL (Solana)**")
            st.code(SOL_ADDR, language="text")
            copy_btn(SOL_ADDR, "Copy SOL")
            qr(SOL_ADDR)

    st.info("📩 Ako želiš potvrdu/priznanicu, pošalji nam **tx hash** i kratku poruku na e-mail (vidi footer).")
    st.caption("Napomena: Donacije nisu porezno priznate osim ako smo registrovani kao udruženje / neprofitno (proveri lokalne propise).")

# 3) Banka
with tabs[2]:
    st.subheader("Banka / Wire")
    st.write("Ovde navedi IBAN/SWIFT ili lokalnu uplatu.")
    st.code("Naziv: TONOSAI Studio\nIBAN: XX00 0000 0000 0000 0000\nSWIFT/BIC: XXXXXXX\nSvrha: Donacija", language="text")

# 4) Ostalo (Ko-fi, OpenCollective, GitHub Sponsors…)
with tabs[3]:
    st.subheader("Ostalo")
    st.write("Dodatni kanali:")
    st.markdown("""
    - **GitHub Sponsors** – mesečno ili jednokratno za OSS
    - **Ko-fi / Buy Me a Coffee** – mikro donacije
    - **OpenCollective** – transparentan budžet zajednice
    """)
