import streamlit as st
import google.generativeai as genai
import urllib.parse

# 1. Configurazione API
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except Exception as e:
    st.error("Configura GEMINI_API_KEY nei Secrets di Streamlit!")
    st.stop()

# Usiamo il nome completo del modello per evitare l'errore NotFound
model = genai.GenerativeModel('models/gemini-1.5-flash')

st.set_page_config(page_title="Area Manager AI", page_icon="👞")
st.title("👞 Assistant Area Manager")

# --- INTERFACCIA ---
col1, col2 = st.columns(2)
with col1:
    distributore = st.text_input("Nome Distributore")
    oggetto = st.text_input("Oggetto Mail")

with col2:
    profilo = st.selectbox("Profilo Partner", ["Partner Storico", "Nuovo Lead", "Recupero Rapporto"])
    obiettivo = st.selectbox("Obiettivo", ["Svuotare Magazzino", "Inserimento Nuovo Articolo", "Aumento Sell-out", "Fissare Formazione"])

bozza = st.text_area("Appunti veloci")

def create_outlook_link(subject, body):
    query = urllib.parse.quote(body)
    subject_query = urllib.parse.quote(subject)
    return f"mailto:?subject={subject_query}&body={query}"

if st.button("Genera 2 Versioni Strategiche"):
    if distributore and bozza:
        prompt = f"""
        Sei un Area Manager DPI. Scrivi DUE varianti di email per {distributore}.
        Profilo: {profilo}. Obiettivo: {obiettivo}. Oggetto: {oggetto}. Note: {bozza}.
        Separa le due versioni chiaramente con la scritta '---VERSIONE2---'.
        """
        try:
            response = model.generate_content(prompt).text
            
            if "---VERSIONE2---" in response:
                v1, v2 = response.split("---VERSIONE2---")
            else:
                v1, v2 = response, "Errore generazione versione 2"

            t1, t2 = st.tabs(["📌 Formale", "🤝 Relazionale"])
            with t1:
                st.code(v1, language="text")
                st.markdown(f'[📧 Apri in Outlook]({create_outlook_link(oggetto, v1)})')
            with t2:
                st.code(v2, language="text")
                st.markdown(f'[📧 Apri in Outlook]({create_outlook_link(oggetto, v2)})')
        except Exception as e:
            st.error(f"Errore: {e}")
    else:
        st.warning("Inserisci i dati!")
        
