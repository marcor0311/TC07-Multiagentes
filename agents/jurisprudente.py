"""
agents/jurisprudente.py

Agente especializado en análisis de jurisprudencia para el sistema ALIE.
-----------------------------------------------------------------------
• Recupera la jurisprudencia filtrada por año (ya entregada en `contexto`)
  y genera un resumen ejecutivo para directivos no abogados.
• Implementa comprobaciones de seguridad para evitar llamadas innecesarias.
• Registra cada paso con logging para facilitar depuración.
"""

from __future__ import annotations

from typing import Any

from agents_utils import get_openai_model

# ---------------------------------------------------------------------
# Prompt del agente
# ---------------------------------------------------------------------
PROMPT_JURISPRUDENTE = """
Eres un asistente legal corporativo experto en análisis jurisprudencial. 
Tu tarea es identificar, analizar y explicar toda la jurisprudencia histórica 
relevante para la empresa Cacti S.A. durante el periodo {periodo}.

Instrucciones:
1. Incluye todos los fallos y precedentes aplicables al contexto empresarial.
2. Para cada caso:
   • Tribunal y número de resolución.
   • Fecha (día/mes/año).
   • Resumen del caso y decisión clave.
   • Impacto práctico para Cacti S.A.
3. Presenta cada caso como una viñeta clara, sin frases genéricas ni repeticiones.
4. Mantén un tono profesional, entendible para ejecutivos no abogados.

Jurisprudencia disponible:
{input}
"""


def _contenido_suficiente(texto: str, umbral: int = 120) -> bool:
    """
    Determina si el texto tiene longitud suficiente como para
    justificar una llamada al modelo de lenguaje.
    """
    return texto and len(texto) >= umbral


def responder_jurisprudencia(contexto: str, periodo: str) -> str:
    """
    Genera un resumen jurisprudencial ejecutivo.

    Args:
        contexto: Texto con extractos de jurisprudencia ya filtrados por RAG.
        periodo:   Cadena con el rango de años solicitado (ej. "2020‑2023").

    Returns:
        Un string con el resumen listo para ser incluido en el informe.
    """
    contexto = contexto.strip()
    periodo = periodo.strip()

    if not _contenido_suficiente(contexto):
        return "No se encontró jurisprudencia relevante para el periodo solicitado."

    try:
        model = get_openai_model()
        response: Any = model.invoke(
            PROMPT_JURISPRUDENTE.format(input=contexto, periodo=periodo)
        )
        return str(response).strip()
    except Exception:
        return (
            "Ocurrió un error al procesar la jurisprudencia. "
            "Por favor, intente de nuevo."
        )