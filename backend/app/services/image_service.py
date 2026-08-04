from fastapi import UploadFile

from app.core.config import ALLOWED_IMAGE_TYPES, MAX_IMAGE_SIZE, UPLOAD_DIR



async def save_image(image: UploadFile | None) -> tuple[str | None, str | None]:
    if image is None or not image.filename:
        return None, None

    content = await image.read()
   
    filename = image.filename.replace("\\", "/").split("/")[-1]
    path = UPLOAD_DIR / filename

    path.write_bytes(content)
    return f"/uploads/{filename}", filename


def delete_image(filename: str | None) -> None:
    if filename:
        path = UPLOAD_DIR / filename
        path.unlink(missing_ok=True)
