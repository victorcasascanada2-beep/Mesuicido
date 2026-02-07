import streamlit as st
from google import genai
from google.oauth2 import service_account

# --- 1. CONEXIÓN (TU LÓGICA DE ia_engine.py - ESTO NO SE TOCA) ---
def conectar_vertex():
    if "google" in st.secrets:
        creds_dict = dict(st.secrets["google"])
        raw_key = str(creds_dict.get("private_key", ""))
        clean_key = raw_key.strip().strip('"').strip("'").replace("\\n", "\n")
        creds_dict["private_key"] = clean_key
        
        google_creds = service_account.Credentials.from_service_account_info(
            creds_dict, 
            scopes=["https://www.googleapis.com/auth/cloud-platform"]
        )
        
        return genai.Client(
            vertexai=True, 
            project=creds_dict.get("project_id"), 
            location="us-central1", 
            credentials=google_creds
        )
    return None

# --- 2. INTERFAZ ---
st.title("🚜 Paso 1: Rastreador Masivo (Sin Resúmenes)")

client = conectar_vertex()

tractor = st.text_input("Modelo de tractor:", "John Deere 6150M")

if st.button("Buscar Anuncios") and client:
    with st.spinner("Rastreando Agriaffaires y TopMaquinaria..."):
        try:
            # OPTIMIZACIÓN: Pedimos texto bruto sin formato para forzar más resultados
            prompt_masivo = (
                f"Busca TODOS los anuncios reales de '{tractor}' en agriaffaires.es y topmaquinaria.com. "
                "No hagas tablas, no resumas y no escribas introducciones. "
                "Dame cada anuncio en una línea simple con este formato: "
                "PORTAL | MODELO | AÑO | HORAS | PRECIO | URL"
            )

            response = client.models.generate_content(
                model="gemini-2.5-pro",
                contents=prompt_masivo,
                config={
                    "tools": [{"google_search": {}}],
                    "temperature": 0.1 # Bajamos temperatura para evitar inventos
                }
            )

            st.markdown("### 📝 Listado de anuncios encontrados:")
            if response.text:
                # Usamos st.text para que respete el formato de manguera de datos
                st.text(response.text)
            else:
                st.warning("No se recibieron resultados.")

        except Exception as e:
            st.error(f"❌ Error en el motor: {str(e)}")
