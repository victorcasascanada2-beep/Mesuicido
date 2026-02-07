import streamlit as st
import vertexai
from google.oauth2 import service_account
from vertexai.generative_models import GenerativeModel, Tool, grounding

# --- 1. CREDENCIALES ---
if "google" in st.secrets:
    creds_info = st.secrets["google"]
    creds = service_account.Credentials.from_service_account_info(creds_info)
else:
    st.error("❌ Revisa los Secrets.")
    st.stop()

# --- 2. CONFIGURACIÓN ---
PROJECT_ID = "subida-fotos-drive"
LOCATION = "europe-west1" 

vertexai.init(project=PROJECT_ID, location=LOCATION, credentials=creds)

# --- 3. HERRAMIENTAS (SINTAXIS CORREGIDA PARA EL ERROR 400) ---
# El error pide usar 'google_search'. En el SDK actual de Vertex, 
# se hace a través de GoogleSearchRetrieval sin parámetros extra.
tools = [
    Tool.from_google_search_retrieval(
        grounding.GoogleSearchRetrieval()
    )
]

# --- 4. MODELO (2.5 PRO) ---
model = GenerativeModel(
    model_name="gemini-2.5-pro", 
    tools=tools
)

# --- 5. INTERFAZ ---
st.title("🚜 Paso 1: Lista de Resultados (Sin Error 400)")

tractor = st.text_input("Modelo de tractor:", "John Deere 6150M")

if st.button("Buscar Anuncios"):
    with st.spinner("Conectando con Google Search..."):
        try:
            prompt = (
                f"Busca anuncios reales de {tractor} en España. "
                "Dame una lista con: Nombre, Precio y URL."
            )
            
            # Llamada limpia al modelo
            response = model.generate_content(prompt)

            st.markdown("### 📝 Resultados:")
            if response.candidates:
                # El texto principal de la respuesta
                st.write(response.candidates[0].content.parts[0].text)
                
                # Opcional: Mostrar las fuentes de búsqueda si están disponibles
                if response.candidates[0].grounding_metadata.search_entry_point:
                    st.divider()
                    st.caption("Fuentes de Google Search:")
                    st.write(response.candidates[0].grounding_metadata.search_entry_point.rendered_content, unsafe_allow_html=True)
            else:
                st.warning("No se recibieron resultados.")

        except Exception as e:
            # Si el error 400 persiste, imprimimos el mensaje detallado para ver si Google pide algo más
            st.error(f"Fallo técnico: {str(e)}")
            if "google_search" in str(e):
                st.info("Google está forzando el cambio a la nueva API de búsqueda.")
