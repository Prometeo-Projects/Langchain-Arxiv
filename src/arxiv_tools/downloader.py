import requests
import fitz


def download_paper(paper_id=None, pdf_url=None, save_path="paper.pdf"):
    """
    Descarga un paper de arXiv y extrae su texto.

    Parameters
    ----------
    paper_id : str
        ID del paper en arXiv (ej: "1706.03762")
    pdf_url : str
        URL directa del PDF de arXiv
    save_path : str
        Ruta donde se guardará el PDF

    Returns
    -------
    full_text : str
        Texto completo extraído del paper
    """

    # 1️⃣ Construir URL
    if pdf_url is None:
        pdf_url = f"https://arxiv.org/pdf/{paper_id}.pdf"

    # 2️⃣ Descargar PDF
    response = requests.get(pdf_url)

    if response.status_code != 200:
        raise Exception("No se pudo descargar el paper")

    with open(save_path, "wb") as f:
        f.write(response.content)

    # 3️⃣ Abrir PDF con PyMuPDF
    doc = fitz.open(save_path)

    # 4️⃣ Extraer texto
    full_text = ""

    for page in doc:
        full_text += page.get_text()

    return full_text
