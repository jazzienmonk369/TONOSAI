# pages/03_donacije.py — Donacije (PayPal + kripto + banka)

from __future__ import annotations
import urllib.parse
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="TONOSAI — Donacije", page_icon="💖", layout="wide")

st.title("💖 Donacije")
st.caption("Hvala što podržavaš TONOSAI. Tvoje donacije održavaju studio, eksperimente i otvorene alate.")

# ---------- Helpers ----------
def copy_btn(text: str, label: str = "Copy"):
    safe = text.replace("'", "\\'")
    components.html(
        f"""
        <button onclick="navigator.clipboard.writeText('{safe}')"
                style="padding:6px 10px;border-radius:8px;border:1px solid rgba(255,255,255,.15);
                       background:rgba(255,255,255,.06);color:#fff;cursor:pointer;">
          {label}
        </button>
        """,
        height=36,
    )

def qr(data: str, size: int = 180):
    q = urllib.parse.quote(data)
    st.image(f"https://quickchart.io/qr?size={size}x{size}&text={q}", width=size)

# ---------- Tabs ----------
tabs = st.tabs(["PayPal", "Crypto", "Banka / Wire", "Ostalo"])

# === 1) PayPal ===
with tabs[0]:
    st.subheader("PayPal donacije")

    # ⇣⇣⇣  postavi svoj PayPal.me link  ⇣⇣⇣
    PAYPAL_ME = "https://paypal.me/tonosai"
    # (opciono) ako želiš da predložiš valutu u brzim iznosima:
    CURRENCY_QS = "?currency=EUR"   # ili "" ako ne želiš da forsiraš valutu

    if not PAYPAL_ME:
        st.warning("Dodaj svoj PayPal.me link u kodu (promenljiva PAYPAL_ME).")
    else:
        # Glavno dugme – korisnik sam bira iznos
        st.link_button("🟦 Doniraj preko PayPal-a (izaberi iznos)", PAYPAL_ME, use_container_width=True)
        st.caption("Otvara PayPal.me stranicu gde sam biraš iznos donacije.")

        st.divider()
        st.markdown("**Brze donacije (jedan klik):**")
        colA, colB, colC, colD = st.columns(4)
        quick = [3, 5, 10, 20]  # iznosi koje nudimo
        cols = [colA, colB, colC, colD]
        for c, amount in zip(cols, quick):
            # paypal.me/korisnik/IZNOS + opcioni ?currency=EUR
            c.link_button(f"€{amount}", f"{PAYPAL_ME}/{amount}{CURRENCY_QS}", use_container_width=True)

        # QR kao alternativa
        st.markdown("—")
        st.caption("Skeniraj QR da otvoriš PayPal.me:")
        qr(PAYPAL_ME)

# === 2) Kripto ===
with tabs[1]:
    st.subheader("Crypto")
    st.caption("Kopiraj adresu ili skeniraj QR. Obavezno izaberi tačnu mrežu u svom wallet-u.")

    # >>> Unesi svoje adrese <<<
    BTC_BECH32   = "bc1_your_btc_address_here"
    ETH_EVM      = "0xYourEvmAddressHere"     # ETH / USDC / USDT (EVM)
    POLYGON_USDC = ETH_EVM                    # obično ista 0x adresa (samo mreža Polygon)
    LIGHTNING    = ""                         # npr. lnurl ili lightning:... (opciono)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**BTC (bech32, mreža: Bitcoin)**")
        st.code(BTC_BECH32, language="text")
        copy_btn(BTC_BECH32, "Copy BTC")
        qr(f"bitcoin:{BTC_BECH32}")

    with col2:
        st.markdown("**ETH (EVM)**")
        st.code(ETH_EVM, language="text")
        copy_btn(ETH_EVM, "Copy ETH")
        qr(f"ethereum:{ETH_EVM}")
        st.caption("**USDC / USDT (EVM)** koriste **istu 0x adresu** — samo u wallet-u izaberi mrežu.")

    with col3:
        st.markdown("**USDC (Polygon)**")
        st.code(POLYGON_USDC, language="text")
        copy_btn(POLYGON_USDC, "Copy Polygon USDC")
        qr(f"ethereum:{POLYGON_USDC}")

        if LIGHTNING:
            st.markdown("---\n**⚡ Lightning**")
            st.code(LIGHTNING, language="text")
            copy_btn(LIGHTNING, "Copy Lightning")
            qr(LIGHTNING)

    st.info("📩 Ako želiš potvrdu/priznanicu, pošalji **tx hash** i kratku poruku na e-mail (vidi footer).")
    st.caption("Napomena: Donacije nisu porezno priznate osim ako je registrovano udruženje / neprofitno (proveri lokalne propise).")

# === 3) Banka / Wire ===
with tabs[2]:
    st.subheader("Banka / Wire")
    st.code(
        "Naziv: TONOSAI Studio\nIBAN: XX00 0000 0000 0000 0000\nSWIFT/BIC: XXXXXXX\nSvrha: Donacija",
        language="text",
    )

# === 4) Ostalo ===
with tabs[3]:
    st.subheader("Ostalo")
    st.markdown(
        """
        - **GitHub Sponsors** – mesečno ili jednokratno za OSS  
        - **Ko-fi / Buy Me a Coffee** – mikro donacije  
        - **OpenCollective** – transparentan budžet zajednice
        """
    )
