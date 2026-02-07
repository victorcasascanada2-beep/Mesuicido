def extraer_mercado_bruto(client, modelo):
    # Prompt ultra-simplificado para maximizar cantidad
    prompt = (
        f"Busca TODOS los anuncios de '{modelo}' en agriaffaires.es y topmaquinaria.com. "
        "Dámelo en texto plano, sin tablas, sin negritas, sin enumerar. "
        "Solo quiero una línea por anuncio con este formato exacto: "
        "PORTAL - MODELO - AÑO - HORAS - PRECIO - URL"
    )
    
    try:
        response = client.models.generate_content(
            model="gemini-2.5-pro",
            contents=prompt,
            config={
                "tools": [{"google_search": {}}],
                "temperature": 0.1, # Precisión máxima
            }
        )
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"
