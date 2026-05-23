import time
from openai import OpenAI

from app.config.settings import settings
from app.utils.logger import logger
from app.utils.exceptions import (
    ProcessingException
)

client = OpenAI(
    api_key=settings.OPENAI_API_KEY
)

MAX_RETRIES = 3
BACKOFF_SECONDS = 2


def transcribe_audio(
    file_path: str
) -> str:
    """
    Whisper transcription with retry logic
    """

    for attempt in range(
        1,
        MAX_RETRIES + 1
    ):
        try:
            logger.info(
                f"Whisper transcription "
                f"attempt {attempt}"
            )

            with open(
                file_path,
                "rb"
            ) as audio_file:
                transcript = (
                    client.audio.transcriptions.create(
                        model="whisper-1",
                        file=audio_file,
                        timeout=60
                    )
                )

            text = (
                transcript.text.strip()
                if transcript
                and hasattr(
                    transcript,
                    "text"
                )
                and transcript.text
                else ""
            )

            if not text:
                logger.warning(
                    "No speech detected "
                    "in audio."
                )
                return (
                    "No speech "
                    "detected "
                    "in audio."
                )

            logger.info(
                "Whisper transcription "
                "successful"
            )

            return text

        except Exception as e:
            logger.warning(
                f"Whisper retry "
                f"{attempt} failed: "
                f"{str(e)}"
            )

            if attempt < MAX_RETRIES:
                sleep_time = (
                    BACKOFF_SECONDS
                    ** attempt
                )
                time.sleep(
                    sleep_time
                )
                continue

            logger.error(
                "Whisper failed "
                "after retries"
            )

            raise ProcessingException(
                "Whisper transcription failed"
            )