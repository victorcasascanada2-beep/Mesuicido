import streamlit as st
import vertexai
from vertexai.generative_models import GenerativeModel, Tool, grounding

# --- CONFIGURACIÓN DE GOOGLE CLOUD ---
PROJECT_ID = "236500839928" 
# Usamos una región específica para inicializar el modelo Gemini
REGION_MODELO = "europe-west1" 
# Tu ID de motor exacto que vive en la multirregión 'eu'
ENGINE_ID = "projects/236500839928/locations/eu/collections/default_collection/engines/tasador-maquinaria-v1_1770400616700"

# Inicialización correcta para Europa
vertexai.init(project=PROJECT_ID, location=REGION_MODELO)

def configurar_herramientas():
    """Conexión ultra-segura desglosando los datos para evitar errores de ID"""
    search_tool = Tool.from_retrieval(
        retrieval=grounding.Retrieval(
            vertex_ai_search=grounding.VertexAISearch(
                # En lugar de la ruta larga, usamos solo el ID final
                datastore="tasador-maquinaria-v1_1770400616700", 
                # Le decimos explícitamente el proyecto y la ubicación
                project="236500839928",
                location="eu" 
            )
        )
    )
    return search_tool
def ejecutar_busqueda(modelo_tractor):
    """Ejecuta la tasación usando Gemini 1.5 Pro"""
    try:
        herramientas = [configurar_herramientas()]
        model = GenerativeModel("gemini-1.5-pro") 
        
        prompt = f"""
        Busca ofertas de {modelo_tractor} en España usando tus fuentes (Milanuncios, Agriaffaires). 
        Dame una tabla con: Modelo, Precio, Horas y Link. 
        Calcula un precio medio al final.
        """
        
        response = model.generate_content(prompt, tools=herramientas)
        return response.text
    except Exception as e:
        return f"⚠️ Error en la consulta: {str(e)}"

# --- INTERFAZ STREAMLIT ---
st.set_page_config(page_title="Tasador Agrícola", layout="centered")
st.title("🚜 Tasador de Tractores")

modelo = st.text_input("¿Qué modelo quieres tasar?", placeholder="Ej: John Deere 6150M")

if st.button("Buscar Ofertas"):
    if modelo:
        with st.spinner("Buscando en Milanuncios y Agriaffaires..."):
            resultado = ejecutar_busqueda(modelo)
            st.markdown(resultado)
    else:
        st.warning("Introduce un modelo para empezar.")
