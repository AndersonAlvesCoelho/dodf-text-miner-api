from fastapi import APIRouter, UploadFile, File, Form
from app.api.controllers import process_dodf_request

router = APIRouter()

@router.post("/process")
async def process_endpoint(
    pdf_file: UploadFile = File(None),
    url: str = Form(None),
    page: int = Form(1),
    page_size: int = Form(50)
):
    return await process_dodf_request(pdf_file, url, page, page_size)


@router.get("/")
def root():
    return {"status": "ok", "message": "API funcionando!"}