        import streamlit as st
import google.generativeai as genai

# 1. Configurazione Sicurezza
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except:
    st.error("⚠️ Configura la chiave nei 'Secrets' di Streamlit!")
    st.stop()

model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="Area Manager AI", page_icon="👞")
st.title("👞 Assistant Area Manager")

# --- INTERFACCIA ---
nome_cliente = st.text_input("Distributore")
oggetto_mail = st.text_input("Oggetto")
finalita = st.selectbox("Finalità", ["Ringraziamento", "Proposta Offerta", "Appuntamento"])
bozza_input = st.text_area("Bozza veloce")

if st.button("Genera Email"):
    if nome_cliente and bozza_input:
        prompt = f"Sei un Area Manager DPI. Scrivi una mail a {nome_cliente} su {oggetto_mail}. Finalità: {finalita}. Note: {bozza_input}"
        response = model.generate_content(prompt)
        st.code(response.text, language="text")
    else:
        st.warning("Compila i campi!")
