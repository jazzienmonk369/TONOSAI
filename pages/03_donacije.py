# pages/03_donacije.py — Donacije (PayPal + kripto + banka) + random "hvala" + Secret Thank You overlay
from __future__ import annotations
import urllib.parse, random
import streamlit as st
import streamlit.components.v1 as components
from lib.ui import lang_selector
from lib.i18n import t

st.set_page_config(page_title="TONOSAI — Donacije", page_icon="💖", layout="wide")
st.markdown("""
<style>
/* pulsirajući halo efekt oko link_button-a */
.tns-pulse a, .tns-pulse button{
  position: relative;
  isolation: isolate;
}
.tns-pulse a::before, .tns-pulse button::before{
  content: "";
  position: absolute;
  inset: -4px;
  border-radius: 12px;
  box-shadow: 0 0 0 0 rgba(255,255,255,0.40);
  animation: tnsPulse 2.2s ease-out infinite;
  z-index: -1;
}
@keyframes tnsPulse{
  0%   { box-shadow: 0 0 0 0 rgba(255,255,255,0.40); }
  70%  { box-shadow: 0 0 0 14px rgba(255,255,255,0); }
  100% { box-shadow: 0 0 0 0 rgba(255,255,255,0); }
}
</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>
/* ── Corner Mist (blagi oblak u uglu) ─────────────────────────────── */
.tns-corner-mist{ position: relative; }
.tns-corner-mist::before{
  content:"";
  position:absolute;
  bottom:-60px; left:-60px;          /* ⬅️ dno-levo; promeni po želji */
  width:360px; height:360px;
  background: radial-gradient(circle at 70% 70%,
              rgba(120,200,255,.24), rgba(120,200,255,0) 60%);
  filter: blur(26px);
  pointer-events:none;
  animation: mistFloat 8s ease-in-out infinite alternate;
  z-index: 0;                        /* ispod sadržaja */
}
@keyframes mistFloat{
  from { transform: translate(-8px, 6px) scale(1.00); opacity:.75; }
  to   { transform: translate( 6px,-6px) scale(1.07); opacity:.45; }
}

/* Varijante boja (po želji) */
.tns-corner-mist.mist-gold::before{
  background: radial-gradient(circle at 70% 70%,
              rgba(255,210,120,.22), rgba(255,210,120,0) 60%);
}
.tns-corner-mist.mist-rose::before{
  background: radial-gradient(circle at 70% 70%,
              rgba(255,140,200,.20), rgba(255,140,200,0) 60%);
}
.tns-corner-mist.mist-emerald::before{
  background: radial-gradient(circle at 70% 70%,
              rgba(110,255,200,.20), rgba(110,255,200,0) 60%);
}
</style>
""", unsafe_allow_html=True)



# ── Jezik / Naslov ───────────────────────────────────────────────────────────
lang_selector("03_donacije")
st.title("💖 Donacije")

# ── Emotivni uvod (SR/EN) ────────────────────────────────────────────────────
if st.session_state.get("lang", "sr") == "en":
    st.markdown(
        "> 💫 **Support TONOSAI**  \n"
        "> TONOSAI is an independent creative studio where **Cosmos, Sound, Human, AI, Art, Science, and Spirituality** unite in **Harmony**.  \n"
        "> Your support helps us continue creating free tools, games, and sounds for the world.  \n"
        "> 🌱 Even the smallest donation keeps the project alive and growing."
    )
else:
    st.markdown(
        "> 💫 **Podrži TONOSAI**  \n"
        "> TONOSAI je nezavisan kreativni studio gde se **Kosmos, Zvuk, Čovek, AI, Umetnost, Nauka i Duhovnost** spajaju u **Harmoniji**.  \n"
        "> Tvoja podrška pomaže da nastavimo da pravimo besplatne alate, igre i zvukove za ceo svet.  \n"
        "> 🌱 I najmanja donacija znači da projekat diše dalje i raste."
    )


st.caption("Hvala što podržavaš TONOSAI. Tvoje donacije održavaju studio, eksperimente i otvorene alate.")

# ── Helpers ──────────────────────────────────────────────────────────────────
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

