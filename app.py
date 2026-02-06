import streamlit as st
import vertexai
from google.oauth2 import service_account
from vertexai.generative_models import GenerativeModel, Tool, grounding

# --- 1. CREDENCIALES ---
# Se asume que en Streamlit Secrets tienes:
# [google]
# type = "service_account"
# project_id = "subida-fotos-drive"
# ...

if "google" in st.secrets:
    creds_info = st.secrets["google"]
    creds = service_account.Credentials.from_service_account_info(creds_info)
else:
    st.error("❌ No encuentro las credenciales en Secrets ([google]).")
    st.stop()

# --- 2. CONFIGURACIÓN CORRECTA ---
# ID del proyecto (NO el número, sino el ID)
PROJECT_ID = "subida-fotos-drive"

# 👉 Gemini (modelos generativos) en Europa
GEMINI_LOCATION = "europe-west1"

# 👉 Vertex AI Search / Data Store
DATA_STORE_ID = "almacen-tasador-v2_1770407667877"
DATA_STORE_LOCATION = "eu"  # ❌ NO global, según tu consola

# Inicialización de Vertex AI
vertexai.init(
    project=PROJECT_ID,
    location=GEMINI_LOCATION,
    credentials=creds
)

# --- 3. HERRAMIENTAS ---
tools = [
    Tool.from_retrieval(
        grounding.Retrieval(
            grounding.VertexAISearch(
                datastore=DATA_STORE_ID,   # ✅ SOLO el ID
                project=PROJECT_ID,
                location=DATA_STORE_LOCATION
            )
        )
    )
]

# --- 4. MODELO ---
# ✅ Versión estable y disponible en Europa
model = GenerativeModel(
    model_name="gemini-2.5-pro",
    tools=tools
)

# --- 5. INTERFAZ ---
st.set_page_config(page_title="Tasador v2", layout="wide")
st.title("🚜 Tasador IA: El Putomilagro")

tractor = st.text_input("Modelo del tractor:", "John Deere 6150M")

if st.button("Tasar ahora"):
    with st.spinner("Buscando precios reales..."):
        try:
            prompt = (
                f"Busca anuncios reales de {tractor} en España. "
                "Devuélveme una tabla con columnas: "
                "Modelo | Precio | Horas | Fuente (URL). "
                "Usa solo datos reales y cita la fuente."
            )

            response = model.generate_content(prompt)

            st.markdown("### 📊 Resultado")
            st.write(response.text)

        except Exception as e:
            st.error(f"❌ Error en la búsqueda: {str(e)}")

st.sidebar.info(f"Conectado al Data Store: {DATA_STORE_ID}")
