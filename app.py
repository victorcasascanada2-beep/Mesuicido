import streamlit as st
from google import genai
from google.oauth2 import service_account

# --- 1. CONEXIÓN (Basada al 100% en tu 1puntocero.txt) ---
def conectar_ia():
    if "google" in st.secrets:
        creds_dict = st.secrets["google"]
        # Limpieza de la clave privada (tal cual lo tienes en tu txt)
        raw_key = str(creds_dict.get("private_key", ""))
        clean_key = raw_key.strip().strip('"').strip("'").replace("\\n", "\n")
        creds_dict["private_key"] = clean_key
        
        google_creds = service_account.Credentials.from_service_account_info(
            creds_dict, 
            scopes=["https://www.googleapis.com/auth/cloud-platform"]
        )
        
        # Conexión profesional a Vertex AI
        return genai.Client(
            vertexai=True, 
            project=creds_dict.get("project_id"), 
            location="europe-west1", 
            credentials=google_creds
        )
    return None

# Inicializamos el cliente
client = conectar_ia()

# --- 2. INTERFAZ ---
st.title("🚜 Paso 1: Lista de Anuncios (Motor 2.5 Pro)")

tractor = st.text_input("Modelo de tractor para listar:", "John Deere 6150M")

if st.button("Buscar Anuncios") and client:
    with st.spinner("Rastreando anuncios reales en España..."):
        try:
            # Esta es la llamada que funciona en tu archivo 1puntocero.txt
            response = client.models.generate_content(
                model="gemini-2.5-pro",
                contents=f"Busca anuncios reales de {tractor} en España. Dame una lista con: Nombre del anuncio, Precio y URL.",
                config={
                    # La sintaxis que arregla el Error 400
                    "tools": [{"google_search": {}}],
                    "temperature": 0.3
                }
            )

            st.markdown("### 📝 Resultados encontrados:")
            if response.text:
                st.write(response.text)
            else:
                st.warning("No se han encontrado resultados. Prueba con otro modelo.")

        except Exception as e:
            st.error(f"❌ Error con el nuevo motor: {str(e)}")
            if "404" in str(e):
                st.info("Revisa que el ID del proyecto sea correcto en los secrets.")

elif not client:
    st.error("No se ha podido conectar con Vertex AI. Revisa tus credenciales.")
