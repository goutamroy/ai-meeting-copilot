import uuid
import os
import tempfile

from fastapi import UploadFile

from app.services.whisper_service import transcribe_audio
from app.services.summary_service import generate_summary
from app.services.embedding_service import generate_embedding
from app.services.pinecone_service import store_embedding
from app.services.blob_service import upload_file
from app.utils.logger import logger
from app.utils.exceptions import ProcessingException


async def process_meeting(file: UploadFile):
    temp_file_path = None

    try:
        meeting_id = str(uuid.uuid4())

        suffix = os.path.splitext(
            file.filename
        )[1] or ".wav"

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix
        ) as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name

        # Step 1: Upload to Azure Blob
        with open(temp_file_path, "rb") as audio_file:
            blob_url = upload_file(
                audio_file,
                file.filename
            )

        # Step 2: Whisper transcription
        transcript = transcribe_audio(
            temp_file_path
        )

        if not transcript.strip():
            raise Exception(
                "Transcript is empty"
            )

        # Step 3: Summary
        summary_response = generate_summary(
            transcript
        )

        summary = summary_response.get(
            "summary", ""
        )

        action_items = summary_response.get(
            "action_items", ""
        )

        key_decisions = summary_response.get(
            "key_decisions", ""
        )

        # Step 4: Embedding
        embedding = generate_embedding(
            transcript
        )

        # Step 5: Pinecone
        store_embedding(
            meeting_id,
            embedding,
            transcript
        )

        return {
            "meeting_id": meeting_id,
            "blob_url": blob_url,
            "transcript": transcript,
            "summary": summary,
            "action_items": action_items,
            "key_decisions": key_decisions,
            "status": "success"
        }

    except Exception as e:
        logger.error(
            f"Meeting pipeline failed: {str(e)}"
        )
        raise ProcessingException(
            "Meeting processing failed"
        )

    finally:
        if (
            temp_file_path
            and os.path.exists(temp_file_path)
        ):
            os.remove(temp_file_path)