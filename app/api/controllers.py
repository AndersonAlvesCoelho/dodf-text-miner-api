from fastapi import HTTPException

from app.api.validators import validate_dodf_link, validate_pdf_file

from app.services.downloader import download_pdf_from_url, save_uploaded_pdf
from app.services.pdf_reader import extract_text_from_pdf_path

from app.api.pipeline.extractor import extract_sections
from app.api.pipeline.parser_sec_1 import extract_section_I
from app.api.pipeline.parser_sec_2 import extract_section_II

from app.api.cache import cache_get, cache_set

async def process_dodf_request(pdf_file, url, page, page_size):
    # Normalizar URL
    if isinstance(url, str):
        url = url.strip()
    else:
        url = None

    # --- Validação: precisa enviar OU url OU pdf ---
    if not url and not pdf_file:
        raise HTTPException(
            400,
            "Você deve enviar uma URL do DODF ou enviar um arquivo PDF."
        )

    # --- Usuário enviou os dois ---
    if url and pdf_file:
        raise HTTPException(
            400,
            "Envie apenas a URL OU o arquivo PDF, não os dois ao mesmo tempo."
        )

    # --- Caso envio URL ---
    if url:
        if not validate_dodf_link(url):
            raise HTTPException(400, "O link enviado não é do Diário Oficial do DF.")

        cache_key = f"url::{url}"
        pdf_path = download_pdf_from_url(url)

    # --- Caso envio PDF ---
    else:
        if pdf_file is None:
            raise HTTPException(400, "Nenhum arquivo PDF foi enviado.")

        validate_pdf_file(pdf_file)

        cache_key = f"file::{pdf_file.filename}"
        pdf_path = save_uploaded_pdf(pdf_file)

    # Cache
    cached = cache_get(cache_key)
    if cached:
        return cached

    # Processamento normal
    extracted_text = extract_text_from_pdf_path(pdf_path)
    sections = extract_sections(extracted_text)

    section_I = sections[0]["conteudo"]
    section_II = sections[1]["conteudo"]

    sec1 = extract_section_I(section_I)
    sec2 = extract_section_II(section_II)

    result = {
        "arquivo": pdf_path,
        "secoes": {
            "section_I": sec1,
            "section_II": sec2
        }
    }

    cache_set(cache_key, result)
    return result



def paginate_response(data, page, page_size):
    itens = data["secoes"]["1"] + data["secoes"]["2"]

    start = (page - 1) * page_size
    end = start + page_size

    return {
        "total": len(itens),
        "page": page,
        "page_size": page_size,
        "results": itens[start:end]
    }
