from fastapi import UploadFile
from app.config.settings import settings
from app.utils.exceptions import ValidationException


async def validate_audio_file(
    file: UploadFile
):
    # -------------------------
    # File name
    # -------------------------
    if not file.filename:
        raise ValidationException(
            "Missing file name"
        )

    # -------------------------
    # Extension validation
    # -------------------------
    extension = (
        "." + file.filename.split(".")[-1].lower()
    )

    if (
        extension
        not in settings.ALLOWED_EXTENSIONS
    ):
        raise ValidationException(
            "Invalid file type. Allowed: "
            ".m4a, .wav, .mp3"
        )

    # -------------------------
    # MIME type validation
    # -------------------------
    if (
        file.content_type
        not in settings.ALLOWED_MIME_TYPES
    ):
        raise ValidationException(
            "Unsupported MIME type. "
            "Allowed: audio/m4a, "
            "audio/wav, audio/mp3"
        )

    # -------------------------
    # Size validation
    # -------------------------
    contents = await file.read()

    if len(contents) > settings.MAX_UPLOAD_SIZE:
        raise ValidationException(
            "File too large. "
            "Max allowed size is 25MB."
        )

    await file.seek(0)

    return True