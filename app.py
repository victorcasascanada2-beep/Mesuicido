import streamlit as st
from PIL import Image
import vertexai
from vertexai.generative_models import GenerativeModel, Tool, GoogleSearchRetrieval
from google.oauth2 import service_account
import os

# -------------------------------------------------
# 1. CONFIGURACIÓN E INTERFAZ (CSS CORREGIDO)
# -------------------------------------------------
st.set_page_config(page_title="Buscador Agrícola", page_icon="🚜", layout="centered")

# Inyectamos el CSS asegurando que las comillas triples envuelvan todo el bloque
st.markdown("""
<style>
    header[data-testid="stHeader"] { display: none !important; }
    [data-testid="stToolbar"] { display: none !important; }
    footer { display: none !important; }
    .block-container { 
        margin-top: -3rem !important; 
        padding-top: 1rem !important; 
        padding-bottom: 2rem !important;
    }
    [data-testid="stImage"] { display: flex; justify-content: center; }
    button[kind="secondaryFormSubmit"] {
        border: 2px solid #2e7d32 !important;
        color: #2e7d32 !important;
        font-weight: bold !important;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# 2. CONEXIÓN GOOGLE (Usando tu tag [google])
# -------------------------------------------------
if "credentials" not in st.session_state:
    try:
        if "google" in st.secrets:
            # Extraemos la info del Secret de Streamlit Cloud
            creds_info = dict(st.secrets["google"])
            st.session_state.credentials = service_account.Credentials.from_service_account_info(creds_info)
            
            # Inicializamos Vertex AI
            vertexai.init(
                project=creds_info["project_id"], 
                location="eu", 
                credentials=st.session_state.credentials
            )
    except Exception as e:
        st.error(f"Error en conexión Google: {e}")

# -------------------------------------------------
# 3. CUERPO DE LA APP (Interfaz de Usuario)
# -------------------------------------------------
# Intentamos cargar el logo si existe en el repo
if os.path.exists("agricolanoroestelogo.jpg"):
    st.image("agricolanoroestelogo.jpg", width=300)

st.title("Buscador de Mercado")
st.caption("Precios y ofertas de maquinaria en tiempo real (Europa)")

# Formulario de búsqueda optimizado
if "resultados" not in st.session_state:
    with st.form("form_busqueda"):
        c1, c2 = st.columns(2)
        with c1:
            marca = st.text_input("Marca", value="John Deere")
            modelo = st.text_input("Modelo", placeholder="Ej: 6175M")
        with c2:
            horas = st.text_input("Horas máx.", placeholder="Ej: 9000")
            region = st.selectbox("Región", ["Europa", "España", "Francia", "Alemania"])
        
        submit = st.form_submit_button("🔍 BUSCAR OFERTAS", use_container_width=True)

    if submit:
        if marca and modelo:
            with st.spinner("Rastreando portales especializados..."):
                try:
                    # Configuración de búsqueda con Grounding en Google
                    search_tool = Tool.from_google_search_retrieval(
                        google_search_retrieval=GoogleSearchRetrieval()
                    )
                    model = GenerativeModel("gemini-1.5-pro")

                    # Definimos el prompt para obtener la tabla que buscas
                    prompt = f"""
                    Busca ofertas reales de {marca} {modelo} con aproximadamente {horas} horas en {region}.
                    Usa tus herramientas de búsqueda para encontrar datos actuales.
                    Genera una tabla comparativa con las columnas: 
                    Modelo | Horas | Año | Precio | Ubicación | Enlace al anuncio
                    """
                    
                    # Llamada al modelo Gemini 1.5 Pro
                    response = model.generate_content(prompt, tools=[search_tool])
                    st.session_state.resultados = response.text
                    st.rerun()
                except Exception as e:
                    st.error(f"Error al conectar con el motor de búsqueda: {e}")
        else:
            st.warning("⚠️ Introduce Marca y Modelo para iniciar la búsqueda.")

# -------------------------------------------------
# 4. VISUALIZACIÓN DE RESULTADOS
# -------------------------------------------------
if "resultados" in st.session_state:
    st.markdown("### 📊 Resultados Encontrados")
    st.markdown(st.session_state.resultados)
    
    if st.button("🔄 REALIZAR OTRA BÚSQUEDA", use_container_width=True):
        del st.session_state.resultados
        st.rerun()
