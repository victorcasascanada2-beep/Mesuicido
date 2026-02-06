import streamlit as st
from PIL import Image
import vertexai
from vertexai.generative_models import GenerativeModel, Tool, GoogleSearchRetrieval
from google.oauth2 import service_account
import os

# -------------------------------------------------
# 1. CONFIGURACIÓN E INTERFAZ (Tu estilo original)
# -------------------------------------------------
st.set_page_config(page_title="Buscador Agrícola", page_icon="🚜", layout="centered")

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
            creds_info = dict(st.secrets["google"])
            st.session_state.credentials = service_account.Credentials.from_service_account_info(creds_info)
            vertexai.init(project=creds_info["project_id"], location="eu", credentials=st.session_state.credentials)
    except Exception as e:
        st.error(f"Error en conexión Google: {e}")

# -------------------------------------------------
# 3. INTERFAZ: LOGO Y TÍTULO
# -------------------------------------------------
if os.path.exists("agricolanoroestelogo.jpg"):
    st.image("agricolanoroestelogo.jpg", width=300)

st.title("Buscador de Mercado")
st.caption("Consulta en tiempo real los precios de tractores en toda Europa.")

# -------------------------------------------------
# 4. FORMULARIO DE BÚSQUEDA (Adaptado)
# -------------------------------------------------
if "resultados_busqueda" not in st.session_state:
    with st.form("form_busqueda"):
        
        c1, c2 = st.columns(2)
        with c1:
            marca = st.text_input("Marca", value="John Deere")
            modelo = st.text_input("Modelo", placeholder="Ej: 6175M")
        with c2:
            horas_max = st.text_input("Horas aprox.", placeholder="Ej: 9000")
            pais = st.selectbox("Región", ["Europa", "España", "Francia", "Alemania"])
        
        detalles_extra = st.text_area("Requisitos adicionales", placeholder="Ej: Con tripuntal, suspensión, año posterior a 2016...")
        
        submit = st.form_submit_button("🔍 BUSCAR OFERTAS REALES", use_container_width=True)

    if submit:
        if marca and modelo:
            with st.spinner("Rastreando Agriaffaires, Tractorpool y más..."):
                try:
                    # Configuramos la herramienta de búsqueda de Google (Grounding)
                    search_tool = Tool.from_google_search_retrieval(
                        google_search_retrieval=GoogleSearchRetrieval()
                    )
                    model = GenerativeModel("gemini-1.5-pro")

                    # Montamos el PROMPT con tus datos
                    prompt = f"""
                    Busca en portales de maquinaria agrícola usados: {marca} {modelo}.
                    Filtros: Máximo {horas_max} horas, ubicación en {pais}.
                    Notas adicionales: {detalles_extra}.
                    
                    Devuelve una tabla comparativa profesional con estas columnas:
                    Modelo | Año | Horas | Precio | Ubicación | Enlace directoimport streamlit as st
from PIL import Image
import vertexai
from vertexai.generative_models import GenerativeModel, Tool, GoogleSearchRetrieval
from google.oauth2 import service_account
import os

# -------------------------------------------------
# 1. CONFIGURACIÓN E INTERFAZ (Tu Estilo Original)
# -------------------------------------------------
st.set_page_config(page_title="Buscador Agrícola", page_icon="🚜", layout="centered")

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
            # Lee de los Secrets de Streamlit Cloud
            creds_info = dict(st.secrets["google"])
            st.session_state.credentials = service_account.Credentials.from_service_account_info(creds_info)
            # Inicializa Vertex AI con tu proyecto
            vertexai.init(
                project=creds_info["project_id"], 
                location="eu", 
                credentials=st.session_state.credentials
            )
    except Exception as e:
        st.error(f"Error en conexión Google: {e}")

# -------------------------------------------------
# 3. CUERPO DE LA APP
# -------------------------------------------------
if os.path.exists("agricolanoroestelogo.jpg"):
    st.image("agricolanoroestelogo.jpg", width=300)

st.title("Buscador de Mercado")
st.caption("Precios y ofertas de maquinaria en tiempo real (Europa)")

# Formulario de búsqueda
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
                    # Configuración de búsqueda en Google (Grounding)
                    search_tool = Tool.from_google_search_retrieval(
                        google_search_retrieval=GoogleSearchRetrieval()
                    )
                    model = GenerativeModel("gemini-1.5-pro")

                    prompt = f"""
                    Busca ofertas reales de {marca} {modelo} con unas {horas} horas en {region}.
                    Genera una tabla comparativa con las columnas: 
                    Modelo | Horas | Año | Precio | Ubicación | Enlace al anuncio
                    """
                    
                    # Generación de contenido con búsqueda en tiempo real
                    response = model.generate_content(prompt, tools=[search_tool])
                    st.session_state.resultados = response.text
                    st.rerun()
                except Exception as e:
                    st.error(f"Error al buscar: {e}")
        else:
            st.warning("Escribe la marca y el modelo.")

# Mostrar resultados
if "resultados" in st.session_state:
    st.markdown(st.session_state.resultados)
    if st.button("🔄 NUEVA BÚSQUEDA", use_container_width=True):
        del st.session_state.resultados
        st.rerun()
                    """
                    
                    response = model.generate_content(prompt, tools=[search_tool])
                    
                    st.session_state.resultados_busqueda = response.text
                    st.rerun()
                except Exception as e:
                    st.error(f"Error en la búsqueda: {e}")
        else:
            st.warning("⚠️ Introduce al menos Marca y Modelo.")

# -------------------------------------------------
# 5. RESULTADOS
# -------------------------------------------------
if "resultados_busqueda" in st.session_state:
    st.markdown("### 📊 Comparativa de Mercado")
    st.markdown(st.session_state.resultados_busqueda)
    
    if st.button("🔄 NUEVA BÚSQUEDA", use_container_width=True):
        del st.session_state.resultados_busqueda
        st.rerun()
