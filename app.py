import streamlit as st
import vertexai
from google.oauth2 import service_account
# Importamos solo lo que tu lista confirmó que existe
from vertexai.generative_models import GenerativeModel, Tool

st.title("🚜 Buscador Agrícola 2.5 Pro")

if "google" in st.secrets:
    try:
        creds_info = dict(st.secrets["google"])
        if "private_key" in creds_info:
            creds_info["private_key"] = creds_info["private_key"].replace("\\n", "\n")
        
        credentials = service_account.Credentials.from_service_account_info(creds_info)
        
        # Sincronizamos con us-central1 (donde tu consola muestra actividad)
        vertexai.init(project=creds_info["project_id"], location="us-central1", credentials=credentials)
        st.success("✅ Sistema conectado y sincronizado.")

        query = st.text_input("¿Qué tractor buscamos?", value="John Deere 6155R")

        if st.button("BUSCAR OFERTAS"):
            with st.spinner("Rastreando portales en España y Europa..."):
                # Creamos la herramienta de búsqueda usando el nombre genérico 'google_search_retrieval'
                # que es el estándar interno cuando no aparece el nombre largo
                search_tool = Tool.from_google_search_retrieval(
                    google_search_retrieval={} # Esta es la forma más compatible
                )
                
                model = GenerativeModel("gemini-2.5-pro")
                
                prompt = f"Busca ofertas de {query} en España. Dame una tabla con Modelo, Precio y Link."
                
                response = model.generate_content(prompt, tools=[search_tool])
                st.markdown(response.text)

    except Exception as e:
        st.error(f"Error técnico: {e}")
