import streamlit as st
import vertexai
from vertexai.generative_models import GenerativeModel
from google.oauth2 import service_account

st.title("🚜 Probando Gemini 2.5 Pro")

if "google" in st.secrets:
    creds_info = dict(st.secrets["google"])
    if "private_key" in creds_info:
        creds_info["private_key"] = creds_info["private_key"].replace("\\n", "\n")
    
    try:
        credentials = service_account.Credentials.from_service_account_info(creds_info)
        
        # CAMBIO: Usamos europe-west1 que SI está en tu lista permitida
        vertexai.init(
            project=creds_info["project_id"], 
            location="europe-west1", 
            credentials=credentials
        )
        
        st.success(f"Conectado a {creds_info['project_id']} en Europe-West1")

        if st.button("Lanzar ráfaga a Gemini 2.5"):
            # Usamos el nombre que viste en tu consola
            model = GenerativeModel("gemini-2.5-pro")
            
            with st.spinner("Consultando al cerebro 2.5..."):
                response = model.generate_content("Confirma conexión en europe-west1")
                st.markdown(f"### Respuesta:\n{response.text}")
                
    except Exception as e:
        st.error(f"Error técnico detallado: {e}")
