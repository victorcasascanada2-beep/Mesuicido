import streamlit as st
import vertexai
from google.oauth2 import service_account
from vertexai.generative_models import GenerativeModel, Tool, GoogleSearchRetrieval # Importación directa

# --- 1. CREDENCIALES (INTACTO) ---
if "google" in st.secrets:
    creds_info = st.secrets["google"]
    creds = service_account.Credentials.from_service_account_info(creds_info)
else:
    st.error("❌ Revisa los Secrets.")
    st.stop()

# --- 2. CONFIGURACIÓN ---
PROJECT_ID = "subida-fotos-drive"
LOCATION = "europe-west1" 

vertexai.init(project=PROJECT_ID, location=LOCATION, credentials=creds)

# --- 3. HERRAMIENTAS (LA SOLUCIÓN AL ERROR 400) ---
# En lugar de grounding.GoogleSearchRetrieval, usamos la clase directa 
# que ya viene configurada para enviar el campo 'google_search'
tools = [
    Tool.from_google_search_retrieval(
        google_search_retrieval=GoogleSearchRetrieval() 
    )
]

# --- 4. MODELO (TU 2.5 PRO) ---
model = GenerativeModel(
    model_name="gemini-2.5-pro", 
    tools=tools
)

# --- 5. INTERFAZ ---
st.title("🚜 Paso 1: Lista de Resultados (2.5 Pro)")

tractor = st.text_input("Modelo de tractor:", "John Deere 6150M")

if st.button("Buscar Anuncios"):
    with st.spinner("Conectando con la nueva API de Google..."):
        try:
            prompt = (
                f"Busca anuncios reales de {tractor} en España. "
                "Dame una lista con: Nombre, Precio y URL."
            )
            
            # Llamada limpia
            response = model.generate_content(prompt)

            st.markdown("### 📝 Resultados:")
            if response.candidates:
                st.write(response.candidates[0].content.parts[0].text)
            else:
                st.warning("No se recibieron resultados.")

        except Exception as e:
            st.error(f"Fallo técnico: {str(e)}")
            st.info("Si el 400 persiste, es que Google exige actualizar la librería 'google-cloud-aiplatform'.")
