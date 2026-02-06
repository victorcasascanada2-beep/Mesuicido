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
        # Inicializamos la herramienta con el nombre nuevo
        herramientas = [configurar_herramientas()]
        model = GenerativeModel("gemini-2.5-pro")
        
        prompt = f"Busca ofertas de {modelo_tractor} en España. Dame una tabla con Modelo, Precio y Link."
        
        # Enviamos la consulta con el mapeo de herramientas actualizado
        response = model.generate_content(prompt, tools=herramientas)
        return response.text
    except Exception as e:
        # Si 'google_search' fallara como argumento, probamos el plan B de la API
        return f"Error en la consulta: {e}"
