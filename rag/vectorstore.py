from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from rag.loader import cargar_documentos
from rag.splitter import dividir_documentos
import os

CHROMA_PATH = "rag/chroma_db"

def construir_vectorstore(anios_filtrados: list[int] = None):
    print("[VECTORSTORE] Iniciando carga y división de documentos...")
    documentos = cargar_documentos()
    chunks = dividir_documentos(documentos)

    # Separar por tipo
    contratos = [c for c in chunks if c.metadata.get("tipo") == "contrato"]
    jurisprudencia = [c for c in chunks if c.metadata.get("tipo") == "jurisprudencia"]
    finanzas = [c for c in chunks if c.metadata.get("tipo") in ("finanzas", "libro_contables")]
    estatutos = [c for c in chunks if c.metadata.get("tipo") == "estatutos"]
    legislacion = [c for c in chunks if c.metadata.get("tipo") == "legislacion"]

    def filtrar_anios(lista):
        if not anios_filtrados:
            return lista
        # Mantener solo los chunks cuyo metadato "año" (o "Año") coincida, manejando espacios y mayúsculas/minúsculas
        return [
            chunk
            for chunk in lista
            if (
                (a := chunk.metadata.get("año") or chunk.metadata.get("Año"))
                and str(a).strip().isdigit()
                and int(str(a).strip()) in anios_filtrados
            )
        ]

    contratos = filtrar_anios(contratos)
    jurisprudencia = filtrar_anios(jurisprudencia)
    finanzas = filtrar_anios(finanzas)
    estatutos = filtrar_anios(estatutos)
    legislacion = filtrar_anios(legislacion)

    # Obtener la API key desde las variables de entorno
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("La API key de OpenAI no está configurada en las variables de entorno.")

    embeddings = OpenAIEmbeddings(
        model="text-embedding-ada-002",
        api_key=api_key
    )

    print("[VECTORSTORE] Construyendo índices vectoriales separados...")
    # Asegurar que los subdirectorios existan
    for sub in ("contrato", "jurisprudencia", "finanzas", "estatutos", "legislacion"):
        os.makedirs(f"{CHROMA_PATH}/{sub}", exist_ok=True)

    vectorstores = {}
    if contratos:
        vectorstores["contrato"] = Chroma.from_documents(documents=contratos, embedding=embeddings, persist_directory=CHROMA_PATH+"/contrato")
    if jurisprudencia:
        vectorstores["jurisprudencia"] = Chroma.from_documents(documents=jurisprudencia, embedding=embeddings, persist_directory=CHROMA_PATH+"/jurisprudencia")
    if finanzas:
        vectorstores["finanzas"] = Chroma.from_documents(documents=finanzas, embedding=embeddings, persist_directory=CHROMA_PATH+"/finanzas")
    if estatutos:
        vectorstores["estatutos"] = Chroma.from_documents(documents=estatutos, embedding=embeddings, persist_directory=CHROMA_PATH+"/estatutos")
    if legislacion:
        vectorstores["legislacion"] = Chroma.from_documents(documents=legislacion, embedding=embeddings, persist_directory=CHROMA_PATH+"/legislacion")
    print("[VECTORSTORE] Vectorstores generados exitosamente.")
    return vectorstores