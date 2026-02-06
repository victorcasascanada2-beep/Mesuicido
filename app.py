import streamlit as st
import vertexai

st.title("🔍 Buscador de Nombres Correctos")

try:
    import vertexai.generative_models as gm
    # Listamos todo lo que hay dentro de la librería para encontrar el nombre del buscador
    nombres_disponibles = dir(gm)
    
    st.write("### Piezas encontradas en la librería de Google:")
    
    # Buscamos si existe algo que se llame 'Search' o 'Retrieval'
    buscadores = [n for n in nombres_disponibles if "Search" in n or "Retrieval" in n]
    
    if buscadores:
        st.success(f"✅ ¡Encontrados! Los nombres correctos son: {buscadores}")
        st.info("Copia estos nombres y dímelos para que ajuste el código final.")
    else:
        st.warning("⚠️ No encuentro 'GoogleSearchRetrieval'. Veamos la lista completa:")
        st.code(nombres_disponibles)

except Exception as e:
    st.error(f"Ni siquiera puedo abrir la librería: {e}")
