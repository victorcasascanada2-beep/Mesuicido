import streamlit as st
import vertexai
from vertexai.generative_models import GenerativeModel, Tool, grounding

# --- DATOS DE TU PROYECTO ---
PROJECT_ID = "236500839928" 
REGION_MODELO = "europe-west1" 
# Tu ID de motor en la multirregión europea
DATA_STORE_PATH = "projects/236500839928/locations/eu/collections/default_collection/engines/tasador-maquinaria-v1_1770400616700"

vertexai.init(project=PROJECT_ID, location=REGION_MODELO)

def configurar_herramientas():
    """Configuración estándar para Vertex AI Search en la web"""
    # Usamos 'VertexAISearch' que es el nombre del componente que creamos
    search_tool = Tool.from_retrieval(
        grounding.Retrieval(
            vertex_ai_search=grounding.VertexAISearch(
                datastore=DATA_STORE_PATH,
                location="eu"
            )
        )
    )
    return search_tool

def ejecutar_busqueda(modelo_tractor):
    try:
        herramientas = [configurar_herramientas()]
        model = GenerativeModel("gemini-1.5-pro") 
        
        prompt = f"Busca ofertas de {modelo_tractor} en España. Dame una tabla con Modelo, Precio y Link."
        
        # Grounding con tus datos de Milanuncios/Agriaffaires
        response = model.generate_content(prompt, tools=herramientas)
        return response.text
    except Exception as e:
        # Este mensaje nos dirá el nombre exacto que falta si falla
        return f"Error detectado: {str(e)}"

# --- INTERFAZ ---
st.title("🚜 Tasador Pro Web")
modelo = st.text_input("Modelo del tractor:")
if st.button("Tasar"):
    if modelo:
        with st.spinner("Buscando en tus fuentes de Europa..."):
            st.markdown(ejecutar_busqueda(modelo))
