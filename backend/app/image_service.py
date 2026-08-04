from fastapi import UploadFile

from app.core.config import ALLOWED_IMAGE_TYPES, MAX_IMAGE_SIZE, UPLOAD_DIR
from app.exceptions import (
    image_already_exists,
    image_too_large,
    invalid_image_type,
)


async def save_image(image: UploadFile | None) -> tuple[str | None, str | None]:
    if image is None or not image.filename:
        return None, None

    if image.content_type not in ALLOWED_IMAGE_TYPES:
        raise invalid_image_type()

    content = await image.read()
    if len(content) > MAX_IMAGE_SIZE:
        raise image_too_large()

    filename = image.filename.replace("\\", "/").split("/")[-1]
    path = UPLOAD_DIR / filename

    if path.exists():
        raise image_already_exists()

    path.write_bytes(content)
    return f"/uploads/{filename}", filename


def delete_image(filename: str | None) -> None:
    if filename:
        path = UPLOAD_DIR / filename
        path.unlink(missing_ok=True)
