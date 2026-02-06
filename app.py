import streamlit as st
import vertexai
from vertexai.generative_models import GenerativeModel, Tool, GoogleSearchRetrieval
from google.oauth2 import service_account
import os

# 1. CONFIGURACIÓN BÁSICA
st.set_page_config(page_title="Buscador 2.5 Pro", page_icon="🚜")

if "google" in st.secrets:
    creds_info = dict(st.secrets["google"])
    if "private_key" in creds_info:
        creds_info["private_key"] = creds_info["private_key"].replace("\\n", "\n")
    
    try:
        credentials = service_account.Credentials.from_service_account_info(creds_info)
        # Usamos la región que funcionó en tu test [cite: 4, 7]
        vertexai.init(project=creds_info["project_id"], location="europe-west1", credentials=credentials)
    except Exception as e:
        st.error(f"Error de llave: {e}")

# 2. INTERFAZ DE BÚSQUEDA
st.title("Buscador de Maquinaria")

with st.form("search_form"):
    marca = st.text_input("Marca", value="John Deere")
    modelo = st.text_input("Modelo", value="6175M")
    submit = st.form_submit_button("🔍 BUSCAR")

if submit:
    with st.spinner("Consultando Google Search con Gemini 2.5 Pro..."):
        try:
            # Activamos la herramienta de búsqueda real
            search_tool = Tool.from_google_search_retrieval(GoogleSearchRetrieval())
            model = GenerativeModel("gemini-2.5-pro")
            
            prompt = f"Busca ofertas actuales de {marca} {modelo}. Dame una tabla con los resultados."
            
            # Ejecución
            response = model.generate_content(prompt, tools=[search_tool])
            st.markdown(response.text)
        except Exception as e:
            st.error(f"Error en la búsqueda: {e}")
