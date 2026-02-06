import streamlit as st
import vertexai
import inspect

st.title("🛠 Mapeo de Estructura Vertex AI")

def explorar_libreria():
    resultados = {}
    try:
        # 1. Intentamos importar el módulo base
        import vertexai.generative_models as gm
        resultados["Modo"] = "Módulo cargado"
        
        # 2. Buscamos todas las clases disponibles que suenen a Búsqueda o Tool
        todas_las_clases = [name for name, obj in inspect.getmembers(gm) if inspect.isclass(obj) or inspect.ismodule(obj)]
        resultados["Clases_Disponibles"] = todas_las_clases
        
        # 3. Buscamos específicamente herramientas de 'grounding' (donde suele vivir la búsqueda)
        if hasattr(gm, 'grounding'):
            resultados["Grounding_Submodule"] = dir(gm.grounding)
            
        return resultados
    except Exception as e:
        return {"Error": str(e)}

# Ejecución y visualización
analisis = explorar_libreria()

if "Error" in analisis:
    st.error(f"Fallo crítico en la librería: {analisis['Error']}")
    st.info("Sugerencia: Cambia 'google-cloud-aiplatform' por 'google-cloud-aiplatform>=1.70.0' en requirements.txt")
else:
    st.success("✅ Estructura mapeada con éxito")
    st.write("### Nombres de variables reales en tu servidor:")
    st.json(analisis)

st.divider()
st.write("Copia el bloque de texto de arriba y lo usamos para escribir la función de búsqueda definitiva.")
