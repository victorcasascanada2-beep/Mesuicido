import streamlit as st
import vertexai
from google.oauth2 import service_account
from vertexai.generative_models import GenerativeModel, Tool, grounding

# --- 1. CREDENCIALES ---
if "google" in st.secrets:
    creds_info = st.secrets["google"]
    creds = service_account.Credentials.from_service_account_info(creds_info)
else:
    st.error("❌ Revisa los Secrets en Streamlit.")
    st.stop()

# --- 2. CONFIGURACIÓN (TUS IDs OFICIALES) ---
PROJECT_ID = "subida-fotos-drive" #
LOCATION = "europe-west1" 

vertexai.init(project=PROJECT_ID, location=LOCATION, credentials=creds)

# --- 3. HERRAMIENTAS ---
# Activamos el buscador siguiendo la lógica de herramientas [cite: 75, 125]
tools = [
    Tool.from_google_search_retrieval(
        grounding.GoogleSearchRetrieval()
    )
]

# --- 4. MODELO (GEMINI-2.5-PRO) ---
# Usamos el ID exacto que aparece en tu tabla de modelos estables
model = GenerativeModel(
    model_name="gemini-2.5-pro", 
    tools=tools
)

# --- 5. INTERFAZ ---
st.title("🚜 Paso 1: Lista de Resultados Reales")

tractor = st.text_input("Introduce modelo para listar anuncios:", "John Deere 6150M")

if st.button("Buscar Anuncios"):
    with st.spinner("Rastreando anuncios reales en España..."):
        try:
            # Solicitud simplificada para obtener una lista numerada [cite: 5, 473]
            prompt = (
                f"Enumera anuncios reales de {tractor} en venta en España. "
                "Para cada uno indica: Nombre del anuncio, Precio y la URL directa."
            )
            
            # Generamos el contenido según la estructura oficial [cite: 471, 491]
            response = model.generate_content(prompt)

            st.markdown("### 📝 Lista de Anuncios Encontrados:")
            
            # Extraemos el texto de la respuesta [cite: 35, 435, 474]
            if response.candidates and response.candidates[0].content.parts:
                st.write(response.candidates[0].content.parts[0].text)
            else:
                st.warning("No se encontraron anuncios disponibles en este momento.")

        except Exception as e:
            st.error(f"❌ Fallo técnico en el Paso 1: {str(e)}")

# Información del proyecto para tu referencia
st.sidebar.info(f"Proyecto Activo: {PROJECT_ID}")
