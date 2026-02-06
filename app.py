import streamlit as st

# Intentamos cargar las dependencias con orden
try:
    import vertexai
    from vertexai.generative_models import GenerativeModel, Tool, GoogleSearchRetrieval
    from google.oauth2 import service_account
    librerias_ok = True
except Exception as e:
    st.error(f"Error de carga: {e}")
    librerias_ok = False

st.title("🚜 Verificación de Alta Sincronizada")

if librerias_ok and "google" in st.secrets:
    try:
        creds = dict(st.secrets["google"])
        creds["private_key"] = creds["private_key"].replace("\\n", "\n")
        credentials = service_account.Credentials.from_service_account_info(creds)
        
        # Sincronizamos con us-central1 donde tienes el consumo
        vertexai.init(project=creds["project_id"], location="us-central1", credentials=credentials)
        st.success("✅ 'Cerebro' Gemini 2.5 Pro detectado.")

        if st.button("PROBAR BÚSQUEDA"):
            # Usamos el modelo que aparece en tu consola
            model = GenerativeModel("gemini-2.5-pro")
            search_tool = Tool.from_google_search_retrieval(GoogleSearchRetrieval())
            
            response = model.generate_content(
                "Busca tractores John Deere en España.",
                tools=[search_tool]
            )
            st.markdown(response.text)
            
    except Exception as e:
        st.error(f"Error en la ejecución: {e}")
else:
    st.warning("Esperando configuración correcta de librerías y secrets...")
