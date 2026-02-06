import streamlit as st
import vertexai
from vertexai.generative_models import GenerativeModel, Tool, grounding

# --- CONFIGURACIÓN DE GOOGLE CLOUD ---
# Datos extraídos de tus capturas
PROJECT_ID = "236500839928" 
LOCATION = "eu" 
ENGINE_ID = "projects/236500839928/locations/eu/collections/default_collection/engines/tasador-maquinaria-v1_1770400616700"

# Inicializamos Vertex AI fuera de las funciones para evitar errores de bloque
vertexai.init(project=PROJECT_ID, location=LOCATION)

def configurar_herramientas():
    """Conecta con tu App de Vertex AI Search en Europa"""
    search_tool = Tool.from_retrieval(
        retrieval=grounding.Retrieval(
            vertex_ai_search=grounding.VertexAISearch(
                datastore=ENGINE_ID,
                location=LOCATION
            )
        )
    )
    return search_tool

def ejecutar_busqueda(modelo_tractor):
    """Lógica de tasación con Gemini 2.5 Pro"""
    try:
        herramientas = [configurar_herramientas()]
        # Usamos el nombre oficial correcto para evitar el error de modelo
        model = GenerativeModel("gemini-2.5-pro") 
        
        prompt = f"""
        Eres un experto tasador de maquinaria agrícola en España.
        Busca ofertas actuales de: {modelo_tractor}
        Extrae precio, horas, año y enlace de Milanuncios y Agriaffaires.
        Genera una tabla comparativa y una conclusión de precio de mercado.
        """
        
        response = model.generate_content(prompt, tools=herramientas)
        return response.text
    except Exception as e:
        return f"⚠️ Error en la consulta: {str(e)}"

# --- INTERFAZ DE USUARIO ---
def main():
    st.set_page_config(page_title="Tasador IA - Maquinaria", layout="wide")
    st.title("🚜 Tasador Pro de Maquinaria")
    
    modelo = st.text_input("Introduce el modelo del tractor:")
    if st.button("Buscar y Tasar"):
        if modelo:
            with st.spinner("Consultando fuentes en España..."):
                resultado = ejecutar_busqueda(modelo)
                st.markdown(resultado)
        else:
            st.warning("Escribe un modelo primero.")

if __name__ == "__main__":
    main()