# ── Random THANKS poruke ─────────────────────────────────────────────────────
THANKS = {
    "sr": [
        "💖 Hvala ti! Tvoj ton sada svira u našoj kosmičkoj simfoniji.",
        "🌌 Tvoja podrška je zvezda koja sija za TONOSAI.",
        "🎵 Svaka tvoja donacija stvara novu melodiju u našem univerzumu.",
        "🌱 Zahvaljujući tebi, TONOSAI raste i diše dalje."
    ],
    "en": [
        "💖 Thank you! Your tone is now part of our cosmic symphony.",
        "🌌 Your support is a star shining for TONOSAI.",
        "🎵 Every donation creates a new melody in our universe.",
        "🌱 Thanks to you, TONOSAI keeps growing and breathing."
    ],
}

def show_secret_thank_you(msg: str):
    """Fullscreen overlay sa porukom zahvalnosti + CSS fade-in + nežne 'iskrice' ✦."""
    components.html(
        f"""
        <div id="tns-overlay"
             style="position:fixed;inset:0;background:rgba(10,10,20,.92);
                    display:flex;align-items:center;justify-content:center;
                    z-index:999999;animation: fadeIn 800ms ease-out;">
          
          <!-- Nebo sa iskrama -->
          <div class="tns-sky" style="position:absolute;inset:0;overflow:hidden;pointer-events:none;">
            <!-- Dovoljno je 14-16 iskrica; raspoređene su u % koordinatama -->
            <span class="spark" style="--x:12%; --y:22%; --d:1.2s;"></span>
            <span class="spark" style="--x:28%; --y:68%; --d:1.6s;"></span>
            <span class="spark" style="--x:44%; --y:12%; --d:1.4s;"></span>
            <span class="spark" style="--x:61%; --y:34%; --d:1.5s;"></span>
            <span class="spark" style="--x:73%; --y:18%; --d:1.3s;"></span>
            <span class="spark" style="--x:82%; --y:56%; --d:1.7s;"></span>
            <span class="spark" style="--x:18%; --y:78%; --d:1.8s;"></span>
            <span class="spark" style="--x:35%; --y:47%; --d:1.25s;"></span>
            <span class="spark" style="--x:52%; --y:72%; --d:1.65s;"></span>
            <span class="spark" style="--x:68%; --y:85%; --d:1.3s;"></span>
            <span class="spark" style="--x:86%; --y:41%; --d:1.55s;"></span>
            <span class="spark" style="--x:10%; --y:40%; --d:1.4s;"></span>
            <span class="spark" style="--x:90%; --y:20%; --d:1.9s;"></span>
            <span class="spark" style="--x:57%; --y:10%; --d:1.2s;"></span>
          </div>

          <!-- Kartica poruke -->
          <div style="position:relative;text-align:center;max-width:640px;padding:28px 24px;
                      border-radius:20px;border:1px solid rgba(255,255,255,.14);
                      background:rgba(255,255,255,.08);color:#fff;backdrop-filter: blur(2px);">
            <div style="font-size:64px;line-height:1;margin-bottom:10px;">💖</div>
            <div style="font-size:22px;margin-bottom:12px;">{msg}</div>
            <div style="opacity:.85;margin-bottom:18px;">
              {"Bez tebe ovo ne bi bilo moguće." if st.session_state.get("lang","sr")!="en" else "Without you, this wouldn’t be possible."}
            </div>
            <button onclick="document.getElementById('tns-overlay').remove()"
                    style="padding:10px 16px;border-radius:12px;border:1px solid rgba(255,255,255,.18);
                           background:rgba(255,255,255,.15);color:#fff;cursor:pointer;font-size:14px;">
              {"Zatvori" if st.session_state.get("lang","sr")!="en" else "Close"}
            </button>
          </div>
        </div>

        <!-- CSS animacije (i dalje unutar istog stringa) -->
        <style>
          @keyframes fadeIn {{
            from {{ opacity: 0; }}
            to   {{ opacity: 1; }}
          }}
          @keyframes twinkle {{
            0%   {{ opacity: .25; transform: scale(.8);   filter: drop-shadow(0 0 0px rgba(255,255,255,.0)); }}
            50%  {{ opacity: .95; transform: scale(1.35); filter: drop-shadow(0 0 6px rgba(255,255,255,.85)); }}
            100% {{ opacity: .35; transform: scale(1.0);  filter: drop-shadow(0 0 2px rgba(255,255,255,.35)); }}
          }}
          .spark {{
            position: absolute;
            left: var(--x); top: var(--y);
            width: 3px; height: 3px; border-radius: 50%;
            background: rgba(255,255,255,.95);
            animation: twinkle var(--d, 1.5s) ease-in-out infinite alternate;
          }}
        </style>
        """,
        height=320, scrolling=False
    )




