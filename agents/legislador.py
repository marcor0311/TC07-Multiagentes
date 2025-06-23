"""
agents/legislador.py

Agente Legislador:
------------------
• Recupera y sintetiza la legislación costarricense relevante para el periodo indicado.
• Devuelve un resumen ejecutivo en formato de viñetas claras y concisas.
• Evita llamadas innecesarias a la API si el contexto es insuficiente.
"""

from agents_utils import get_openai_model

PROMPT_LEGISLADOR = """
Eres un asistente legal corporativo experto en legislación costarricense. Tu tarea es revisar todas las leyes proporcionadas y generar un resumen ejecutivo para Cacti S.A., considerando el periodo especificado.

Formato esperado para cada entrada:
---LEGISLACION---
Año: [Año de promulgación]
Ley: [Nombre de la ley]
Artículo: [Número o descripción del artículo]
Tema: [Área temática de la ley]
Norma_Aplicada: [Nombre de la norma aplicable]
Resumen: [Resumen del artículo]
---FIN---

Utiliza este nuevo formato para procesar y resumir toda la información.

Instrucciones:
1. Incluye todas las leyes cuya clave "Año" esté en el rango proporcionado.
2. Para cada ley relevante:
   - Presenta en viñetas:
     • Nombre de la ley y artículo.
     • Breve resumen.
     • Año de la ley.
     • Implicaciones prácticas para Cacti S.A.
3. Mantén un lenguaje claro, profesional y no redundante.
4. Si no hay leyes relevantes, indica explícitamente "No se encontró legislación relevante."

Contenido:
{input}
"""


def responder_legislacion(contexto: str, anios_filtrados: list[int]) -> str:
    """
    Genera un resumen legal basado en las leyes encontradas en el contexto, usando un modelo de lenguaje.

    Args:
        contexto: Texto con extractos legislativos ya filtrados por RAG.
        anios_filtrados: Lista de años permitidos según el periodo de análisis.

    Returns:
        Un texto en español con viñetas ejecutivas. Si no hay contexto suficiente,
        devuelve un mensaje indicándolo.
    """
    contexto = contexto.strip()
    if not contexto or "---LEGISLACION---" not in contexto:
        return "No se encontró legislación relevante para el periodo solicitado."

    try:
        model = get_openai_model()
        respuesta = model.invoke(
            PROMPT_LEGISLADOR.format(input=contexto, periodo=", ".join(map(str, anios_filtrados)))
        )
        return str(respuesta).strip()
    except Exception:
        return (
            "Ocurrió un error al procesar la legislación. "
            "Por favor, intente de nuevo."
        )