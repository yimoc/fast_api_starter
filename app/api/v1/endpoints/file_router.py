import logging
import os

from fastapi import APIRouter, Request
from fastapi import File, UploadFile, Form, HTTPException, status
import aiofiles
from fastapi.responses import FileResponse

from app.core.exception.exceptions import SodaflowResponseError
# from starlette.requests import Request

from app.core.web.response_base import Result, Meta, SodaflowResponseBase

logger = logging.getLogger(__name__)
router = APIRouter()



@router.post("/upload")
async def upload(request : Request, file: UploadFile = File(...), data: str = Form(...)):
    UPLOAD_CHUNK_SIZE = 1024 * 1024  # adjust the chunk size as desired
    try:
        logger.debug(f'data = {data}, file={file.filename} , {file.size}')
        file_repository_path = os.path.join(request.app.state.APP_DIR, request.app.state.config['COMMON']['FILE_DIR'])
        os.makedirs(file_repository_path, exist_ok=True)
        file_path = os.path.join(file_repository_path, os.path.basename(file.filename))
        async with aiofiles.open(file_path, 'wb') as f:
            while chunk := await file.read(UPLOAD_CHUNK_SIZE):
                await f.write(chunk)
    except Exception:
        logging.exception("upload error")
        raise SodaflowResponseError(code="FILEUPLOADFAIL",
                                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    message='There was an error uploading the file')
    finally:
        await file.close()

    data = dict(filename=file.filename, size=file.size)
    result = Result()
    meta = Meta(version='v1')
    response_data = SodaflowResponseBase[dict](data=data, result=result, meta=meta)

    return response_data

@router.get("/download/{file_name}")
async def download(request : Request, file_name: str):
    file_repository_path = os.path.join(request.app.state.APP_DIR, request.app.state.config['COMMON']['FILE_DIR'])
    os.makedirs(file_repository_path, exist_ok=True)
    file_path = os.path.join(file_repository_path, file_name)
    return FileResponse(file_path) #, media_type='image/jpeg', filename=image_name)
