import streamlit as st
import google.generativeai as genai
import urllib.parse

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
st.markdown("---")

# --- INTERFACCIA ---
col1, col2 = st.columns(2)
with col1:
    distributore = st.text_input("Nome Distributore", placeholder="Es: Rossi Sicurezza")
    oggetto = st.text_input("Oggetto Mail", placeholder="Es: Aggiornamento Listino Calzature")

with col2:
    profilo = st.selectbox("Profilo Partner", ["Partner Storico", "Nuovo Lead", "Recupero Rapporto"])
    obiettivo = st.selectbox("Obiettivo", ["Svuotare Magazzino", "Inserimento Nuovo Articolo", "Aumento Sell-out", "Fissare Formazione"])

bozza = st.text_area("Appunti veloci per la mail", placeholder="Es: visti ottimi risultati mese scorso, proporre nuova linea S3S traspirante...")

# Funzione per creare il link di Outlook
def create_outlook_link(subject, body):
    query = urllib.parse.quote(body)
    subject_query = urllib.parse.quote(subject)
    return f"mailto:?subject={subject_query}&body={query}"

if st.button("Genera 2 Versioni Strategiche"):
    if distributore and bozza:
        prompt = f"""
        Sei un Area Manager nel settore DPI calzature. Scrivi DUE varianti di email per {distributore}.
        Profilo: {profilo}. Obiettivo: {obiettivo}. Oggetto: {oggetto}. Note: {bozza}.
        
        VERSIONE 1: Formale e precisa, focalizzata sui dati e sui vantaggi tecnici.
        VERSIONE 2: Più colloquiale e relazionale, focalizzata sulla partnership e sul supporto.
        
        Separa le due versioni chiaramente con la scritta "---VERSIONE2---".
        Usa un italiano fluido da professionista B2B.
        """
        
        with st.spinner('Gemini sta scrivendo...'):
            response = model.generate_content(prompt).text
            
            if "---VERSIONE2---" in response:
                v1, v2 = response.split("---VERSIONE2---")
            else:
                v1, v2 = response, "Errore nella generazione della seconda versione."

            # Creazione delle TAB per visualizzare le 2 versioni
            tab1, tab2 = st.tabs(["📌 Versione Formale", "🤝 Versione Relazionale"])

            with tab1:
                st.code(v1, language="text")
                link_v1 = create_outlook_link(oggetto, v1)
                st.markdown(f'<a href="{link_v1}" target="_blank" style="background-color: #0078d4; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">📧 Apri in Outlook (V1)</a>', unsafe_allow_html=True)

            with tab2:
                st.code(v2, language="text")
                link_v2 = create_outlook_link(oggetto, v2)
                st.markdown(f'<a href="{link_v2}" target="_blank" style="background-color: #0078d4; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">📧 Apri in Outlook (V2)</a>', unsafe_allow_html=True)
    else:
        st.warning("Inserisci i dati necessari!")

st.markdown("---")
st.caption("Strumento Area Manager - Settore DPI")
