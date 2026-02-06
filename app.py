import streamlit as st
import vertexai
from google.oauth2 import service_account
from vertexai.generative_models import GenerativeModel, Tool, GoogleSearchRetrieval

st.title("🚜 Buscador Agrícola")

# 1. CONEXIÓN (La base que dio éxito)
if "google" in st.secrets:
    try:
        creds_info = dict(st.secrets["google"])
        if "private_key" in creds_info:
            creds_info["private_key"] = creds_info["private_key"].replace("\\n", "\n")
        
        credentials = service_account.Credentials.from_service_account_info(creds_info)
        
        # Usamos la región europea que te funcionó en el PDF anterior
        vertexai.init(project=creds_info["project_id"], location="europe-west1", credentials=credentials)
        st.success("✅ Conexión europea establecida.")
    except Exception as e:
        st.error(f"Fallo de conexión: {e}")
        st.stop()

# 2. EL PASO ADELANTE: La Búsqueda
query = st.text_input("¿Qué tractor quieres encontrar?", value="John Deere 6155R")

if st.button("BUSCAR"):
    with st.spinner("Consultando portales europeos..."):
        try:
            # Aquí activamos la herramienta de búsqueda de Google
            search_tool = Tool.from_google_search_retrieval(GoogleSearchRetrieval())
            model = GenerativeModel("gemini-2.5-pro")
            
            # Le pedimos que busque específicamente en Europa como configuramos
            prompt = f"Busca ofertas de {query} en portales agrícolas de España y Europa. Dame precios y links."
            
            response = model.generate_content(prompt, tools=[search_tool])
            st.markdown(response.text)
        except Exception as e:
            st.error(f"Error en la búsqueda: {e}")
