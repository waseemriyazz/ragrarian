from fastapi import APIRouter, UploadFile, File
from core.model import Query, Answer, RephraseRequest
from core.utils import process_pdf, handle_query, rephrase_text
import os

router = APIRouter()

@router.post("/upload_pdf")
async def upload_pdf(file: UploadFile = File(...)):
    file_path = f"data/{file.filename}"
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())
    
    process_pdf(file_path)
    return {"message": "PDF processed successfully"}

@router.post("/query", response_model=Answer)
async def query(query: Query):
    answer = handle_query(query.text)
    return Answer(text=answer)

@router.post("/rephrase", response_model=Answer)
async def rephrase(request: RephraseRequest):
    rephrased_text = rephrase_text(request.text, request.format_option)
    return Answer(text=rephrased_text)

@router.post("/delete_vector_databases")
async def delete_vector_databases():
    deleted_files = []
    for store_name in os.listdir('data'):
        if store_name.endswith('.pkl'):
            os.remove(f"data/{store_name}")
            deleted_files.append(store_name)
    return {"message": f"Vector databases deleted: {', '.join(deleted_files)}"}