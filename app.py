import streamlit as st

st.title("🛠 Prueba de Dependencias")

# Test A: Nueva dependencia sencilla
try:
    import pandas as pd
    st.success("✅ Pandas cargado. ¡Streamlit está leyendo el requirements.txt!")
except ImportError:
    st.error("❌ Ni siquiera Pandas carga. El archivo requirements.txt está siendo ignorado.")

# Test B: Vertex AI
try:
    import vertexai
    from vertexai.generative_models import GenerativeModel, Tool, GoogleSearchRetrieval
    st.success("✅ Vertex AI cargado correctamente.")
except ImportError as e:
    st.error(f"❌ Vertex AI sigue fallando: {e}")
    
