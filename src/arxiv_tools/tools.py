from langchain.tools import tool
from .downloader import download_paper

@tool
def arxiv_download_tool(paper_id: str):
    """Descarga un paper de arXiv y devuelve su texto."""

    text = download_paper(paper_id=paper_id)
    return text
