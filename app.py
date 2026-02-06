import streamlit as st
import vertexai
from vertexai.generative_models import GenerativeModel
from google.oauth2 import service_account

st.title("🚜 Probando Gemini 2.5 Pro")

if "google" in st.secrets:
    creds_info = dict(st.secrets["google"])
    # Limpiamos la clave privada por si acaso
    if "private_key" in creds_info:
        creds_info["private_key"] = creds_info["private_key"].replace("\\n", "\n")
    
    try:
        credentials = service_account.Credentials.from_service_account_info(creds_info)
        
        # IMPORTANTE: Usamos 'eu' y el proyecto correcto
        vertexai.init(
            project=creds_info["project_id"], 
            location="eu", 
            credentials=credentials
        )
        
        st.success(f"Conectado a {creds_info['project_id']} en la región EU")

        if st.button("Lanzar ráfaga a Gemini 2.5"):
            # Usamos el nombre exacto de tu captura
            model = GenerativeModel("gemini-2.5-pro")
            
            with st.spinner("Consultando al cerebro 2.5..."):
                response = model.generate_content("Hola, confirma que eres Gemini 2.5 Pro y que la conexión es correcta.")
                st.markdown(f"### Respuesta de la IA:\n{response.text}")
                
    except Exception as e:
        st.error(f"Error técnico: {e}")
else:
    st.error("No se detectan los Secrets.")
