import streamlit as st

st.title("🛠 Prueba de Dependencias")

# Test A: Nueva dependencia sencilla
try:
    import pandas as pd
    st.success("✅ Pandas cargado. ¡Streamlit está leyendo el requirements.txt!")
except ImportError:
    st.error("❌ Ni siquiera Pandas carga. El archivo requirements.txt está siendo ignorado.")

# Test B: Vertex AI
try:import streamlit as st
import vertexai
from google.oauth2 import service_account
from vertexai.generative_models import GenerativeModel, Tool, GoogleSearchRetrieval

st.title("🚜 Verificación de Alta Sincronizada")

if "google" in st.secrets:
    try:
        creds = dict(st.secrets["google"])
        creds["private_key"] = creds["private_key"].replace("\\n", "\n")
        credentials = service_account.Credentials.from_service_account_info(creds)
        
        # PASO A: Inicializamos en la región donde está tu historial de uso (USA)
        vertexai.init(project=creds["project_id"], location="us-central1", credentials=credentials)
        st.success("✅ 'Cerebro' (Gemini 2.5 Pro) detectado en us-central1")

        # PASO B: Botón para testear la búsqueda europea
        if st.button("PROBAR BÚSQUEDA EN EUROPA"):
            model = GenerativeModel("gemini-2.5-pro")
            # Forzamos a la herramienta a mirar en el motor de búsqueda
            search_tool = Tool.from_google_search_retrieval(GoogleSearchRetrieval())
            
            response = model.generate_content(
                "Busca tractores John Deere en portales de España.",
                tools=[search_tool]
            )
            st.write("### Resultado del buscador:")
            st.markdown(response.text)
            
    except Exception as e:
        st.error(f"Error detectado: {e}")
    import vertexai
    from vertexai.generative_models import GenerativeModel, Tool, GoogleSearchRetrieval
    st.success("✅ Vertex AI cargado correctamente.")
except ImportError as e:
    st.error(f"❌ Vertex AI sigue fallando: {e}")
    
