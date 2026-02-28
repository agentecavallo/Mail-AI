import streamlit as st
import google.generativeai as genai

# 1. Configurazione Sicurezza (Recupero dai Secrets)
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except:
    st.error("⚠️ Errore: API Key non trovata. Controlla i Secrets su Streamlit Cloud.")
    st.stop()

model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="Area Manager AI", page_icon="👞")
st.title("👞 Assistant Area Manager")
st.markdown("---")

# --- NUOVA INTERFACCIA CON PUNTI 1 E 3 ---

# Riga 1: Dati Base
col1, col2 = st.columns(2)
with col1:
    distributore = st.text_input("Nome Distributore", placeholder="Es: TecnoSafety Srl")
with col2:
    oggetto = st.text_input("Oggetto Mail", placeholder="Es: Promo scarpe estive")

# Riga 2: Strategia (Punto 1 e 3)
col3, col4 = st.columns(2)
with col3:
    profilo = st.selectbox(
        "Profilo Partner (Punto 1)",
        ["Partner Storico (Tono caldo)", "Nuovo Lead (Tono professionale)", "Recupero Rapporto (Tono empatico)"]
    )
with col4:
    obiettivo = st.selectbox(
        "Obiettivo Commerciale (Punto 3)",
        ["Svuotare Magazzino", "Inserimento Nuovo Articolo", "Aumento Sell-out", "Fissare Formazione Tecnica"]
    )

# Riga 3: Contenuto Libero
bozza = st.text_area("Cosa vuoi comunicare? (Appunti veloci)", 
                      placeholder="Es: ordini ottimi, presentare nuova linea S3, sconto 5% per ordini entro venerdì")

# --- GENERAZIONE ---
if st.button("Genera Email Strategica"):
    if distributore and bozza:
        prompt = f"""
        Sei un Area Manager esperto nel settore DPI e calzature antinfortunistiche.
        Scrivi un'email a un distributore con queste caratteristiche:
        - Nome: {distributore}
        - Profilo Relazionale: {profilo}
        - Obiettivo Principale: {obiettivo}
        - Oggetto: {oggetto}
        - Note dell'utente: {bozza}
        
        REGOLE:
        1. Se il profilo è 'Partner Storico', usa un linguaggio che valorizzi la collaborazione passata.
        2. Se l'obiettivo è 'Fissare Formazione', sottolinea come questo aiuterà i suoi venditori a chiudere più contratti.
        3. Scrivi in un italiano fluido, da professionista a professionista, evitando lo stile 'robotico'.
        """
        
        with st.spinner('Elaborazione strategia in corso...'):
            try:
                response = model.generate_content(prompt)
                st.subheader("Email Pronta:")
                st.code(response.text, language="text")
            except Exception as e:
                st.error(f"Errore durante la generazione: {e}")
    else:
        st.warning("Inserisci almeno il nome del distributore e una bozza di testo.")
