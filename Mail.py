import streamlit as st
import google.generativeai as genai

# Configurazione API Gemini
genai.configure(api_key="LA_TUA_API_KEY")
model = genai.GenerativeModel('gemini-pro')

st.title("🚀 Sales Manager AI - Generatore Email Distributori")

# 1. Input Nome Cliente
nome_cliente = st.text_input("Nome Distributore", placeholder="Es: Rossi Antinfortunistica")

# 2. Oggetto
oggetto_mail = st.text_input("Oggetto dell'email")

# 3. Finalità (Selettore)
finalita = st.selectbox(
    "Finalità della comunicazione",
    ["Ringraziamento (Rilassato)", "Proposta Offerta (Schematico)", "Richiesta Appuntamento (Pragmatico)"]
)

# 4. Bozza Testo (Punti chiave)
bozza_input = st.text_area("Punti chiave da includere", placeholder="Es: visti ottimi risultati, proporre stock calzature S3 per stagione invernale")

if st.button("Genera Email"):
    if nome_cliente and bozza_input:
        # Definizione del prompt in base alla finalità
        istruzioni_stile = ""
        if "Ringraziamento" in finalita:
            istruzioni_stile = "Usa un tono rilassato e amichevole. Sottolinea l'importanza della partnership e il buon lavoro svolto."
        elif "Offerta" in finalita:
            istruzioni_stile = "Usa un tono schematico e professionale. Elenca i vantaggi commerciali e tecnici in modo chiaro (usa i bullet points)."
        else:
            istruzioni_stile = "Usa un tono pragmatico e diretto. Vai subito al punto e proponi una call o un incontro fissando un obiettivo."

        prompt = f"""
        Sei un Area Manager esperto di un'azienda produttrice di calzature antinfortunistiche (DPI).
        Scrivi un'email a un distributore partner.
        
        DETTAGLI:
        - Nome Distributore: {nome_cliente}
        - Oggetto: {oggetto_mail}
        - Stile richiesto: {istruzioni_stile}
        - Concetti da inserire: {bozza_input}
        
        Nota: L'email deve sembrare scritta da una persona reale, non da un robot.
        """

        with st.spinner('Gemini sta scrivendo per te...'):
            response = model.generate_content(prompt)
            st.subheader("Risultato:")
            st.write(response.text)
            st.button("Copia testo")
    else:
        st.error("Per favore, inserisci almeno il nome del cliente e i punti chiave.")
