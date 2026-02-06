import streamlit as st
from PIL import Image
import vertexai
from vertexai.generative_models import GenerativeModel, Tool, GoogleSearchRetrieval
from google.oauth2 import service_account
import os

# --- 1. CONFIGURACIÓN E INTERFAZ ---
st.set_page_config(page_title="Buscador Agrícola", page_icon="🚜", layout="centered")

st.markdown("""
<style>
    header[data-testid="stHeader"] { display: none !important; }
    footer { display: none !important; }
    .block-container { 
        margin-top: -3rem !important; 
        padding-top: 1rem !important; 
    }
    [data-testid="stImage"] { display: flex; justify-content: center; }
</style>
""", unsafe_allow_html=True)

# --- 2. CONEXIÓN GOOGLE (Limpieza de Clave) ---
if "credentials" not in st.session_state:
    try:
        if "google" in st.secrets:
            creds_info = dict(st.secrets["google"])
            # Limpiamos posibles errores de formato en la clave
            if "private_key" in creds_info:
                creds_info["private_key"] = creds_info["private_key"].replace("\\n", "\n")
            
            st.session_state.credentials = service_account.Credentials.from_service_account_info(creds_info)
            vertexai.init(
                project=creds_info["project_id"], 
                location="eu", 
                credentials=st.session_state.credentials
            )
    except Exception as e:
        st.error(f"Error de conexión: {e}")

# --- 3. INTERFAZ Y LÓGICA ---
if os.path.exists("agricolanoroestelogo.jpg"):
    st.image("agricolanoroestelogo.jpg", width=300)

st.title("Buscador de Mercado")

with st.form("form_busqueda"):
    c1, c2 = st.columns(2)
    marca = c1.text_input("Marca", value="John Deere")
    modelo = c1.text_input("Modelo", value="6175M")
    horas = c2.text_input("Horas", value="9000")
    region = c2.selectbox("Región", ["Europa", "España", "Francia"])
    submit = st.form_submit_button("🔍 BUSCAR OFERTAS", use_container_width=True)

if submit:
    with st.spinner("Buscando en tiempo real..."):
        try:
            search_tool = Tool.from_google_search_retrieval(GoogleSearchRetrieval())
            model = GenerativeModel("gemini-1.5-pro")
            
            prompt = f"Busca ofertas de {marca} {modelo} con {horas}h en {region}. Dame una tabla con links."
            response = model.generate_content(prompt, tools=[search_tool])
            
            st.session_state.resultados = response.text
        except Exception as e:
            st.error(f"Error en búsqueda: {e}")

if "resultados" in st.session_state:
    st.markdown(st.session_state.resultados)
    if st.button("Nueva búsqueda"):
        del st.session_state.resultados
        st.rerun()
