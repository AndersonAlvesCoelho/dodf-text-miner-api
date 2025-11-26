import os
import hashlib
import requests
from fastapi import HTTPException

STORAGE_DIR = "storage/pdf"

def get_pdf_storage_path(url_or_name: str):
    # cria hash estável p/ evitar conflitos
    pdf_hash = hashlib.md5(url_or_name.encode()).hexdigest()
    return os.path.join(STORAGE_DIR, f"{pdf_hash}.pdf")


def download_pdf_from_url(url: str):
    os.makedirs(STORAGE_DIR, exist_ok=True)

    pdf_path = get_pdf_storage_path(url)

    # Se o PDF já existe, não baixa novamente
    if os.path.exists(pdf_path):
        return pdf_path

    response = requests.get(url)

    if response.status_code != 200:
        raise HTTPException(400, "Erro ao baixar o PDF do DODF.")

    with open(pdf_path, "wb") as f:
        f.write(response.content)

    return pdf_path


def save_uploaded_pdf(upload_file):
    os.makedirs(STORAGE_DIR, exist_ok=True)

    pdf_path = get_pdf_storage_path(upload_file.filename)

    # Se já existe, reutiliza
    if os.path.exists(pdf_path):
        return pdf_path

    content = upload_file.file.read()

    with open(pdf_path, "wb") as f:
        f.write(content)

    return pdf_path
