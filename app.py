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

# --- 2. CONFIGURACIÓN (Tus datos confirmados) ---
PROJECT_ID = "subida-fotos-drive"
GEMINI_LOCATION = "europe-west1"
DATA_STORE_ID = "almacen-tasador-v2_1770407667877"
DATA_STORE_LOCATION = "eu" 

vertexai.init(
    project=PROJECT_ID, 
    location=GEMINI_LOCATION, 
    credentials=creds
)

# --- 3. HERRAMIENTAS (El "Tándem" ganador) ---
tools = [
    # Herramienta 1: Tu Bucket (vía Data Store)
    Tool.from_retrieval(
        grounding.Retrieval(
            grounding.VertexAISearch(
                datastore=DATA_STORE_ID,
                project=PROJECT_ID,
                location=DATA_STORE_LOCATION
            )
        )
    ),
    # Herramienta 2: Google Search (Para buscar en Milanuncios/Agriaffaires)
    Tool.from_google_search_retrieval(
        grounding.GoogleSearchRetrieval()
    )
]

# --- 4. MODELO ---
model = GenerativeModel(
    model_name="gemini-1.5-pro", 
    tools=tools
)

# --- 5. INTERFAZ ---
st.set_page_config(page_title="Tasador v2", layout="wide")
st.title("🚜 Tasador IA: El Putomilagro")

tractor = st.text_input("¿Qué tractor quieres tasar?", "John Deere 6150M")

if st.button("Tasar ahora"):
    if not tractor:
        st.warning("Escribe un modelo de tractor.")
    else:
        with st.spinner(f"Buscando precios reales para {tractor}..."):
            try:
                prompt = (
                    f"Busca anuncios reales actuales en España para el tractor: {tractor}. "
                    "Es obligatorio que presentes los resultados en una TABLA con estas columnas: "
                    "Modelo | Precio | Horas/Año | Fuente (URL del anuncio). "
                    "Si no encuentras el modelo exacto, busca los más similares."
                )

                response = model.generate_content(prompt)

                # --- VISUALIZACIÓN DE RESULTADOS ---
                st.markdown("### 📊 Informe de Tasación")
                
                # Intentamos sacar el texto de varias formas para no quedarnos en blanco
                texto_final = ""
                if response.text:
                    texto_final = response.text
                elif response.candidates and response.candidates[0].content.parts:
                    texto_final = response.candidates[0].content.parts[0].text
                
                if texto_final:
                    st.write(texto_final)
                else:
                    st.info("La IA no ha devuelto texto directo. Revisa las fuentes abajo.")

                # Mostramos las fuentes reales de internet que ha consultado
                with st.expander("🔗 Ver fuentes y enlaces consultados"):
                    if response.candidates[0].grounding_metadata.search_entry_point:
                        st.write("Datos extraídos de Google Search:")
                        st.write(response.candidates[0].grounding_metadata.search_entry_point.rendered_content)
                    else:
                        st.write("La información proviene de tu Data Store privado.")

            except Exception as e:
                st.error(f"❌ Error en la conexión: {str(e)}")

# Sidebar para info técnica
st.sidebar.markdown("---")
st.sidebar.info(f"**Proyecto:** {PROJECT_ID}\n\n**Data Store:** {DATA_STORE_ID}")
