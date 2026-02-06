import streamlit as st
import vertexai
from google.oauth2 import service_account
from vertexai.generative_models import GenerativeModel, Tool, grounding

# --- 1. CREDENCIALES (INTACTO) ---
if "google" in st.secrets:
    creds_info = st.secrets["google"]
    creds = service_account.Credentials.from_service_account_info(creds_info)
else:
    st.error("❌ No encuentro las credenciales en Secrets ([google]).")
    st.stop()

# --- 2. CONFIGURACIÓN CORRECTA (INTACTO) ---
PROJECT_ID = "subida-fotos-drive"
GEMINI_LOCATION = "europe-west1"
DATA_STORE_ID = "almacen-tasador-v2_1770407667877"
DATA_STORE_LOCATION = "eu"

vertexai.init(
    project=PROJECT_ID,
    location=GEMINI_LOCATION,
    credentials=creds
)

# --- 3. HERRAMIENTAS (AJUSTADO PARA EVITAR ERROR 400) ---
tools = [
    # Tu conexión al Data Store (INTACTO)
    Tool.from_retrieval(
        grounding.Retrieval(
            grounding.VertexAISearch(
                datastore=DATA_STORE_ID,
                project=PROJECT_ID,
                location=DATA_STORE_LOCATION
            )
        )
    ),
    # Google Search corregido según la nueva documentación de Vertex AI
    Tool.from_google_search_retrieval(
        grounding.GoogleSearchRetrieval()
    )
]

# --- 4. MODELO (INTACTO) ---
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
            
            # Gestión de respuesta para asegurar que se pinte en pantalla
            if response.text:
                st.write(response.text)
            else:
                # Si response.text falla por seguridad, usamos la ruta directa al contenido
                st.write(response.candidates[0].content.parts[0].text)

            # Opcional: Mostrar las fuentes de Google Search debajo
            if response.candidates[0].grounding_metadata.search_entry_point:
                with st.expander("Ver fuentes oficiales"):
                    st.write(response.candidates[0].grounding_metadata.search_entry_point.rendered_content, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"❌ Error en la búsqueda: {str(e)}")

st.sidebar.info(f"Conectado al Data Store: {DATA_STORE_ID}")
