import streamlit as st
import vertexai
from google.oauth2 import service_account
from vertexai.generative_models import GenerativeModel, Tool, grounding

# --- 1. CREDENCIALES ---
if "google" in st.secrets:
    creds_info = st.secrets["google"]
    creds = service_account.Credentials.from_service_account_info(creds_info)
else:
    st.error("❌ Revisa los Secrets en Streamlit.")
    st.stop()

# --- 2. CONFIGURACIÓN ---
PROJECT_ID = "subida-fotos-drive"
LOCATION = "europe-west1" # Región de Bélgica, la más estable para esto

vertexai.init(project=PROJECT_ID, location=LOCATION, credentials=creds)

# --- 3. HERRAMIENTAS (Solo buscador de Google para este paso) ---
# Vamos a probar PRIMERO que internet funciona. Si esto va, luego metemos tu Data Store.
tools = [
    Tool.from_google_search_retrieval(
        grounding.GoogleSearchRetrieval()
    )
]

# --- 4. MODELO ---
model = GenerativeModel(model_name="gemini-1.5-pro", tools=tools)

# --- 5. INTERFAZ SIMPLE ---
st.title("🚜 Paso 1: Lista de Resultados")

tractor = st.text_input("Modelo de tractor:", "John Deere 6150M")

if st.button("Buscar Anuncios"):
    with st.spinner("Buscando en Milanuncios, Agriaffaires, etc..."):
        try:
            # Prompt directo para obtener una LISTA
            prompt = f"Busca anuncios reales de {tractor} en venta en España. Dame una lista con el nombre del anuncio, el precio y el enlace."
            
            response = model.generate_content(prompt)

            # Mostramos el resultado tal cual viene
            st.markdown("### 📝 Resultados encontrados:")
            if response.text:
                st.write(response.text)
            else:
                # Si el texto directo falla, sacamos la parte cruda
                st.write(response.candidates[0].content.parts[0].text)

        except Exception as e:
            st.error(f"❌ Fallo en el Paso 1: {str(e)}")
