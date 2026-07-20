from fastapi import FastAPI, APIRouter, Depends, UploadFile, status
from fastapi.responses import JSONResponse
from helpers.config import get_settings, Settings
import os
from controllers import DataController,ProjectController, ProcessController
import logging
import aiofiles

from models.enums.ResponseEnum import ResponseSignal

from .schemes.data import ProcessRequest
logger = logging.getLogger("uvicorn.error")


data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["Base", "Data"]
)



@data_router.post('/upload/{project_id}')
async def upload_data(project_id: str,file: UploadFile,
                       app_settings: Settings = Depends(get_settings)):
    
    data_controller = DataController()
    is_valid, result_signal = data_controller.validate_upload_file(file)
    
    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": result_signal}
        )
    
    project_dir_path = ProjectController().get_project_path(project_id)

    # file_path = os.path.join(project_dir_path, file.filename)
    file_path, file_id = data_controller.generate_unique_filename(file.filename, project_id)



    try:
        async with aiofiles.open(file_path, 'wb') as out_file:
            while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
                await out_file.write(chunk)

    except Exception as e:
        
        logger.error(f"Error File upload failed: {e}")

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "message": ResponseSignal.FILE_UPLOAD_FAILED.value
                }
        )


    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": ResponseSignal.FILE_UPLOAD_SUCCESS.value,
            "file_id": file_id,
            }
    )
    
    
@data_router.post('/process/{project_id}')
async def process_endpoint(project_id: str, process_request: ProcessRequest):
    
    file_id = process_request.file_id
    chunk_size = process_request.chunk_size
    overlap_size = process_request.overlap_size

    process_controller = ProcessController(project_id=project_id)
    
    file_content = process_controller.get_file_content(file_id)
    
    file_chunks = process_controller.process_file_content(file_id, file_content, chunk_size, overlap_size)

    if file_chunks is None or len(file_chunks) == 0:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "message": ResponseSignal.PROCESSING_FAILED.value
                }
        )
        
    return file_chunks