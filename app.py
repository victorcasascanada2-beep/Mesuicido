import streamlit as st
import vertexai
from vertexai.generative_models import GenerativeModel, Tool, grounding

# --- CONFIGURACIÓN ESTÁTICA ---
PROJECT_ID = "236500839928" 
REGION_MODELO = "europe-west1" 
# Solo el ID final, sin el prefijo "projects/..."
DATA_STORE_ID = "tasador-maquinaria-v1_1770400616700" 

vertexai.init(project=PROJECT_ID, location=REGION_MODELO)

def configurar_herramientas():
    """Configuración desglosada para cumplir con el requisito del error"""
    return Tool.from_retrieval(
        grounding.Retrieval(
            grounding.VertexAISearch(
                # Pasamos las 3 piezas por separado como exige el mensaje de error
                data_store_id=DATA_STORE_ID,
                project=PROJECT_ID,
                location="eu" # Tu ubicación multirregión
            )
        )
    )

def ejecutar_busqueda(modelo_tractor):
    try:
        model = GenerativeModel("gemini-1.5-pro") 
        prompt = f"Busca ofertas de {modelo_tractor} en España. Tabla con precio, horas y link."
        
        # Inyectamos la herramienta configurada por piezas
        response = model.generate_content(prompt, tools=[configurar_herramientas()])
        return response.text
    except Exception as e:
        return f"Error en el intento: {str(e)}"

# --- INTERFAZ ---
st.title("🚜 Tasador Agrícola Pro")
modelo = st.text_input("Modelo de tractor a tasar:", "John Deere 6150M")

if st.button("Buscar en Milanuncios"):
    with st.spinner("Pidiendo permiso a Google Cloud Europa..."):
        st.markdown(ejecutar_busqueda(modelo))
