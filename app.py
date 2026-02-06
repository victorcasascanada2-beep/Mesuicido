import streamlit as st
import vertexai
from vertexai.generative_models import GenerativeModel
from google.oauth2 import service_account
from google.cloud import aiplatform

st.title("🔍 Escáner de Modelos Disponibles")

if "google" in st.secrets:
    creds_info = dict(st.secrets["google"])
    creds_info["private_key"] = creds_info["private_key"].replace("\\n", "\n")
    credentials = service_account.Credentials.from_service_account_info(creds_info)
    
    # Probamos con 'europe-west1' o 'us-central1'
    REGION = "us-central1" 
    
    try:
        vertexai.init(project=creds_info["project_id"], location=REGION, credentials=credentials)
        st.success(f"Conectado al proyecto: {creds_info['project_id']}")
        
        # Intentamos listar modelos o probar los más comunes
        test_models = ["gemini-1.0-pro", "gemini-1.5-pro-002", "gemini-pro"]
        
        st.subheader("Probando disponibilidad:")
        for m_name in test_models:
            try:
                model = GenerativeModel(m_name)
                # Un test rápido sin búsqueda, solo texto
                response = model.generate_content("test", generation_config={"max_output_tokens": 5})
                st.write(f"✅ **{m_name}**: DISPONIBLE")
            except Exception as e:
                st.write(f"❌ **{m_name}**: No disponible ({e})")
                
    except Exception as e:
        st.error(f"Error general: {e}")
