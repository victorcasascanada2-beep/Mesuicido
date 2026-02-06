import streamlit as st
import vertexai
from google.oauth2 import service_account
from vertexai.generative_models import GenerativeModel, Tool, grounding

# --- 1. CREDENCIALES ---
if "google" in st.secrets:
    creds_info = st.secrets["google"]
    creds = service_account.Credentials.from_service_account_info(creds_info)
else:
    st.error("❌ No encuentro las credenciales en Secrets ([google]).")
    st.stop()

# --- 2. CONFIGURACIÓN ---
PROJECT_ID = "subida-fotos-drive"
GEMINI_LOCATION = "europe-west1"
DATA_STORE_ID = "almacen-tasador-v2_1770407667877"
DATA_STORE_LOCATION = "eu" 

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
                datastore=DATA_STORE_ID,
                project=PROJECT_ID,
                location=DATA_STORE_LOCATION
            )
        )
    ),
    Tool.from_google_search_retrieval(
        grounding.GoogleSearchRetrieval()
    )
]

# --- 4. MODELO (Tu versión Gemini 2.5 Pro) ---
model = GenerativeModel(
    model_name="gemini-2.5-pro", 
    tools=tools
)

# --- 5. INTERFAZ ---
st.set_page_config(page_title="Tasador v2", layout="wide")
st.title("🚜 Tasador IA: El Putomilagro")

tractor = st.text_input("Modelo del tractor:", "John Deere 6150M")

if st.button("Tasar ahora"):
    if not tractor:
        st.warning("Escribe un modelo de tractor.")
    else:
        with st.spinner(f"Buscando precios para {tractor}..."):
            try:
                prompt = (
                    f"Busca anuncios actuales de {tractor} en España. "
                    "Devuélveme una tabla con: Modelo | Precio | Horas | Fuente (URL)."
                )

                response = model.generate_content(prompt)

                st.markdown("### 📊 Resultado")
                
                if response.candidates:
                    resultado = response.candidates[0].content.parts[0].text
                    st.write(resultado)
                else:
                    st.error("La IA no devolvió resultados.")

                with st.expander("🔗 Ver fuentes consultadas"):
                    if response.candidates[0].grounding_metadata.search_entry_point:
                        st.write(response.candidates[0].grounding_metadata.search_entry_point.rendered_content, unsafe_allow_html=True)
                    else:
                        st.info("Información del Data Store privado.")

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

st.sidebar.info(f"Data Store: {DATA_STORE_ID}")
