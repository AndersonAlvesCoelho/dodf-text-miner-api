import re
from fastapi import HTTPException

def validate_dodf_link(url: str) -> bool:
    pattern = r"^https:\/\/dodf\.df\.gov\.br\/.*visualizar-pdf.*arquivo=.*\.pdf"
    return re.search(pattern, url) is not None

def validate_pdf_file(file):
    if file is None:
        return
    
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(400, "Arquivo enviado não é um PDF.")
