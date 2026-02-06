import streamlit as st
import vertexai
from google.oauth2 import service_account
from vertexai.generative_models import GenerativeModel, Tool, grounding

# --- 1. CREDENCIALES (Cargadas desde tus Secrets de Streamlit) ---
if "google" in st.secrets:
    creds_info = st.secrets["google"]
    creds = service_account.Credentials.from_service_account_info(creds_info)
else:
    st.error("❌ No encuentro las credenciales en Secrets ([google]).")
    st.stop()

# --- 2. CONFIGURACIÓN DE TU INFRAESTRUCTURA ---
PROJECT_ID = "subida-fotos-drive"
GEMINI_LOCATION = "europe-west1"
DATA_STORE_ID = "almacen-tasador-v2_1770407667877"
DATA_STORE_LOCATION = "eu" 

# Inicialización de Vertex AI con tus credenciales
vertexai.init(
    project=PROJECT_ID,
    location=GEMINI_LOCATION,
    credentials=creds
)

# --- 3. CONFIGURACIÓN DE HERRAMIENTAS (GROUNDING) ---
# Unimos tu "trastero" de archivos con el "buscador" de Google
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

# --- 5. INTERFAZ DE STREAMLIT ---
st.set_page_config(page_title="Tasador v2", layout="wide", page_icon="🚜")

st.title("🚜 Tasador IA: El Putomilagro")
st.markdown("""
Esta herramienta busca anuncios reales en **Milanuncios, Agriaffaires y Mascus**, 
comparándolos con tu base de datos privada en Google Cloud.
""")

# Input del usuario
tractor = st.text_input("Introduce el modelo de maquinaria:", "John Deere 6150M")

if st.button("Tasar ahora"):
    if not tractor:
        st.warning("Escribe algo para buscar.")
    else:
        with st.spinner(f"Rastreando el mercado para {tractor}..."):
            try:
                # El Prompt diseñado para que devuelva una tabla limpia
                prompt = (
                    f"Busca anuncios actuales de {tractor} en España. "
                    "Es obligatorio que presentes los resultados en una TABLA con: "
                    "Modelo | Precio | Horas | Fuente (URL del anuncio). "
                    "Al final, estima un precio medio basado en los resultados."
                )

                response = model.generate_content(prompt)

                # --- MOSTRAR RESULTADOS EN PANTALLA ---
                st.markdown("---")
                st.markdown(f"### 📊 Informe de Mercado: {tractor}")
                
                # Extraemos el texto de la respuesta de la IA
                if response.candidates:
                    resultado_texto = response.candidates[0].content.parts[0].text
                    st.write(resultado_texto)
                else:
                    st.error("La IA no ha podido generar una respuesta. Inténtalo de nuevo.")

                # Sección para ver las fuentes de Google
                with st.expander("🔗 Ver enlaces y fuentes consultadas"):
                    if response.candidates[0].grounding_metadata.search_entry_point:
                        html_fuentes = response.candidates[0].grounding_metadata.search_entry_point.rendered_content
                        st.write(html_fuentes, unsafe_allow_html=True)
                    else:
                        st.info("La información procede íntegramente de tu Data Store (
