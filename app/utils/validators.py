from fastapi import UploadFile

from app.config.settings import settings
from app.utils.exceptions import ValidationException


# -----------------------------------
# AUDIO FILE VALIDATION
# -----------------------------------
async def validate_audio_file(
    file: UploadFile
):
    if not file:
        raise ValidationException(
            "No file uploaded"
        )

    # Validate MIME type
    if (
        file.content_type
        not in settings.ALLOWED_MIME_TYPES
    ):
        raise ValidationException(
            f"Unsupported file type: "
            f"{file.content_type}"
        )

    # Validate extension
    filename = (
        file.filename or ""
    ).lower()

    allowed_extensions = (
        ".m4a",
        ".wav",
        ".mp3"
    )

    if not filename.endswith(
        allowed_extensions
    ):
        raise ValidationException(
            "Only .m4a, .wav, "
            ".mp3 files allowed"
        )

    # Validate file size
    file.file.seek(
        0,
        2
    )
    file_size = (
        file.file.tell()
    )
    file.file.seek(0)

    if (
        file_size
        > settings.MAX_UPLOAD_SIZE
    ):
        raise ValidationException(
            "File size exceeds "
            "allowed limit"
        )

    return True