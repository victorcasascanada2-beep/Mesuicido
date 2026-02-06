import streamlit as st
import vertexai
from vertexai.generative_models import GenerativeModel, Tool, GoogleSearchRetrieval
from google.oauth2 import service_account

# 1. TÍTULO DE LA APP
st.title("🚜 Buscador Agrícola (Paso 1)")

# 2. CONEXIÓN (La que funcionó en el PDF)
if "google" in st.secrets:
    try:
        creds_info = dict(st.secrets["google"])
        if "private_key" in creds_info:
            creds_info["private_key"] = creds_info["private_key"].replace("\\n", "\n")
        
        credentials = service_account.Credentials.from_service_account_info(creds_info)
        
        # Inicializamos en la región confirmada
        vertexai.init(
            project=creds_info["project_id"], 
            location="europe-west1", 
            credentials=credentials
        )
        st.success("✅ Conexión con europe-west1 establecida.")
    except Exception as e:
        st.error(f"Error en la conexión: {e}")
        st.stop()

# 3. BÚSQUEDA SIMPLE
query = st.text_input("Escribe marca y modelo:", value="John Deere 6175M")

if st.button("BUSCAR"):
    with st.spinner("Buscando ofertas reales..."):
        try:
            # Añadimos la herramienta de Google Search
            search_tool = Tool.from_google_search_retrieval(GoogleSearchRetrieval())
            model = GenerativeModel("gemini-2.5-pro")
            
            prompt = f"Busca ofertas de {query}. Dame una lista con precios y enlaces."
            
            response = model.generate_content(prompt, tools=[search_tool])
            st.markdown(response.text)
        except Exception as e:
            st.error(f"Error en la búsqueda: {e}")
