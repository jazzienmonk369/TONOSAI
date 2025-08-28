import streamlit as st
import boot  # globalni CSS

st.set_page_config(page_title="TONOSAI — Donacije", page_icon="💫", layout="wide")

st.title("💫 Podrži TONOSAI")
st.write("Hvala što razmišljaš da podržiš razvoj novih alata! Donacije idu na servere, audio biblioteke i razvoj modula.")

c1, c2 = st.columns([2,1])
with c1:
    method = st.radio("Metod", ["PayPal", "Ko-fi", "Buy Me a Coffee"], horizontal=True)
    amount = st.slider("Iznos (EUR)", 1, 50, 5)
    msg = st.text_input("Poruka (opciono)", "")

    # TODO: upiši svoje naloge:
    PAYPAL_ME = "tvoj_paypal_me_username"     # npr. "jazziemonk"
    KOFI = "tvoj_kofi_username"               # npr. "tonosai"
    BMC  = "tvoj_bmc_username"                # npr. "tonosai"

    if method == "PayPal":
        # PayPal.me format: https://paypal.me/<user>/<amount>EUR
        link = f"https://paypal.me/{PAYPAL_ME}/{amount}EUR"
    elif method == "Ko-fi":
        # Ko-fi parametar iznosa se rešava na njihovoj strani – link je dovoljan
        link = f"https://ko-fi.com/{KOFI}"
    else:
        link = f"https://buymeacoffee.com/{BMC}"

    st.link_button("❤️ Doniraj", link, use_container_width=True)
    st.caption("Link vodi na bezbednu stranicu provajdera (PayPal/Ko-fi/BMC).")

with c2:
    st.subheader("Alternativno")
    iban = "RS00 0000 0000 0000 0000 00"  # Ako hoćeš bank transfer
    st.write("IBAN (bank transfer):")
    st.code(iban)
    st.caption("Pošalji nam poruku nakon uplate kako bismo te dodali u listu zvezda ⭐")
