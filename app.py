import streamlit as st
import vertexai
from google.oauth2 import service_account
from vertexai.generative_models import GenerativeModel, Tool, GoogleSearchRetrieval

st.title("🚜 Buscador Agrícola (Sincronizado EU)")

if "google" in st.secrets:
    try:
        creds_info = dict(st.secrets["google"])
        if "private_key" in creds_info:
            creds_info["private_key"] = creds_info["private_key"].replace("\\n", "\n")
        
        credentials = service_account.Credentials.from_service_account_info(creds_info)
        
        # Aquí usamos 'eu' porque es donde elegiste el API de búsqueda
        vertexai.init(project=creds_info["project_id"], location="eu", credentials=credentials)
        st.success("✅ Conexión establecida con la región de búsqueda (EU)")
    except Exception as e:
        st.error(f"Error de conexión: {e}")
        st.stop()

query = st.text_input("Modelo de tractor a buscar:", value="John Deere 6155R")

if st.button("BUSCAR EN EUROPA"):
    with st.spinner("Conectando con el motor de búsqueda europeo..."):
        try:
            # Esta es la herramienta que configuramos en Europa
            search_tool = Tool.from_google_search_retrieval(GoogleSearchRetrieval())
            model = GenerativeModel("gemini-2.5-pro")
            
            response = model.generate_content(
                f"Busca ofertas de {query} en portales europeos. Dame precios y enlaces.",
                tools=[search_tool]
            )
            st.markdown(response.text)
        except Exception as e:
            st.error(f"Aviso: Si ves un error de región, es que Gemini 2.5 aún no está disponible en 'eu' para tu cuenta. Error: {e}")
