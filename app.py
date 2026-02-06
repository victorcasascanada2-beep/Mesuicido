import streamlit as st
import vertexai
from google.oauth2 import service_account
from google.cloud import aiplatform

st.title("🛠 Diagnóstico de Conexión")

# PASO 1: Leer los Secrets
st.subheader("1. Lectura de Secrets")
if "google" in st.secrets:
    st.success("✅ Tag [google] encontrado en Secrets")
    creds_info = dict(st.secrets["google"])
    st.write(f"Proyecto detectado: `{creds_info.get('project_id')}`")
else:
    st.error("❌ No se encuentra el tag [google] en Secrets")
    st.stop()

# PASO 2: Validar la Clave Privada
st.subheader("2. Validación de Credenciales")
try:
    if "private_key" in creds_info:
        # Limpieza de seguridad para el formato de la clave
        creds_info["private_key"] = creds_info["private_key"].replace("\\n", "\n")
    
    credentials = service_account.Credentials.from_service_account_info(creds_info)
    st.success("✅ Formato de credenciales válido")
except Exception as e:
    st.error(f"❌ Error en el formato del JSON/Key: {e}")
    st.stop()

# PASO 3: Inicializar Vertex AI
st.subheader("3. Conexión con Vertex AI")
try:
    vertexai.init(
        project=creds_info["project_id"],
        location="us-central1", # Usamos us-central1 para la prueba inicial por ser la más estable
        credentials=credentials
    )
    st.success("✅ Vertex AI inicializado correctamente")
except Exception as e:
    st.error(f"❌ Error al inicializar Vertex AI: {e}")
    st.stop()

# PASO 4: Prueba de "Latido" (Ping)
st.subheader("4. Prueba de Respuesta (Ping)")
if st.button("Lanzar prueba de comunicación"):
    try:
        from vertexai.generative_models import GenerativeModel
        model = GenerativeModel("gemini-1.5-flash") # Usamos Flash por ser el más rápido para pruebas
        
        with st.spinner("Esperando respuesta de Gemini..."):
            response = model.generate_content("Hola, di 'Conexión OK'")
            st.write(f"Respuesta de la IA: **{response.text}**")
            st.success("🎉 ¡CONEXIÓN COMPLETA! El sistema está listo.")
    except Exception as e:
        st.error(f"❌ Error en la llamada a la IA: {e}")
        st.info("Nota: Revisa si el email de la cuenta de servicio tiene el rol 'Vertex AI User' en Google Cloud Console.")
