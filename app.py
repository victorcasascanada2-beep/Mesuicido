import streamlit as st

st.title("🚜 Control de Errores")

# Intentamos cargar la librería de una forma que no bloquee la pantalla
try:
    import vertexai
    from vertexai.generative_models import GenerativeModel
    st.success("✅ ¡POR FIN! Las librerías de Google están instaladas.")
    st.info("Ahora ya podemos dar el siguiente paso hacia la búsqueda en Europa.")
except Exception as e:
    st.error("❌ Las librerías siguen sin cargar.")
    st.write(f"Error técnico: {e}")
    st.stop()

st.write("Si ves esto, el sistema está listo para el siguiente paso.")
