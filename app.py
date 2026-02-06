def configurar_herramientas():
    """Ajustado al nuevo estándar 'google_search' pedido por el error 400"""
    import vertexai.generative_models as gm
    
    # El error dice: "please use google_search field instead"
    # En las versiones más nuevas, esto se hace pasando el objeto directamente al Tool
    search_query_tool = Tool.from_google_search_retrieval(
        google_search=gm.grounding.GoogleSearchRetrieval() 
    )
    return search_query_tool

def ejecutar_busqueda(modelo_tractor):
    """Lógica con Gemini 2.5 Pro y el nuevo campo de búsqueda"""
    try:
        # Inicializamos la herramienta con el nombre nuevoimport streamlit as st
import vertexai
from vertexai.generative_models import GenerativeModel, Tool, grounding

# --- CONFIGURACIÓN DE GOOGLE CLOUD ---
# Usamos los datos exactos de tus capturas
PROJECT_ID = "236500839928" 
LOCATION = "eu"  # Tu app vive en la región europea
# Tu ID de motor recuperado de la pestaña API
ENGINE_ID = "projects/236500839928/locations/eu/collections/default_collection/engines/tasador-maquinaria-v1_1770400616700"

# Inicializamos Vertex AI con la ubicación europea
vertexai.init(project=PROJECT_ID, location=LOCATION)

def configurar_herramientas():
    """Conecta Gemini con tu App de Vertex AI Search (Milanuncios, Agriaffaires)"""
    # Configuramos la herramienta para que use tu Data Store específico
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
    """Lógica de tasación usando el cerebro de Gemini y tus fuentes de datos"""
    try:
        # Cargamos tu herramienta personalizada
        herramientas = [configurar_herramientas()]
        
        # Usamos el modelo pro para mayor precisión en la comparativa
        model = GenerativeModel("gemini-1.5-pro") 
        
        prompt = f"""
        Eres un experto tasador de maquinaria agrícola en España.
        Tu tarea es buscar ofertas actuales de: {modelo_tractor}
        
        Instrucciones:
        1. Consulta exclusivamente las fuentes configuradas (Milanuncios, Agriaffaires).
        2. Extrae el precio, las horas de uso, el año de fabricación y el enlace.
        3. Genera una tabla comparativa con estos datos.
        4. Al final, da una conclusión sobre cuál es el 'precio justo' de mercado para este modelo.
        """
        
        # Generar contenido con el soporte de tus datos (Grounding)
        response = model.generate_content(prompt, tools=herramientas)
        return response.text
    except Exception as e:
        return f"⚠️ Error en la consulta: {str(e)}"

# --- INTERFAZ DE USUARIO CON STREAMLIT ---
def main():
    st.set_page_config(page_title="Tasador IA - Maquinaria Agrícola", layout="wide")
    
    st.title("🚜 Tasador Pro de Maquinaria")
    st.subheader("Búsqueda inteligente en Milanuncios y Agriaffaires")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        modelo = st.text_input("Introduce el modelo del tractor (ej. John Deere 6150M):")
        if st.button("Buscar y Tasar"):
            if modelo:
                with st.spinner(f"Buscando ofertas de {modelo} en España..."):
                    resultado = ejecutar_busqueda(modelo)
                    st.markdown(resultado)
            else:
                st.warning("Por favor, introduce un modelo para buscar.")

    with col2:
        st.info("""
        **Configuración Activa:**
        - **Región:** Europa (eu)
        - **Fuentes:** Indexación automática de sitios web
        - **Motor:** Vertex AI Search v1
        """)

if __name__ == "__main__":
    main()
        herramientas = [configurar_herramientas()]
        model = GenerativeModel("gemini-2.5-pro")
        
        prompt = f"Busca ofertas de {modelo_tractor} en España. Dame una tabla con Modelo, Precio y Link."
        
        # Enviamos la consulta con el mapeo de herramientas actualizado
        response = model.generate_content(prompt, tools=herramientas)
        return response.text
    except Exception as e:
        # Si 'google_search' fallara como argumento, probamos el plan B de la API
        return f"Error en la consulta: {e}"
