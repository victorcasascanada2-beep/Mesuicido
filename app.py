import streamlit as st
import vertexai
from vertexai.generative_models import GenerativeModel, Tool, GoogleSearchRetrieval
from google.oauth2 import service_account

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Buscador EU", page_icon="🚜")

if "google" in st.secrets:
    creds_info = dict(st.secrets["google"])
    # Limpieza de clave para asegurar que el formato sea correcto
    if "private_key" in creds_info:
        creds_info["private_key"] = creds_info["private_key"].replace("\\n", "\n")
    
    try:
        credentials = service_account.Credentials.from_service_account_info(creds_info)
        # Inicializamos en 'eu' que es tu configuración de Agent Builder
        vertexai.init(project=creds_info["project_id"], location="eu", credentials=credentials)
        st.success("✅ Librerías cargadas y Vertex AI inicializado en EU")
        
        if st.button("Hacer Ping a Gemini 1.5 Pro"):
            model = GenerativeModel("gemini-1.5-pro")
            response = model.generate_content("Di 'Conexión exitosa en Europa'")
            st.write(response.text)
            
    except Exception as e:
        st.error(f"Error de inicialización: {e}")
else:
    st.error("Faltan los Secrets de Google")
