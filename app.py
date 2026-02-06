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
PROJECT_ID = "236500839928" 
REGION_MODELO = "europe-west1" 
DATA_STORE_ID = "tasador-maquinaria-v1_1770401678792" 

# Inicializamos con tus credenciales reales
vertexai.init(project=PROJECT_ID, location=REGION_MODELO, credentials=creds)

def configurar_herramientas():
    return Tool.from_retrieval(
        grounding.Retrieval(
            grounding.VertexAISearch(
                datastore=DATA_STORE_ID,
                project=PROJECT_ID,
                location="eu" # Tu almacén de datos en Europa
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
