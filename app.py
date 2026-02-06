import streamlit as st
import vertexai
from google.oauth2 import service_account
from vertexai.generative_models import GenerativeModel, Tool, grounding

# --- 1. CONEXIÓN CON STREAMLIT CLOUD SECRETS ---
# Leemos el bloque [google_cloud] de tu panel de Secrets
if "google_cloud" in st.secrets:
    creds_info = st.secrets["google_cloud"]
    # Forzamos la creación del objeto de credenciales para que Vertex no busque el servidor de Google
    creds = service_account.Credentials.from_service_account_info(creds_info)
else:
    st.error("❌ No encuentro la sección [google_cloud] en los Secrets de Streamlit.")
    st.stop()

# --- 2. CONFIGURACIÓN DEL LABORATORIO ---
PROJECT_ID = "236500839928" 
REGION_MODELO = "europe-west1" # Región válida para Gemini
# ID de tu motor en Europa
DATA_STORE_ID = "tasador-maquinaria-v1_1770400616700" 

# Inicialización CRUCIAL para Streamlit Cloud: pasamos las credenciales explícitamente
vertexai.init(project=PROJECT_ID, location=REGION_MODELO, credentials=creds)

def configurar_herramientas():
    """Conecta con el buscador usando los nombres que el log nos confirmó"""
    return Tool.from_retrieval(
        grounding.Retrieval(
            grounding.VertexAISearch(
                datastore=DATA_STORE_ID, # El nombre 'datastore' es el que pidió el log
                project=PROJECT_ID,
                location="eu" # El buscador vive en la multirregión eu
            )
        )
    )

def ejecutar_busqueda(modelo_tractor):
    try:
        model = GenerativeModel("gemini-1.5-pro") 
        prompt = f"""
        Busca ofertas de {modelo_tractor} en España. 
        Usa tus fuentes (Milanuncios, Agriaffaires).
        Dame una tabla con: Modelo, Precio, Horas y Link.
        Calcula un precio medio al final.
        """
        # Enviamos la consulta al laboratorio de Google en Europa
        response = model.generate_content(prompt, tools=[configurar_herramientas()])
        return response.text
    except Exception as e:
        return f"⚠️ Error en el laboratorio: {str(e)}"

# --- INTERFAZ ---
st.title("🚜 Tasador IA - Entorno Laboratorio")
modelo = st.text_input("Modelo del tractor:", "John Deere 6150M")

if st.button("Tasar ahora"):
    with st.spinner("Conectando Streamlit Cloud con Vertex AI Europa..."):
        st.markdown(ejecutar_busqueda(modelo))
