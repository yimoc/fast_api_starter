import logging
import zipfile
import os
from dataclasses import dataclass

import aiofiles
from fastapi import UploadFile, File
from pydantic import BaseModel

logger = logging.getLogger(__name__)

def get_file_name(dest_path, filename):
    file_path = os.path.join(dest_path, filename)
    if os.path.isfile(file_path):
        file_name_ext = filename.split('.', 1)
        filename = file_name_ext[0] + "_1." + file_name_ext[1]
        return get_file_name(dest_path, filename)
    else:
        return filename


async def upload_file(dest_path, file: UploadFile = File(...)):
    UPLOAD_CHUNK_SIZE = 1024 * 1024  # adjust the chunk size as desired
    try:
        # 일반 pdf 파일
        if file.filename.split('.')[-1] == 'pdf':
            logger.debug(f'file={file.filename} , {file.size}')
            os.makedirs(dest_path, exist_ok=True)
            filename = get_file_name(dest_path, os.path.basename(file.filename))
            file_path = os.path.join(dest_path, filename)
            async with aiofiles.open(file_path, 'wb') as f:
                while chunk := await file.read(UPLOAD_CHUNK_SIZE):
                    await f.write(chunk)

            result = UploadFileResult(filename=filename, size=file.size, file_path= file_path)
        # zip 파일
        else:

            result = []

            logger.debug(f'file={file.filename} , {file.size}')
            os.makedirs(dest_path, exist_ok=True)
            filename = get_file_name(dest_path, os.path.basename(file.filename))
            file_path = os.path.join(dest_path, filename)

            async with aiofiles.open(file_path, 'wb') as zip_file:
                # zip파일을 먼저 업로드
                while chunk := await file.read(UPLOAD_CHUNK_SIZE):
                    await zip_file.write(chunk)

                # 업로드 후 zip파일의 내용을 읽어서 .pdf파일만 추가 업로드
                with zipfile.ZipFile(file_path, 'r') as zip_ref:

                    file_list = zip_ref.infolist()
                    pdf_files = [file for file in file_list if file.filename.split('.')[-1] == 'pdf']

                    for pdf_file in pdf_files:

                        # zip_ref에는 decode 되기 전의 이름으로 적재되어있다.
                        decoded_pdf_file = pdf_file.filename.encode('cp437').decode('euc-kr')

                        extracted_file_path = os.path.join(dest_path, decoded_pdf_file)

                        # zipfile은 async를 지원하지 않는다.
                        with open(extracted_file_path, 'wb') as extracted_file:
                            with zip_ref.open(pdf_file.filename) as source_file:
                                while chunk := source_file.read(UPLOAD_CHUNK_SIZE):
                                    extracted_file.write(chunk)

                        result.append(
                            UploadFileResult(filename=decoded_pdf_file, size=source_file._orig_file_size, file_path= extracted_file_path)
                        )

            # zip 파일 안에 있는 모든 pdf 파일을 업로드하면, zip파일은 삭제한다.
            os.remove(file_path)
        
    finally:
        await file.close()
    return  result

class UploadFileResult(BaseModel):
    filename: str
    size: int
    file_path: str
