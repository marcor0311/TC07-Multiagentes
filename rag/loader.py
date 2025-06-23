"""
rag/loader.py

Carga documentos legales en formato segmentado:

    ---CONTRATO---         (o ---JURISPRUDENCIA--- / ---LEGISLACION---)
    <clave>: <valor>
    …
    ---FIN---

Para legislación, los segmentos intermedios usan simplemente `---` como separador.
Cada segmento se convierte en un `Document` con metadatos normalizados.
"""

import re
from pathlib import Path
from typing import List

from langchain_community.document_loaders import TextLoader
from langchain.docstore.document import Document

BASE_DIR = Path("data")
TIPOS = ["legislacion", "jurisprudencia", "contrato", "estatutos", "libro_contables"]

SEGMENT_RE = re.compile(r"^---(.*?)---$", re.MULTILINE)


def _segmentar_contenido(texto: str) -> List[str]:
    """
    Divide el texto en segmentos delimitados por líneas '---…---'.
    Para legislación, los segmentos internos también están separados por '---'.

    Retorna una lista de segmentos (cadenas) sin los marcadores.
    """
    bloques = []
    marcas = [m for m in SEGMENT_RE.finditer(texto)]
    if not marcas:
        # No hay separadores -> texto completo como un bloque
        return [texto.strip()]

    for i, match in enumerate(marcas):
        start = match.end()
        end = marcas[i + 1].start() if i + 1 < len(marcas) else len(texto)
        segmento = texto[start:end].strip()
        if segmento and segmento.upper() != "FIN":
            bloques.append(segmento)
    return bloques


def _parse_metadata(segmento: str, tipo: str) -> dict:
    """
    Extrae metadatos simples (año, mes, etc.) del segmento.
    """
    meta = {"tipo": tipo}
    for linea in segmento.splitlines():
        if ":" not in linea:
            continue
        clave, valor = [s.strip() for s in linea.split(":", 1)]
        clave_lower = clave.lower()
        if clave_lower in {"año", "ano", "year"}:
            meta["año"] = valor
        elif clave_lower in {"mes"}:
            meta["mes"] = valor
        elif clave_lower in {"empresa"}:
            meta["empresa"] = valor
        elif clave_lower in {"ley"}:
            meta["ley"] = valor
        elif clave_lower in {"artículo", "articulo"}:
            meta["articulo"] = valor
        elif clave_lower in {"resolución", "resolucion"}:
            meta["resolucion"] = valor
    return meta


def cargar_documentos() -> List[Document]:
    """
    Recorre los directorios en `data/` y carga cada archivo .txt,
    dividiéndolo según los marcadores '---…---'. Devuelve una lista
    de `Document` para usar en la fase de vectorización.
    """
    documentos: List[Document] = []

    for tipo in TIPOS:
        ruta = BASE_DIR / tipo
        if not ruta.exists():
            continue
        for archivo in ruta.glob("*.txt"):
            # Cargar texto completo
            loader = TextLoader(str(archivo))
            raw_docs = loader.load()  # regresa una lista con un Document
            if not raw_docs:
                continue
            texto = raw_docs[0].page_content
            # Dividir en segmentos
            segmentos = _segmentar_contenido(texto)
            for seg in segmentos:
                meta = _parse_metadata(seg, tipo)
                documentos.append(Document(page_content=seg.strip(), metadata=meta))

    print(f"[LOADER] Documentos cargados: {len(documentos)}")
    return documentos
