import streamlit as st
import vertexai
from google.oauth2 import service_account
from vertexai.generative_models import GenerativeModel, Tool, grounding

# --- 1. CREDENCIALES (INTACTO) ---
if "google" in st.secrets:
    creds_info = st.secrets["google"]
    creds = service_account.Credentials.from_service_account_info(creds_info)
else:
    st.error("❌ Error en Secrets")
    st.stop()

# --- 2. CONFIGURACIÓN (Tus IDs reales) ---
PROJECT_ID = "subida-fotos-drive"
GEMINI_LOCATION = "europe-west1"
DATA_STORE_ID = "almacen-tasador-v2_1770407667877"
DATA_STORE_LOCATION = "eu"

vertexai.init(project=PROJECT_ID, location=GEMINI_LOCATION, credentials=creds)

# --- 3. HERRAMIENTAS (EL PARCHE DEL ERROR 400) ---
tools = [
    # Herramienta 1: Tu almacén de datos
    Tool.from_retrieval(
        grounding.Retrieval(
            grounding.VertexAISearch(
                datastore=DATA_STORE_ID,
                project=PROJECT_ID,
                location=DATA_STORE_LOCATION
            )
        )
    ),
    # Herramienta 2: Google Search (CON LA SINTAXIS QUE PIDE EL ERROR)
    Tool.from_google_search_retrieval(
        grounding.GoogleSearchRetrieval() 
    )
]

# --- 4. MODELO (Usamos 1.5-pro que es el que acepta este buscador en Europa) ---
model = GenerativeModel(
    model_name="gemini-1.5-pro", 
    tools=tools
)

# --- 5. INTERFAZ ---
st.title("🚜 Tasador IA: El Putomilagro")

tractor = st.text_input("Modelo del tractor:", "John Deere 6150M")

if st.button("Tasar ahora"):
    with st.spinner("Buscando en tiempo real..."):
        try:
            prompt = f"Busca anuncios de {tractor} en España. Dame una tabla con Modelo, Precio, Horas y URL."
            response = model.generate_content(prompt)
            
            # Mostramos el resultado
            if response.text:
                st.markdown(response.text)
            else:
                st.write(response.candidates[0].content.parts[0].text)

        except Exception as e:
            st.error(f"Error de Google: {str(e)}")
            st.info("Si el error 400 persiste, es que la función de búsqueda está caída en tu región.")
