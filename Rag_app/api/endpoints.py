from fastapi import APIRouter, UploadFile, File, HTTPException
from Rag_app.core.model import Query, Answer, RephraseRequest
from Rag_app.core.utils import process_pdf, handle_query, rephrase_text
import os
import logging

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

router = APIRouter()

@router.post("/upload_pdf")
async def upload_pdf(file: UploadFile = File(...)):
    file_path = f"data/{file.filename}"
    try:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())
        
        process_pdf(file_path)
        return {"message": "PDF processed successfully"}
    except Exception as e:
        logger.error(f"Error processing PDF file: {e}")
        raise HTTPException(status_code=500, detail="Error processing PDF file")

@router.post("/query", response_model=Answer)
async def query(query: Query, temperature: float = 1.0):
    try:
        answer = handle_query(query.text, temperature=temperature)
        return Answer(text=answer)
    except Exception as e:
        logger.error(f"Error handling query: {e}")
        raise HTTPException(status_code=500, detail="Error handling query")

@router.post("/rephrase", response_model=Answer)
async def rephrase(request: RephraseRequest, temperature: float = 1.0):
    try:
        rephrased_text = rephrase_text(request.text, request.format_option, temperature=temperature)
        return Answer(text=rephrased_text)
    except Exception as e:
        logger.error(f"Error rephrasing text: {e}")
        raise HTTPException(status_code=500, detail="Error rephrasing text")

@router.post("/delete_vector_databases")
async def delete_vector_databases():
    deleted_files = []
    try:
        data_dir = 'data'
        if not os.path.exists(data_dir):
            raise HTTPException(status_code=404, detail="Data directory not found")

        for store_name in os.listdir(data_dir):
            if store_name.endswith('.pkl'):
                os.remove(os.path.join(data_dir, store_name))
                deleted_files.append(store_name)
        
        if not deleted_files:
            return {"message": "No vector databases found to delete"}

        return {"message": f"Vector databases deleted: {', '.join(deleted_files)}"}
    except Exception as e:
        logger.error(f"Error deleting vector databases: {e}")
        raise HTTPException(status_code=500, detail="Error deleting vector databases")
