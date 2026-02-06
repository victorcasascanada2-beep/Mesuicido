import streamlit as st
import vertexai
from vertexai.generative_models import GenerativeModel, Tool, grounding

# --- CONFIGURACIÓN ---
PROJECT_ID = "236500839928" 
REGION_MODELO = "europe-west1" 
# Tu ID de motor exacto
ID_DEL_ALMACEN = "tasador-maquinaria-v1_1770400616700" 

vertexai.init(project=PROJECT_ID, location=REGION_MODELO)

def configurar_herramientas():
    """Corregido: usamos 'datastore' como sugiere el error"""
    return Tool.from_retrieval(
        grounding.Retrieval(
            grounding.VertexAISearch(
                datastore=ID_DEL_ALMACEN, # Cambiado de data_store_id a datastore
                project=PROJECT_ID,
                location="eu" # Mantenemos Europa
            )
        )
    )

def ejecutar_busqueda(modelo_tractor):
    try:
        model = GenerativeModel("gemini-1.5-pro") 
        prompt = f"Busca ofertas de {modelo_tractor} en España. Dame una tabla con Modelo, Precio y Link."
        
        # Inyectamos la herramienta corregida
        response = model.generate_content(prompt, tools=[configurar_herramientas()])
        return response.text
    except Exception as e:
        return f"Error en el intento: {str(e)}"

# --- INTERFAZ ---
st.title("🚜 Tasador Maestro")
modelo = st.text_input("Modelo del tractor:", "John Deere 6150M")

if st.button("Buscar y Tasar"):
    if modelo:
        with st.spinner("Consultando Milanuncios y Agriaffaires..."):
            st.markdown(ejecutar_busqueda(modelo))
