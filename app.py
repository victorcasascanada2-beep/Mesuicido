import streamlit as st
import vertexai
from google.oauth2 import service_account
from vertexai.generative_models import GenerativeModel, Tool, grounding

# --- 1. CREDENCIALES ---
if "google" in st.secrets:
    creds_info = st.secrets["google"]
    creds = service_account.Credentials.from_service_account_info(creds_info)
else:
    st.error("❌ Revisa los Secrets.")
    st.stop()

# --- 2. CONFIGURACIÓN (TUS DATOS) ---
PROJECT_ID = "subida-fotos-drive"
LOCATION = "europe-west1" 

vertexai.init(project=PROJECT_ID, location=LOCATION, credentials=creds)

# --- 3. HERRAMIENTAS ---
# Solo el buscador de Google para validar que el 2.5 Pro conecta a internet
tools = [
    Tool.from_google_search_retrieval(
        grounding.GoogleSearchRetrieval()
    )
]

# --- 4. MODELO (2.5 PRO, COMO DEBE SER) ---
model = GenerativeModel(
    model_name="gemini-2.5-pro", 
    tools=tools
)

# --- 5. INTERFAZ ---
st.title("🚜 Paso 1: Lista con Gemini 2.5 Pro")

tractor = st.text_input("Modelo de tractor:", "John Deere 6150M")

if st.button("Buscar Anuncios"):
    with st.spinner("Rastreando mercado con 2.5 Pro..."):
        try:
            # Prompt simple para asegurar que la respuesta sea una lista
            prompt = f"Busca anuncios reales de {tractor} en España. Dame una lista con: Nombre, Precio y URL."
            
            # Llamada directa sin argumentos extra que causen error
            response = model.generate_content(prompt)

            st.markdown("### 📝 Resultados:")
            if response.candidates:
                st.write(response.candidates[0].content.parts[0].text)
            else:
                st.warning("No se encontraron resultados.")

        except Exception as e:
            st.error(f"❌ Error con 2.5 Pro: {str(e)}")
