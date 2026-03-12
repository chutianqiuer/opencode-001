import os
import uuid
from datetime import datetime
from typing import Optional
from fastapi import UploadFile
from app.config import settings


class FileStorage:
    def __init__(self, upload_dir: str = settings.UPLOAD_DIR):
        self.upload_dir = upload_dir
        os.makedirs(upload_dir, exist_ok=True)

    def _get_file_extension(self, filename: str) -> str:
        return filename.rsplit(".", 1)[-1].lower() if "." in filename else ""

    def _generate_filename(self, original_filename: str) -> str:
        ext = self._get_file_extension(original_filename)
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        unique_id = uuid.uuid4().hex[:8]
        return f"{timestamp}_{unique_id}.{ext}" if ext else f"{timestamp}_{unique_id}"

    def _get_date_path(self) -> str:
        return datetime.now().strftime("%Y/%m/%d")

    async def save(self, file: UploadFile, sub_dir: str = "") -> str:
        date_path = self._get_date_path()
        save_dir = os.path.join(self.upload_dir, sub_dir, date_path)
        os.makedirs(save_dir, exist_ok=True)
        filename = self._generate_filename(file.filename or "unknown")
        file_path = os.path.join(save_dir, filename)
        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)
        relative_path = os.path.join(sub_dir, date_path, filename)
        return relative_path.replace("\\", "/")

    def delete(self, file_path: str) -> bool:
        full_path = os.path.join(self.upload_dir, file_path)
        if os.path.exists(full_path):
            os.remove(full_path)
            return True
        return False

    def get_url(self, file_path: str) -> str:
        return f"/uploads/{file_path}"

    def validate_image(self, file: UploadFile) -> bool:
        allowed_types = ["image/jpeg", "image/png", "image/gif"]
        if file.content_type not in allowed_types:
            return False
        return True


file_storage = FileStorage()
