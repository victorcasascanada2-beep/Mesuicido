# =================================================
# 1. IMPORTACIÓN DE LIBRERÍAS (EL "MOTOR" COMPLETO)
# =================================================
import streamlit as st
from PIL import Image
import time
import base64

# Tus módulos locales (los que están en el ZIP)
import ia_engine
import html_generator
import google_drive_manager
import location_manager
import config_prompt

# =================================================
# 2. CONFIGURACIÓN E INTERFAZ
# =================================================
st.set_page_config(page_title="Tasador Agrícola Pro", page_icon="🚜", layout="centered")

# Estilo para el logo y limpieza de la interfaz
st.markdown("""
<style>
    [data-testid="stToolbar"], footer {display: none;}
    .block-container { padding-top: 2rem !important; }
    [data-testid="stImage"] { display: flex; justify-content: center; }
</style>
""", unsafe_allow_html=True)

# Logo
try:
    st.image("afoto.png", width=250)
except:
    st.title("🚜 Agrícola Noroeste")

# =================================================
# 3. CONEXIÓN A VERTEX AI (USANDO TU ia_engine)
# =================================================
if "client" not in st.session_state:
    if "google" in st.secrets:
        # Pasamos los secrets a la función que ya limpia la private_key
        st.session_state.client = ia_engine.conectar_vertex(dict(st.secrets["google"]))
    else:
        st.error("❌ Falta la configuración 'google' en Streamlit Secrets.")
        st.stop()

# =================================================
# 4. FORMULARIO DE TASACIÓN
# =================================================
with st.form("tasacion_form"):
    col1, col2 = st.columns(2)
    with col1:
        marca = st.selectbox("Marca", ["John Deere", "Fendt", "New Holland", "Case IH", "Massey Ferguson"])
        modelo = st.text_input("Modelo", placeholder="Ej: 6150M")
    with col2:
        anio = st.number_input("Año", min_value=1990, max_value=2026, value=2018)
        horas = st.number_input("Horas de uso", min_value=0, step=500)
    
    observaciones = st.text_area("Extras detectados (Pala, Tripuntal, Contrapesos...)")
    fotos = st.file_uploader("Sube fotos para análisis visual", accept_multiple_files=True, type=['png', 'jpg', 'jpeg'])
    
    submit = st.form_submit_button("🚀 INICIAR TASACIÓN Y RASTREO")

# =================================================
# 5. PROCESAMIENTO (DATOS + FOTOS)
# =================================================
if submit and modelo:
    with st.spinner("⚡ Ejecutando rastreo masivo en Agriaffaires y TopMaquinaria..."):
        try:
            # A. RASTREO DE MERCADO (MODO TEXTO BRUTO PARA MÁXIMOS RESULTADOS)
            # Usamos el prompt directo para evitar el límite de 3 anuncios
            prompt_busqueda = (
                f"Busca TODOS los anuncios de '{marca} {modelo}' en agriaffaires.es y topmaquinaria.com. "
                "No uses tablas. Dame una línea por anuncio con este formato: "
                "PORTAL | MODELO | AÑO | HORAS | PRECIO | URL"
            )
            
            busqueda_raw = st.session_state.client.models.generate_content(
                model="gemini-2.5-pro",
                contents=prompt_busqueda,
                config={"tools": [{"google_search": {}}], "temperature": 0.1}
            )
            
            # B. ANÁLISIS VISUAL (USANDO TU ia_engine.py)
            analisis_fotos = ""
            if fotos:
                st.info("📸 Analizando imágenes para buscar extras y desgaste...")
                analisis_fotos = ia_engine.realizar_peritaje(
                    st.session_state.client, marca, modelo, anio, horas, observaciones, fotos
                )

            # C. CONSOLIDACIÓN DE RESULTADOS
            st.session_state.informe_final = (
                f"## 📊 RESULTADOS DE MERCADO (Rastreo Profundo)\n\n"
                f"{busqueda_raw.text}\n\n"
                f"--- \n"
                f"## 🔍 INFORME DE PERITAJE VISUAL\n\n"
                f"{analisis_fotos}"
            )
            st.session_state.modelo_final = modelo
            
        except Exception as e:
            st.error(f"❌ Error técnico: {str(e)}")

# =================================================
# 6. RESULTADOS Y GUARDADO
# =================================================
if "informe_final" in st.session_state:
    st.divider()
    st.markdown(st.session_state.informe_final)
    
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("☁️ GUARDAR EN DRIVE"):
            with st.spinner("Subiendo a la carpeta de Agrícola Noroeste..."):
                # Generamos el nombre y el HTML
                nombre_doc = f"Tasacion_{st.session_state.modelo_final}_{int(time.time())}.html"
                html_contenido = html_generator.formatear_contenido(st.session_state.informe_final)
                
                # Subimos usando tu google_drive_manager
                id_drive = google_drive_manager.subir_informe(dict(st.secrets["google"]), nombre_doc, html_contenido)
                if id_drive:
                    st.success(f"✅ Informe guardado con ID: {id_drive}")
    
    with col_b:
        # Opción para descargar localmente
        st.download_button("📥 DESCARGAR INFORME", 
                           data=st.session_state.informe_final, 
                           file_name=f"tasacion_{st.session_state.modelo_final}.txt")
