import streamlit as st
from google import genai
from google.oauth2 import service_account

# --- 1. CONEXIÓN (Copiada de tu ia_engine.py) ---
def conectar_vertex():
    if "google" in st.secrets:
        # IMPORTANTE: Creamos un dict nuevo porque st.secrets no deja escribir
        creds_dict = dict(st.secrets["google"])
        
        # Tu lógica exacta de limpieza de clave
        raw_key = str(creds_dict.get("private_key", ""))
        clean_key = raw_key.strip().strip('"').strip("'").replace("\\n", "\n")
        creds_dict["private_key"] = clean_key
        
        google_creds = service_account.Credentials.from_service_account_info(
            creds_dict, 
            scopes=["https://www.googleapis.com/auth/cloud-platform"]
        )
        
        # Cliente GenAI con el interruptor Vertex activado
        return genai.Client(
            vertexai=True, 
            project=creds_dict.get("project_id"), 
            location="us-central1", # O la que prefieras
            credentials=google_creds
        )
    return None

# --- 2. INTERFAZ ---
st.title("🚜 Paso 1: Lista con Gemini 2.5 Pro")

client = conectar_vertex()

tractor = st.text_input("Modelo de tractor:", "John Deere 6150M")

if st.button("Buscar Anuncios") and client:
    with st.spinner("Rastreando mercado..."):
        try:
            # Llamada idéntica a la de tu ia_engine.py
            response = client.models.generate_content(
                model="gemini-2.5-pro",
                contents=f"Busca anuncios reales de {tractor} en España. Dame una lista con: Nombre, Precio y URL.",
                config={
                    "tools": [{"google_search": {}}], # LA SOLUCIÓN DEFINITIVA
                    "temperature": 0.35
                }
            )

            st.markdown("### 📝 Resultados:")
            if response.text:
                st.write(response.text)
            else:
                st.warning("No se recibieron resultados.")

        except Exception as e:
            st.error(f"❌ Error en el motor: {str(e)}")
