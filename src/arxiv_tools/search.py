#!/usr/bin/env python3
"""
ArXiv Paper Searcher
====================
Busca papers científicos en arXiv de forma sencilla.

Instalación:
    pip install arxiv

Uso como librería:
    from arxiv_searcher import arxiv_query
    papers = arxiv_query("machine learning", 5)
    for p in papers:
        print(p['title'])

Uso en terminal:
    python arxiv_searcher.py "Riemann Hypothesis" --limit 5
"""

import arxiv
import json
import argparse
from typing import List, Dict, Optional


def arxiv_query(query: str, nro_respuestas: int = 10) -> List[Dict]:
    """
    Busca papers en arXiv y retorna lista de diccionarios.

    Args:
        query: Término de búsqueda (ej: "Riemann Hypothesis", "quantum computing")
        nro_respuestas: Número máximo de papers a retornar (default: 10)

    Returns:
        Lista de diccionarios con keys: id, title, summary, pdf_url, authors, published

    Raises:
        Exception: Si hay error de conexión o la query es inválida

    Example:
        >>> papers = arxiv_query("General Relativity", 2)
        >>> print(papers[0]['title'])
        'On the General Relativity...'
    """
    try:
        search = arxiv.Search(
            query=query,
            max_results=nro_respuestas,
            sort_by=arxiv.SortCriterion.Relevance
        )

        papers_list = []
        for result in search.results():
            paper_dict = {
                "id": result.entry_id.split('/')[-1],
                "title": result.title,
                "summary": result.summary,
                "pdf_url": result.pdf_url,
                "authors": [str(author) for author in result.authors],
                "published": result.published.strftime("%Y-%m-%d") if result.published else None
            }
            papers_list.append(paper_dict)

        return papers_list

    except Exception as e:
        raise Exception(f"Error buscando en arXiv: {str(e)}")
