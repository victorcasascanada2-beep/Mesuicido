import streamlit as st
from google import genai
from google.oauth2 import service_account

# --- 1. CONEXIÓN (TU ESTÁNDAR DE ia_engine.py) ---
def conectar_ia():
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

# --- 2. FUNCIÓN DE RASTREO ESPECÍFICO ---
def buscar_en_agriaffaires(client, modelo):
    # Instrucción ultra-específica para forzar la búsqueda en el dominio
    prompt = (
        f"Actúa como un analista de mercado agrícola. "
        f"Busca anuncios actuales del tractor '{modelo}' en el portal agriaffaires.es. "
        "Necesito que generes una tabla comparativa con las siguientes columnas: "
        "| Modelo Exacto | Año | Horas | Ubicación | Precio | URL del Anuncio |"
    )
    
    try:
        response = client.models.generate_content(
            model="gemini-2.5-pro",
            contents=prompt,
            config={
                "tools": [{"google_search": {}}], # Usamos la búsqueda para saltar el bloqueo
                "temperature": 0.1 # Temperatura mínima para máxima precisión en datos
            }
        )
        return response.text
    except Exception as e:
        return f"❌ Error accediendo a Agriaffaires: {str(e)}"

# --- 3. INTERFAZ ---
st.title("🚜 Extractor Agriaffaires 2.5 Pro")

client = conectar_ia()

if client:
    modelo_tractor = st.text_input("Introduce modelo (ej: John Deere 6150M):")
    
    if st.button("Rastrear Agriaffaires"):
        if modelo_tractor:
            with st.spinner(f"Accediendo a Agriaffaires para {modelo_tractor}..."):
                tabla_resultados = buscar_en_agriaffaires(client, modelo_tractor)
                st.markdown("### 📊 Comparativa de Mercado (Agriaffaires)")
                st.markdown(tabla_resultados)
        else:
            st.warning("Por favor, introduce un modelo.")
