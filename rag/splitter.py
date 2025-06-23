"""
rag/splitter.py

Divide los documentos cargados en fragmentos semánticos únicamente cuando su
longitud supera el `chunk_size` especificado. Esto evita sobre‑fragmentar
documentos cortos (por ejemplo, un solo artículo de ley) y reduce llamadas
innecesarias al modelo en la fase de RAG.
"""

from typing import List

from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

DEFAULT_CHUNK_SIZE = 600
DEFAULT_CHUNK_OVERLAP = 80


def _needs_split(text: str, threshold: int) -> bool:
    """True si el texto supera el umbral y requiere división."""
    return len(text) > threshold


def dividir_documentos(
    documentos: List[Document],
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    chunk_overlap: int = DEFAULT_CHUNK_OVERLAP,
) -> List[Document]:
    """
    Divide los documentos en fragmentos solo cuando sea necesario.

    • Para documentos cortos (<= chunk_size) devuelve el documento tal cual.
    • Para documentos largos usa RecursiveCharacterTextSplitter respetando solapamiento.
    • Conservar metadatos originales en los fragmentos resultantes.
    """
    if not documentos:
        print("No hay documentos para dividir.")
        return []

    print(f"Total documentos recibidos: {len(documentos)}")

    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        encoding_name="cl100k_base",
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )

    chunks: List[Document] = []
    for doc in documentos:
        if _needs_split(doc.page_content, chunk_size):
            # Mantener metadatos en cada fragmento
            sub_docs = splitter.split_documents([doc])
            for sub in sub_docs:
                sub.metadata.update(doc.metadata)
            chunks.extend(sub_docs)
        else:
            chunks.append(doc)

    print(f"Fragmentos generados: {len(chunks)}")
    return chunks