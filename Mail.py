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

# Usiamo il nome corto 'gemini-1.5-flash' per massima compatibilità
model = genai.GenerativeModel('gemini-1.5-flash')

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

bozza = st.text_area("Appunti veloci (es. porto il pranzo martedì)")

def create_outlook_link(subject, body):
    query = urllib.parse.quote(body)
    subject_query = urllib.parse.quote(subject)
    return f"mailto:?subject={subject_query}&body={query}"

if st.button("Genera 2 Versioni Strategiche"):
    if distributore and bozza:
        prompt = f"""
        Sei un Area Manager esperto di calzature antinfortunistiche. 
        Scrivi DUE varianti di email diverse per il distributore {distributore}.
        Profilo: {profilo}. Obiettivo: {obiettivo}. Oggetto: {oggetto}. Note: {bozza}.
        
        VERSIONE 1: Tono formale, tecnico, focalizzato su efficienza e dati.
        VERSIONE 2: Tono relazionale, amichevole, focalizzato sulla partnership.
        
        IMPORTANTE: Separa le due versioni con la stringa esatta: ---VERSIONE2---
        """
        try:
            # Generazione contenuto
            response = model.generate_content(prompt).text
            
            if "---VERSIONE2---" in response:
                v1, v2 = response.split("---VERSIONE2---")
            else:
                v1, v2 = response, "Seconda versione non generata correttamente. Riprova."

            # Visualizzazione con TAB
            t1, t2 = st.tabs(["📌 Versione Formale", "🤝 Versione Relazionale"])
            
            with t1:
                st.write(v1)
                st.markdown(f'[📧 Apri in Outlook]({create_outlook_link(oggetto, v1)})')
            
            with t2:
                st.write(v2)
                st.markdown(f'[📧 Apri in Outlook]({create_outlook_link(oggetto, v2)})')
                
        except Exception as e:
            st.error(f"Errore di generazione: {e}. Prova a controllare la tua API Key.")
    else:
        st.warning("Inserisci il nome del distributore e qualche appunto per procedere!")