def show_thanks(amount_label: str | None = None):
    msgs = THANKS["en"] if st.session_state.get("lang","sr") == "en" else THANKS["sr"]
    msg = random.choice(msgs)
    if amount_label:
        msg = f"{msg}  \n{amount_label}"
    st.success(msg)
    st.balloons()
    st.toast("Hvala na podršci! 💖" if st.session_state.get("lang","sr")!="en" else "Thank you for the support! 💖")
    # „Secret Thank You“ overlay
    show_secret_thank_you(msg)

# ── Tabs ─────────────────────────────────────────────────────────────────────
tabs = st.tabs(["PayPal", "Crypto", "Banka / Wire", "Ostalo"])

# === 1) PayPal ===============================================================
with tabs[0]:
    st.subheader("PayPal donacije" if st.session_state.get("lang","sr")!="en" else "PayPal donations")

    # ⇣⇣⇣  postavi svoj PayPal.me link  ⇣⇣⇣
    PAYPAL_ME = "https://paypal.me/tonosai"   # <— OVDE TVOJ LINK
    CURRENCY_QS = "?currency=EUR"             # "" ako ne želiš da fiksiraš valutu

    if not PAYPAL_ME:
        st.warning("Dodaj svoj PayPal.me link u kodu (promenljiva PAYPAL_ME).")
    else:
        # Glavno dugme – korisnik sam bira iznos (sa 'pulse' aureolom)
        st.markdown('<div class="tns-pulse">', unsafe_allow_html=True)
        clicked_main = st.link_button(
            "💫 Doniraj preko PayPal-a (izaberi iznos)" if st.session_state.get("lang","sr")!="en"
            else "💫 Donate via PayPal (choose amount)",
            PAYPAL_ME, use_container_width=True
        )
        st.markdown('</div>', unsafe_allow_html=True)

        if clicked_main:
            show_thanks("💳 PayPal")

        st.caption(
            "Otvara PayPal.me stranicu gde sam biraš iznos donacije."
            if st.session_state.get("lang","sr")!="en" else
            "Opens PayPal.me page where you choose the amount."
        )

        st.divider()
        st.markdown("**Brze donacije (jedan klik):**" if st.session_state.get("lang","sr")!="en" else "**Quick donations (one click):**")

        colA, colB, colC, colD = st.columns(4)
        quick = [3, 5, 10, 20]
        icons = {3:"🎵", 5:"🌌", 10:"🧩", 20:"🚀"}

        labels_sr = {
            3: "€3 🎵 Kafa za TONOSAI",
            5: "€5 🌌 Podrška zvučnim eksperimentima",
            10: "€10 🧩 Razvoj novih alata",
            20: "€20 🚀 Veliki skok za studio",
        }
        labels_en = {
            3: "€3 🎵 Coffee for TONOSAI",
            5: "€5 🌌 Support for sound experiments",
            10: "€10 🧩 Develop new tools",
            20: "€20 🚀 A big leap for the studio",
        }

        subs_sr = {
            3: "Mali znak pažnje, velika podrška.",
            5: "Pomaže da nastaju novi loop-ovi.",
            10: "Direktno ulažeš u alate.",
            20: "Otvara nova vrata i mogućnosti.",
        }
        subs_en = {
            3: "Small sign, big impact.",
            5: "Helps new loops & melodies.",
            10: "Directly funds tools.",
            20: "Opens new possibilities.",
        }

        cols = [colA, colB, colC, colD]
        for c, amount in zip(cols, quick):
            btn_text = f"€{amount} {icons[amount]}"
            clicked = c.link_button(
                btn_text,
                f"{PAYPAL_ME}/{amount}{CURRENCY_QS}",
                use_container_width=True
            )
            # mini opis ispod svakog dugmeta
            c.caption(subs_en[amount] if st.session_state.get("lang","sr")=="en" else subs_sr[amount])

            if clicked:
                lbl = labels_en[amount] if st.session_state.get("lang","sr")=="en" else labels_sr[amount]
                show_thanks(lbl)

        # QR kao alternativa
st.markdown("—")

# 👇 OTVORI maglu oko QR-a (dno-levo)
st.markdown('<div class="tns-corner-mist">', unsafe_allow_html=True)

