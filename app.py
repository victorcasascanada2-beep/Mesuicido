import streamlit as st
import json
from google import genai
from google.genai import types
from google.oauth2 import service_account

# Configuración de la interfaz de la página
st.set_page_config(page_title="IA Tasadora de Tractores", page_icon="🚜", layout="wide")

def get_tasador_client():
    """
    Inicializa el cliente de Vertex AI utilizando los secretos de Streamlit.
    Se añade el scope 'cloud-platform' para evitar el error de OAuth.
    """
    try:
        # Buscamos la clave 'google' en los Secrets de Streamlit
        if "google" not in st.secrets:
            st.error("No se encontró la clave 'google' en los Secrets de Streamlit.")
            return None
            
        creds_info = st.secrets["google"]
        
        # Convertimos a diccionario si los secretos vienen como string JSON
        if isinstance(creds_info, str):
            creds_info = json.loads(creds_info)
            
        # DEFINICIÓN DEL SCOPE: Esto soluciona el error 'invalid_scope'
        # Permite que la cuenta de servicio acceda a los servicios de Google Cloud
        scopes = ['https://www.googleapis.com/auth/cloud-platform']
        
        google_creds = service_account.Credentials.from_service_account_info(
            creds_info, 
            scopes=scopes
        )
        
        # Inicializamos el cliente de la API GenAI de Google
        # Usamos la ubicación 'europe-west1' para resultados locales en Europa
        return genai.Client(
            vertexai=True,
            project=creds_info.get("project_id"),
            location="europe-west1",
            credentials=google_creds
        )
    except Exception as e:
        st.error(f"Error en la autenticación: {e}")
        return None

def realizar_tasacion(modelo_tractor, horas, anio, extra_info):
    """
    Ejecuta la búsqueda con Grounding (Google Search) y genera el informe técnico.
    """
    client = get_tasador_client()
    if not client:
        return "Error: No se pudo establecer conexión con el motor de IA."
    
    # Identificador del modelo Gemini 2.5 Flash
    model_id = "gemini-2.5-flash-preview-09-2025"
    
    # Instrucciones del sistema para definir el comportamiento del modelo
    system_prompt = """
    Eres un perito tasador senior especializado en maquinaria agrícola europea.
    Tu objetivo es proporcionar una valoración de mercado precisa y realista.
    
    METODOLOGÍA:
    1. Usa Google Search para encontrar anuncios actuales en Agriaffaires, Mascus y Traktorpool.
    2. Identifica al menos 5 anuncios de unidades similares (modelo, año, horas).
    3. Calcula el valor medio del mercado y establece un rango (Min/Max).
    4. Analiza extras como suspensión TLS, tripuntal o GPS para ajustar el valor al alza.
    5. Presenta los datos en una tabla comparativa clara seguida de tu conclusión profesional.
    """

    # Configuración de la herramienta de búsqueda (Grounding)
    # El dynamic_threshold en 0.1 fuerza la búsqueda externa casi siempre
    search_tool = types.Tool(
        google_search_retrieval=types.GoogleSearchRetrieval(
            dynamic_retrieval_config=types.DynamicRetrievalConfig(
                dynamic_threshold=0.1
            )
        )
    )

    prompt_usuario = f"""
    Realiza una tasación profesional para el siguiente tractor:
    - Marca y Modelo: {modelo_tractor}
    - Año de fabricación: {anio}
    - Horas de motor: {horas}
    - Equipamiento y estado: {extra_info}
    """

    try:
        # Generación de la respuesta
        response = client.models.generate_content(
            model=model_id,
            contents=prompt_usuario,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                tools=[search_tool],
                temperature=0.1, # Precisión máxima en datos numéricos
                max_output_tokens=4096
            )
        )
        return response.text
    except Exception as e:
        return f"Se produjo un error durante la generación del informe: {str(e)}"

# --- INTERFAZ STREAMLIT ---

st.title("🚜 Sistema de Tasación de Maquinaria Agrícola")
st.write("Análisis de mercado en tiempo real mediante Inteligencia Artificial y Búsqueda de Google.")

# Columnas para los datos de entrada
c1, c2, c3 = st.columns(3)
with c1:
    modelo_input = st.text_input("Modelo del Tractor", value="John Deere 6175M")
with c2:
    anio_input = st.number_input("Año", min_value=1990, max_value=2026, value=2021)
with c3:
    horas_input = st.number_input("Horas Totales", min_value=0, value=3000, step=100)

detalles_input = st.text_area("Estado y Extras (Opcional)", 
                             placeholder="Ej: Transmisión AutoQuad, Suspensión TLS, neumáticos al 90%...")

if st.button("🚀 Iniciar Peritaje"):
    if not modelo_input:
        st.warning("Debes introducir un modelo para realizar la búsqueda.")
    else:
        # Indicador de carga
        with st.status("Consultando anuncios en Agriaffaires y Mascus...", expanded=True) as status:
            st.write("Analizando tendencias de mercado...")
            resultado = realizar_tasacion(modelo_input, horas_input, anio_input, detalles_input)
            status.update(label="Tasación completada", state="complete")
        
        # Resultados
        st.divider()
        st.markdown(resultado)

# Sidebar informativa
st.sidebar.markdown("### Configuración Técnica")
st.sidebar.info("Motor: Gemini 2.5 Flash\nRegión: europe-west1\nGrounding: Habilitado")
st.sidebar.caption("Esta app busca anuncios reales en vivo para evitar datos obsoletos.")
