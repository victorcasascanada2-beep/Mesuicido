import streamlit as st
from google import genai
from google.oauth2 import service_account

# --- 1. TU CONEXIÓN ESTÁNDAR (La que no falla) ---
def conectar_ia():
    if "google" in st.secrets:
        creds_dict = dict(st.secrets["google"])
        raw_key = str(creds_dict.get("private_key", ""))
        creds_dict["private_key"] = raw_key.strip().strip('"').strip("'").replace("\\n", "\n")
        
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

# --- 2. MOTOR DE BÚSQUEDA PROFUNDA ---
def buscar_agriaffaires_masivo(client, modelo):
    # Definimos el "Barrido" para engañar al límite de 3 resultados
    prompt = (
        f"Busca de forma exhaustiva anuncios del tractor '{modelo}' en agriaffaires.es. "
        "Necesito que encuentres al menos 15 resultados diferentes. "
        "Para lograrlo, busca anuncios en diferentes zonas: Castilla y León, Galicia, Andalucía y Aragón. "
        "Presenta los resultados en una TABLA con: | Modelo | Año | Horas | Provincia | Precio | URL |"
    )
    
    try:
        response = client.models.generate_content(
            model="gemini-2.5-pro",
            contents=prompt,
            config={
                "tools": [{"google_search": {}}],
                "temperature": 0.2
            }
        )
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

# --- 3. INTERFAZ ---
st.title("🚜 Buscador de Alto Rendimiento")
client = conectar_ia()

if client:
    modelo = st.text_input("Modelo de tractor:", "John Deere 6150M")
    if st.button("Rastrear Mercado (15+ resultados)"):
        with st.spinner("Realizando barrido por zonas..."):
            tabla = buscar_agriaffaires_masivo(client, modelo)
            st.markdown(tabla)
