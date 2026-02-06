import streamlit as st
import sys
import subprocess

st.title("🛠 Reparación de Dependencias")

# Paso A: Verificar qué ve el sistema
st.subheader("1. Verificación de instalación")
try:
    import vertexai
    st.success("✅ ¡CONSEGUIDO! La librería 'vertexai' ya está instalada.")
    
    # Solo si funciona la anterior, probamos la otra
    from vertexai.generative_models import GenerativeModel, Tool, GoogleSearchRetrieval
    st.success("✅ Módulo 'generative_models' cargado correctamente.")
    
except ImportError as e:
    st.error(f"❌ Las dependencias NO se han instalado: {e}")
    st.info("Revisa que el archivo en GitHub se llame 'requirements.txt' (todo minúsculas).")
    
    # Botón de emergencia para ver qué hay instalado
    if st.button("Listar paquetes instalados"):
        result = subprocess.run([sys.executable, "-m", "pip", "list"], capture_output=True, text=True)
        st.code(result.stdout)
