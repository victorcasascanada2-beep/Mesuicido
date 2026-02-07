import streamlit as st
import vertexai
from google.oauth2 import service_account
from vertexai.generative_models import GenerativeModel, Tool, grounding

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

# --- 3. HERRAMIENTAS (SINTAXIS COMPATIBLE) ---
# Volvemos a 'grounding', pero sin pasarle parámetros para que
# el sistema intente elegir el nombre de campo correcto solo.
tools = [
    Tool.from_google_search_retrieval(
        google_search_retrieval=grounding.GoogleSearchRetrieval()
    )
]

# --- 4. MODELO (2.5 PRO) ---
model = GenerativeModel(
    model_name="gemini-2.5-pro", 
    tools=tools
)

# --- 5. INTERFAZ ---
st.title("🚜 Paso 1: Lista de Resultados (2.5 Pro)")

tractor = st.text_input("Modelo de tractor:", "John Deere 6150M")

if st.button("Buscar Anuncios"):
    with st.spinner("Conectando con Google..."):
        try:
            prompt = (
                f"Busca anuncios reales de {tractor} en España. "
                "Dame una lista con: Nombre del anuncio, Precio y URL."
            )
            
            # Generamos contenido de la forma más simple posible
            response = model.generate_content(prompt)

            st.markdown("### 📝 Resultados:")
            if response.candidates:
                st.write(response.candidates[0].content.parts[0].text)
            else:
                st.warning("No se recibieron resultados.")

        except Exception as e:
            st.error(f"Fallo técnico: {str(e)}")
            # Si vuelve a salir el error 400, el problema es la versión de la librería en Streamlit
            if "google_search_retrieval" in str(e):
                st.info("Sigue enviando el nombre antiguo. Intentaremos un último truco si esto falla.")
