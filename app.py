import streamlit as st
from google import genai
from google.oauth2 import service_account
from PIL import Image
import io
import time

# =================================================
# 1. FUNCIONES INTEGRADAS (Para evitar ModuleNotFoundError)
# =================================================

def conectar_vertex(creds_dict):
    """Lógica recuperada de tu ia_engine.py"""
    creds_copy = dict(creds_dict)
    raw_key = str(creds_copy.get("private_key", ""))
    clean_key = raw_key.strip().strip('"').strip("'").replace("\\n", "\n")
    creds_copy["private_key"] = clean_key
    google_creds = service_account.Credentials.from_service_account_info(
        creds_copy, 
        scopes=["https://www.googleapis.com/auth/cloud-platform"]
    )
    return genai.Client(
        vertexai=True, 
        project=creds_copy.get("project_id"), 
        location="us-central1", 
        credentials=google_creds
    )

def realizar_peritaje_visual(client, marca, modelo, fotos):
    """Análisis de fotos recuperado y simplificado de tu ia_engine.py"""
    fotos_ia = []
    for foto in fotos:
        img = Image.open(foto).convert("RGB")
        img.thumbnail((800, 800))
        fotos_ia.append(img)
    
    prompt = f"Analiza estas fotos del tractor {marca} {modelo}. Busca extras (pala, tripuntal) y estado de neumáticos."
    
    response = client.models.generate_content(
        model="gemini-2.5-pro",
        contents=[prompt] + fotos_ia
    )
    return response.text

# =================================================
# 2. INTERFAZ Y ESTILO
# =================================================
st.set_page_config(page_title="Tasador Agrícola Pro", page_icon="🚜")

# Logo
try:
    st.image("afoto.png", width=200)
except:
    st.title("🚜 Agrícola Noroeste")

# Conexión
if "client" not in st.session_state:
    if "google" in st.secrets:
        st.session_state.client = conectar_vertex(st.secrets["google"])
    else:
        st.error("❌ Configura los Secrets de Google.")
        st.stop()

# =================================================
# 3. FORMULARIO PRINCIPAL
# =================================================
with st.form("tasacion"):
    marca = st.selectbox("Marca", ["John Deere", "Fendt", "New Holland", "Case IH"])
    modelo = st.text_input("Modelo", value="6150M")
    fotos = st.file_uploader("Fotos del tractor", accept_multiple_files=True)
    
    btn_tasar = st.form_submit_button("🚀 INICIAR TASACIÓN")

# =================================================
# 4. PROCESAMIENTO
# =================================================
if btn_tasar and modelo:
    with st.spinner("Realizando rastreo masivo y análisis visual..."):
        try:
            # RASTREO (El manguerazo de texto bruto que pediste)
            prompt_busqueda = (
                f"Busca TODOS los anuncios de '{marca} {modelo}' en agriaffaires.es y topmaquinaria.com. "
                "Dame los resultados en líneas simples: PORTAL | MODELO | PRECIO | URL"
            )
            
            res_busqueda = st.session_state.client.models.generate_content(
                model="gemini-2.5-pro",
                contents=prompt_busqueda,
                config={"tools": [{"google_search": {}}]}
            )
            
            # PERITAJE
            res_fotos = ""
            if fotos:
                res_fotos = realizar_peritaje_visual(st.session_state.client, marca, modelo, fotos)
            
            # RESULTADO FINAL
            st.divider()
            st.markdown("### 📊 LISTADO DE MERCADO ENCONTRADO")
            st.text(res_busqueda.text) # st.text mantiene el formato bruto mejor que markdown
            
            if res_fotos:
                st.markdown("### 🔍 ANÁLISIS VISUAL")
                st.write(res_fotos)
                
        except Exception as e:
            st.error(f"Error en la ejecución: {e}")
