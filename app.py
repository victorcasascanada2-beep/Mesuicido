import streamlit as st
import vertexai
from vertexai.generative_models import GenerativeModel, Tool, GoogleSearchRetrieval
from google.oauth2 import service_account

st.title("🚜 Buscador Agrícola (Modo EU)")

# 1. CARGA DE CREDENCIALES
if "google" in st.secrets:
    creds_info = dict(st.secrets["google"])
    # Limpiamos la clave por si las tres comillas metieron caracteres extra
    if "private_key" in creds_info:
        creds_info["private_key"] = creds_info["private_key"].replace("\\n", "\n")
    
    try:
        credentials = service_account.Credentials.from_service_account_info(creds_info)
        
        # 2. INICIALIZACIÓN EN LA REGIÓN CORRECTA
        # Usamos 'eu' porque es lo que configuraste en Agent Builder
        vertexai.init(project=creds_info["project_id"], location="eu", credentials=credentials)
        
        st.success("✅ Conectado a Google Cloud (Región: EU)")
        
        # 3. PRUEBA DE MOTOR
        if st.button("Probar conexión con Gemini 1.5 Pro"):
            model = GenerativeModel("gemini-1.5-pro")
            # Respuesta rápida para validar
            response = model.generate_content("Di 'Sistema EU listo'")
            st.write(f"Respuesta: **{response.text}**")
            
    except Exception as e:
        st.error(f"Error de configuración: {e}")
else:
    st.error("No se encontraron los Secrets [google]")
