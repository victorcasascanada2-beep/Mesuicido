import streamlit as st
import vertexai
from google.oauth2 import service_account

# Importamos las piezas base confirmadas
from vertexai.generative_models import GenerativeModel, Tool

st.title("🚜 Localizador de Maquinaria")

# 1. Configuración de Variables
PROJECT_ID = st.secrets["google"]["project_id"]
LOCATION = "us-central1" # Donde tienes el consumo activo

def configurar_herramientas():
    """Configura el buscador usando la ruta exacta hallada en tu servidor"""
    import vertexai.generative_models as gm
    # Usamos la ruta confirmada: gm.grounding.GoogleSearchRetrieval
    search_query_tool = Tool.from_google_search_retrieval(
        google_search_retrieval=gm.grounding.GoogleSearchRetrieval()
    )
    return search_query_tool

def ejecutar_busqueda(modelo_tractor):
    """Lógica de búsqueda con Gemini 2.5 Pro"""
    try:
        herramientas = [configurar_herramientas()]
        model = GenerativeModel("gemini-2.5-pro")
        
        prompt = f"Busca ofertas actuales de {modelo_tractor} en España. Incluye precio y link."
        
        response = model.generate_content(prompt, tools=herramientas)
        return response.text
    except Exception as e:
        return f"Error en la consulta: {e}"

# 2. Interfaz de Usuario
if "google" in st.secrets:
    try:
        creds = dict(st.secrets["google"])
        creds["private_key"] = creds["private_key"].replace("\\n", "\n")
        credentials = service_account.Credentials.from_service_account_info(creds)
        
        vertexai.init(project=PROJECT_ID, location=LOCATION, credentials=credentials)
        st.success(f"✅ Conectado a {LOCATION} con Gemini 2.5 Pro")
        
        tractor = st.text_input("Introduce marca y modelo:", "John Deere 6155R")
        if st.button("BUSCAR AHORA"):
            with st.spinner("Buscando en tiempo real..."):
                resultado = ejecutar_busqueda(tractor)
                st.markdown(resultado)
                
    except Exception as e:
        st.error(f"Fallo de inicialización: {e}")
