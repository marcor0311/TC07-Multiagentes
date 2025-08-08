# TC07 Multi agentes

[Video de Presentación](https://drive.google.com/file/d/1VMgCbDIQcOl8HY2lbyLXFEq-h8lzNETi/view?usp=sharing)

![image](https://github.com/user-attachments/assets/92ad01c1-a103-426e-aeb1-3ed508212845)

Caso escogido: Asistente Legal Inteligente: Ayuda a redactar respuestas legales a partir de legislación, jurisprudencia y contratos.

Sistema multi‑agente basado en **LangChain** + **LangGraph** que genera informes legales automatizados para **Cacti S.A.**.  
Combina recuperación semántica (RAG sobre **Chroma**) y generación con **OpenAI GPT‑4o** para analizar contratos, jurisprudencia y legislación y entregar un PDF ejecutivo.

---

## Estructura

```
.
├── agents/
│   ├── jurisprudente.py   # Análisis de jurisprudencia
│   ├── legislador.py      # Síntesis de legislación
│   └── redactor_legal.py  # Orquestador + RAG + PDF
├── data/                  # Contratos, jurisprudencia y leyes en texto
├── graph/
│   └── flujo.py           # Definición del flujo LangGraph
├── main.py                # Punto de entrada
└── requirements.txt
```

---

## Requisitos

```bash
python -m venv .venv
source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

---

## Variable de entorno

El sistema usa la API de OpenAI para **embeddings** y generación:

```bash
export OPENAI_API_KEY="tu‑clave‑api"
```

- Asegúrate de tener acceso al modelo **gpt‑4o** y al endpoint de *embeddings*.
- En Windows PowerShell: `$Env:OPENAI_API_KEY="tu‑clave‑api"`

---

## Ejecución

```bash
python main.py
```

---

## Arquitectura

- **Usuario** → dispara el flujo y recibe el informe.
- **Agentes IA** (Langchain/LangGraph): *legislador*, *jurisprudente*, *redactor_legal*.
- **Chroma Vector Store** almacena contratos, jurisprudencia y legislación.
- **Embeddings usando OpenaAI API** crea/actualiza vectores (dotted arrows en el diagrama).
- **GPT‑4o API** responde prompts del *redactor_legal* (RAG).
