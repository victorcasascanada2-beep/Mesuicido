import streamlit as st
import vertexai
from google.oauth2 import service_account
from vertexai.generative_models import GenerativeModel, Tool, grounding

# --- 1. CONEXIÓN CORREGIDA A TUS SECRETS ---
# Cambiamos "google_cloud" por "google" que es como lo tienes tú
if "google" in st.secrets:
    creds_info = st.secrets["google"]
    creds = service_account.Credentials.from_service_account_info(creds_info)
else:
    st.error("❌ Sigo sin encontrar la sección en Secrets. Asegúrate de que en el panel pone [google].")
    st.stop()

# --- 2. CONFIGURACIÓN ---
PROJECT_ID = "236500839928" import streamlit as st
import os
from google.cloud import aiplatform
from vertexai.generative_models import GenerativeModel, Tool, grounding

# --- CONFIGURACIÓN DE GOOGLE CLOUD ---
PROJECT_ID = "tasador-maquinaria" # Tu ID de proyecto
LOCATION = "europe-west1"         # Tu región en Europa
# ESTE ES TU NUEVO ID GANADOR:
DATA_STORE_ID = "datastore-maquinaria-v1_1770401775478" 
DATA_STORE_LOCATION = "eu"

# Inicializar Vertex AI
aiplatform.init(project=PROJECT_ID, location=LOCATION)

# --- CONFIGURACIÓN DE HERRAMIENTAS (GROUNDING) ---
# Usamos el Data Store que creaste Y Google Search para que no pida permisos
herramientas = [
    Tool.from_google_search_retrieval(
        grounding.GoogleSearchRetrieval()
    ),
    Tool.from_retrieval(
        grounding.Retrieval(
            grounding.VertexAISearch(
                datastore_id=DATA_STORE_ID,
                project=PROJECT_ID,
                location=DATA_STORE_LOCATION,
            )
        )
    ),
]

# --- MODELO DE IA ---
model = GenerativeModel(
    model_name="gemini-1.5-pro",
    tools=herramientas
)

# --- INTERFAZ DE STREAMLIT ---
st.set_page_config(page_title="Tasador Experto de Tractores", layout="wide")
st.title("🚜 El Putomilagro: Tasador de Maquinaria v2")
st.subheader("Búsqueda libre en internet sin bloqueos de dominio")

tractor_query = st.text_input("¿Qué tractor quieres tasar?", placeholder="Ej: John Deere 6155R del 2019 con 5000 horas")

if st.button("Buscar Precios Reales"):
    if tractor_query:
        with st.spinner("Buscando en Milanuncios, Agriaffaires y más..."):
            try:
                prompt = f"""
                Actúa como un tasador profesional de maquinaria agrícola. 
                Busca en internet precios actuales para: {tractor_query}.
                
                Genera una tabla con:
                1. Modelo exacto
                2. Precio
                3. Horas/Año
                4. Fuente (la web donde está el anuncio)
                
                Al final, calcula un precio medio de mercado.
                """
                
                response = model.generate_content(prompt)
                
                # Mostrar resultado
                st.markdown("### 📊 Resultado de la Tasación")
                st.write(response.text)
                
            except Exception as e:
                st.error(f"Error: {e}")
                st.info("Asegúrate de haber ejecutado 'gcloud auth application-default login' en tu terminal.")
    else:
        st.warning("Introduce un modelo de tractor.")
REGION_MODELO = "europe-west1" 
DATA_STORE_ID = "tasador-maquinaria-v1_1770401678792" 

# Inicializamos con tus credenciales reales
vertexai.init(project=PROJECT_ID, location=REGION_MODELO, credentials=creds)

def configurar_herramientas():
    # Creamos la ruta completa. Esto obliga a la API a ir a 'eu' y buscar el ID exacto.
    # A veces el datastore solo con el ID no basta cuando se usa 'eu'.
    nombre_completo_datastore = f"projects/{PROJECT_ID}/locations/eu/collections/default_collection/dataStores/{DATA_STORE_ID}"
    
    return Tool.from_retrieval(
        grounding.Retrieval(
            grounding.VertexAISearch(
                datastore=nombre_completo_datastore, # <--- Pasamos la ruta completa aquí
                project=PROJECT_ID,
                location="eu" 
            )
        )
    )

def ejecutar_busqueda(modelo_tractor):
    try:
        model = GenerativeModel("gemini-2.5-pro") 
        prompt = f"Busca ofertas de {modelo_tractor} en España. Dame una tabla con Modelo, Precio y Link."
        
        # El spinner debería dejar de girar y soltar la respuesta
        response = model.generate_content(prompt, tools=[configurar_herramientas()])
        return response.text
    except Exception as e:
        return f"⚠️ Error en el laboratorio: {str(e)}"

# --- INTERFAZ ---
st.title("🚜 Tasador IA - Laboratorio Streamlit")
modelo = st.text_input("Modelo del tractor:", "John Deere 6150M")

if st.button("Tasar ahora"):
    with st.spinner("Conectando con tus fuentes en Europa..."):
        st.markdown(ejecutar_busqueda(modelo))
