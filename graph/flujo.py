# graph/flujo.py

import re
from rag.vectorstore import construir_vectorstore
from agents.redactor_legal import redactar_respuesta_legal, generar_pdf

def ejecutar_flujo_legal(pregunta: str, empresa: str, periodo: str) -> str:
    """
    Ejecuta el flujo legal completo: filtra años, recupera documentos, redacta el resumen legal y genera un PDF.
    """

    anios = sorted(set(int(a) for a in re.findall(r"\d{4}", periodo)))
    if not anios:
        return "No se detectaron años válidos en el periodo proporcionado."

    # Construir el vectorstore filtrando solo por los años relevantes
    vs = construir_vectorstore(anios_filtrados=anios)

    # Recuperar documentos clave usando el vectorstore correcto por tipo
    contexto = {
        "contrato": [d.page_content for d in vs["contrato"].similarity_search(f"contratos firmados {empresa}", k=20)] if "contrato" in vs else [],
        "jurisprudencia": [d.page_content for d in vs["jurisprudencia"].similarity_search(f"jurisprudencia aplicable {empresa}", k=20)] if "jurisprudencia" in vs else [],
        "finanzas": [d.page_content for d in vs["finanzas"].similarity_search(f"libros contables de {empresa}", k=20)] if "finanzas" in vs else [],
        "estatutos": [d.page_content for d in vs["estatutos"].similarity_search(f"estatutos de {empresa}", k=5)] if "estatutos" in vs else [],
        "legislacion": [d.page_content for d in vs["legislacion"].similarity_search(f"legislación relevante {empresa}", k=10)] if "legislacion" in vs else []
    }

    total_docs = sum(len(v) for v in contexto.values())

    # Redactar respuesta legal
    resumen = redactar_respuesta_legal(contexto, anio_inicio=anios[0], anio_fin=anios[-1])

    # Generar PDF
    generar_pdf(resumen)

    return resumen