st.caption(
    "Skeniraj QR da otvoriš PayPal.me:"
    if st.session_state.get("lang","sr")!="en" else
    "Scan the QR to open PayPal.me:"
)
qr(PAYPAL_ME)

# 👆 ZATVORI maglu
st.markdown('</div>', unsafe_allow_html=True)



# === 2) Kripto ===============================================================
with tabs[1]:
    st.subheader("Crypto")
    st.caption("Kopiraj adresu ili skeniraj QR. OBAVEZNO izaberi TAČNU mrežu u svom wallet-u.")

    # >>> TVOJE ADRESE (ETH i POL već imaš) <<<
    BTC_BECH32    = "bc1qpdrrqtujud7t2q6q65tpmjs9vgzhxu9lcqmn9t"                      # dodaćemo kasnije (bc1…)
    ETH_EVM       = "0x26Fb51465403ECf2edD94d06a471Adb539B8ee24"     # ETH / EVM  (isti 0x)
    USDC_POLYGON  = "0x26Fb51465403ECf2edD94d06a471Adb539B8ee24"     # USDC / Polygon (isti 0x)
    USDT_TRC20    = ""                      # dodaćemo kasnije (T…)

    # mini CSS bedž za mrežu
    st.markdown(
        "<style>.tns-chip{display:inline-block;padding:2px 8px;border-radius:999px;"
        "font-size:11px;border:1px solid rgba(255,255,255,.25);opacity:.9;margin-left:6px}</style>",
        unsafe_allow_html=True
    )

    # helper: prikaži samo ako adresa postoji
    def wallet_block(title_html: str, addr: str, note: str = "", qr_prefix: str = "", copy_label: str = "Copy"):
        if not addr:
            return
        st.markdown(title_html, unsafe_allow_html=True)
        if note:
            st.caption(note)
        st.code(addr, language="text")
        copy_btn(addr, copy_label)
        qr(f"{qr_prefix}{addr}")
        st.markdown("---")

    # raspored u 2 kolone
    col1, col2 = st.columns(2)

    with col1:
        wallet_block(
            f"**USDC** <span class='tns-chip'>Polygon</span>",
            USDC_POLYGON,
            "0x adresa (ista kao ETH). U svom wallet-u obavezno izaberi mrežu Polygon.",
            qr_prefix="", copy_label="Copy USDC-Polygon",
        )

        # USDT (TRC20) – tek kad budeš imao T… adresu (Trust iPad / TronLink)
        wallet_block(
            f"**USDT** <span class='tns-chip'>TRC20 / Tron</span>",
            USDT_TRC20,
            "Niski fee, super za male iznose.",
            qr_prefix="", copy_label="Copy USDT-TRC20",
        )

    with col2:
        wallet_block(
            f"**ETH** <span class='tns-chip'>EVM / Ethereum</span>",
            ETH_EVM,
            "Univerzalno podržano.",
            qr_prefix="", copy_label="Copy ETH (EVM)",
        )

        wallet_block(
            f"**BTC** <span class='tns-chip'>Bitcoin</span>",
            BTC_BECH32,
            "On-chain fee može biti veći; za male iznose razmisli o Lightning-u.",
            qr_prefix="bitcoin:", copy_label="Copy BTC",
        )

    # kratko uputstvo za posetioce (SR/EN)
    if st.session_state.get("lang","sr") == "en":
        st.caption("💡 How to donate crypto: • Send **ETH** (network: Ethereum) to the 0x address. "
                   "• Send **USDC** (network: Polygon) to the same 0x address. Always double-check the network in your wallet.")
    else:
        st.caption("💡 Kako donirati kripto: • **ETH** (mreža: Ethereum) pošalji na 0x adresu. "
                   "• **USDC** (mreža: Polygon) pošalji na istu 0x adresu. Uvek proveri mrežu u svom wallet-u.")



# === 3) Banka / Wire =========================================================
with tabs[2]:
    st.subheader("Banka / Wire")
    st.code(
        "Naziv: TONOSAI Studio\nIBAN: XX00 0000 0000 0000 0000\nSWIFT/BIC: XXXXXXX\nSvrha: Donacija",
        language="text",
    )

# === 4) Ostalo ===============================================================
with tabs[3]:
    st.subheader("Ostalo")
    st.markdown(
        """
        - **GitHub Sponsors** – mesečno ili jednokratno za OSS  
        - **Ko-fi / Buy Me a Coffee** – mikro donacije  
        - **OpenCollective** – transparentan budžet zajednice
        """
    )
