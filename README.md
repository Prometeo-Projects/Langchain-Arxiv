# ArXiv Tools

`arxiv_tools` es una biblioteca en Python diseñada para buscar, descargar y procesar papers científicos desde arXiv. Además, incluye herramientas integradas para indexar el contenido en una base de datos vectorial (ChromaDB) y crear agentes conversacionales utilizando LangChain.

## Características Principales

*   **Búsqueda en arXiv:** Busca papers por título, autor o tema.
*   **Descarga y Extracción:** Descarga los PDFs de arXiv y extrae su texto completo utilizando PyMuPDF (`fitz`).
*   **Indexación Vectorial:** Fragmenta el texto y lo almacena en una base de datos Chroma local utilizando embeddings de HuggingFace (`sentence-transformers`).
*   **Integración con LangChain:** Incluye herramientas (`@tool`) listas para ser consumidas por agentes de IA.

## Instalación

Para utilizar esta biblioteca, necesitas instalar las siguientes dependencias:

```bash
pip install arxiv requests pymupdf langchain langchain-community sentence-transformers chromadb
```

## Estructura del Proyecto

El código fuente se encuentra en `src/arxiv_tools/`:
*   `search.py`: Contiene `arxiv_query()` para buscar metadatos de papers.
*   `downloader.py`: Contiene `download_paper()` para descargar y extraer el texto de un PDF.
*   `indexer.py`: Contiene `save_to_vdb()` para chunkear el texto y guardarlo en ChromaDB.
*   `tools.py`: Contiene `arxiv_download_tool`, una herramienta de LangChain.

## Uso Básico

### 1. Buscar un Paper

Puedes buscar papers relacionados con un tema específico:

```python
from src.arxiv_tools.search import arxiv_query

papers = arxiv_query("quantum computing", nro_respuestas=2)
for p in papers:
    print(f"Título: {p['title']}")
    print(f"ID: {p['id']}\n")
```

### 2. Descargar y Extraer Texto

Dado el ID de un paper, descárgalo y obtén su texto:

```python
from src.arxiv_tools.downloader import download_paper

# El ID suele ser el número al final de la URL de arXiv (ej: 1706.03762)
texto_paper = download_paper(paper_id="1706.03762")
print(texto_paper[:500]) # Muestra los primeros 500 caracteres
```

### 3. Guardar en Base de Datos Vectorial

Puedes indexar el texto extraído en ChromaDB para realizar búsquedas semánticas posteriormente (RAG):

```python
from src.arxiv_tools.indexer import save_to_vdb

metadata = {"source": "arxiv", "paper_id": "1706.03762", "title": "Attention Is All You Need"}
vdb = save_to_vdb(full_text=texto_paper, metadata=metadata, persist_directory="./mi_vdb")

print(f"Documentos guardados en: ./mi_vdb")
```

## Uso con Agentes de LangChain

La biblioteca incluye una herramienta lista para usar (`arxiv_download_tool`) que puedes proporcionar a un agente de LangChain para que investigue papers de forma autónoma.

### Ejemplo de Configuración de un Agente

```python
from langchain.agents import initialize_agent, AgentType
from langchain_openai import ChatOpenAI # O el LLM de tu preferencia
from src.arxiv_tools.tools import arxiv_download_tool

# 1. Inicializar el LLM
llm = ChatOpenAI(temperature=0, model="gpt-4o-mini")

# 2. Definir la lista de herramientas del agente
tools = [arxiv_download_tool]

# 3. Inicializar el agente
agente = initialize_agent(
    tools,
    llm,
    agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# 4. Ejecutar el agente
respuesta = agente.run("Por favor, descarga el paper con ID '1706.03762' de arXiv y hazme un resumen de la introducción.")
print(respuesta)
```

En este ejemplo, el agente será capaz de utilizar la herramienta para descargar el PDF, leer su contenido de forma interna y responder a tu pregunta basándose en el texto real del paper.
