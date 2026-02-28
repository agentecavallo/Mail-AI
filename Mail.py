        import streamlit as st
import google.generativeai as genai

# 1. Configurazione Sicurezza (Legge dai Secrets di Streamlit)
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except:
    st.error("⚠️ Errore: API Key non configurata. Vai in Settings > Secrets su Streamlit Cloud.")
    st.stop()

# Inizializza il modello (1.5-flash è ottimo per le email)
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="Area Manager AI Assistant", page_icon="👞")

st.title("👞 Assistant Area Manager")
st.markdown("---")

# --- INTERFACCIA ---
col1, col2 = st.columns(2)

with col1:
    nome_cliente = st.text_input("Distributore", placeholder="Es: Rossi Srl")
    oggetto_mail = st.text_input("Oggetto", placeholder="Es: Nuova collezione 2026")

with col2:
    finalita = st.selectbox(
        "Finalità",
        ["Ringraziamento (Rilassato)", "Proposta Offerta (Schematico)", "Richiesta Appuntamento (Pragmatico)"]
    )

bozza_input = st.text_area("Cosa vuoi scrivere? (Bozza veloce)", 
                            placeholder="Es: ringrazia per l'ordine, proponi campionario estivo, sottolinea sconti volume")

# --- LOGICA DI GENERAZIONE ---
if st.button("Genera Email"):
    if not nome_cliente or not bozza_input:
        st.warning("Compila il nome del distributore e la bozza per continuare.")
    else:
        # Prompt dinamico basato sulla finalità
        if "Ringraziamento" in finalita:
            stile = "tono rilassato, amichevole ma professionale, focus sul rapporto di partnership."
        elif "Offerta" in finalita:
            stile = "tono schematico, usa bullet points per i vantaggi, focus su margini e disponibilità."
        else:
            stile = "tono pragmatico e diretto, focus sull'agenda e sull'efficienza."

        prompt = f"""
        Sei un esperto Area Manager di un'azienda di calzature antinfortunistiche (DPI).
        Scrivi un'email a un distributore partner seguendo queste istruzioni:
        - Destinatario: {nome_cliente}
        - Oggetto: {oggetto_mail}
        - Stile: {stile}
        - Punti chiave da includere: {bozza_input}
        
        Importante: Scrivi in un italiano naturale, fluido e professionale. Evita frasi fatte da robot.
        """

        with st.spinner('Scrittura in corso...'):
            try:
                response = model.generate_content(prompt)
                st.markdown("### Email Generata:")
                st.code(response.text, language="text") # Il formato code facilita il copia-incolla
            except Exception as e:
                st.error(f"Si è verificato un errore: {e}")

st.markdown("---")
st.caption("Strumento riservato - Settore DPI Calzature")
