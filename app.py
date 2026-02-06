import streamlit as st
import json
from google import genai
from google.genai import types
from google.oauth2 import service_account

# Configuración de la página
st.set_page_config(page_title="IA Tasadora de Tractores", page_icon="🚜", layout="wide")

def get_tasador_client():
    """
    Construye las credenciales y el cliente desde los secrets de Streamlit.
    Usa la clave 'google' especificada por el usuario.
    """
    try:
        # Cargamos el JSON de la cuenta de servicio usando la clave 'google'
        if "google" not in st.secrets:
            st.error("No se encontró la clave 'google' en los Secrets de Streamlit.")
            return None
            
        creds_info = st.secrets["google"]
        
        # Si el secreto es un string (JSON), lo convertimos a dict
        if isinstance(creds_info, str):
            creds_info = json.loads(creds_info)
            
        google_creds = service_account.Credentials.from_service_account_info(creds_info)
        
        return genai.Client(
            vertexai=True,
            project=creds_info.get("project_id"),
            location="europe-west1", # Ubicación optimizada para Europa
            credentials=google_creds
        )
    except Exception as e:
        st.error(f"Error en la autenticación: {e}")
        return None

def realizar_tasacion(modelo_tractor, horas, anio, extra_info):
    """
    Lógica de búsqueda y generación de informe de tasación.
    """
    client = get_tasador_client()
    if not client:
        return "No se pudo conectar con el servicio de IA. Verifica tus credenciales."
    
    model_id = "gemini-2.5-flash-preview-09-2025"
    
    system_prompt = """
    Eres un perito tasador senior de maquinaria agrícola europea.
    Tu tarea es generar un informe técnico de valoración basado en datos reales de mercado.
    
    METODOLOGÍA:
    1. Utiliza Google Search para encontrar anuncios actuales en Agriaffaires, Mascus y Traktorpool.
    2. Identifica al menos 5 anuncios comparables recientes.
    3. Calcula el valor medio ajustado por depreciación según horas y año.
    4. Identifica equipamiento extra (suspensión, GPS, pala) y valora su impacto.
    
    FORMATO DE RESPUESTA:
    - Tabla comparativa de anuncios encontrados.
    - Valoración estimada (Rango Min/Max).
    - Análisis de liquidez y demanda del modelo.
    - Fuentes consultadas con enlaces directos.
    """

    search_tool = types.Tool(
        google_search_retrieval=types.GoogleSearchRetrieval(
            dynamic_retrieval_config=types.DynamicRetrievalConfig(
                dynamic_threshold=0.1 
            )
        )
    )

    user_query = f"""
    Realiza una tasación exhaustiva para:
    - Modelo: {modelo_tractor}
    - Año: {anio}
    - Horas: {horas}
    - Detalles adicionales: {extra_info}
    """

    try:
        response = client.models.generate_content(
            model=model_id,
            contents=user_query,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                tools=[search_tool],
                temperature=0.1,
                max_output_tokens=4096
            )
        )
        return response.text
    except Exception as e:
        return f"Error durante la generación de la tasación: {str(e)}"

# --- INTERFAZ DE USUARIO (Streamlit) ---

st.title("🚜 Peritaje de Maquinaria con IA")
st.subheader("Tasación profesional basada en el mercado europeo actual")

with st.sidebar:
    st.header("Configuración de IA")
    st.info("Utilizando Gemini 2.5 Pro con Grounding de búsqueda para obtener precios reales en vivo.")
    st.divider()
    st.caption("Región de procesamiento: europe-west1")

# Formulario de entrada
col1, col2, col3 = st.columns(3)

with col1:
    modelo = st.text_input("Marca y Modelo", placeholder="Ej: Valtra G125")
with col2:
    anio = st.number_input("Año", min_value=1980, max_value=2026, value=2021)
with col3:
    horas = st.number_input("Horas totales", min_value=0, value=2000, step=50)

detalles = st.text_area("Equipamiento y estado", placeholder="Ej: Suspensión de cabina, tripuntal delantero, neumáticos al 80%...")

if st.button("Generar Informe"):
    if not modelo:
        st.warning("Introduce el modelo del tractor para continuar.")
    else:
        with st.status("Consultando bases de datos internacionales...", expanded=True) as status:
            st.write("Analizando Agriaffaires y Mascus...")
            resultado = realizar_tasacion(modelo, horas, anio, detalles)
            status.update(label="Análisis finalizado", state="complete", expanded=False)
        
        st.divider()
        st.markdown(resultado)
