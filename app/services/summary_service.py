import time
from openai import OpenAI

from app.config.settings import settings
from app.utils.logger import logger
from app.utils.exceptions import (
    ValidationException,
    ProcessingException
)

client = OpenAI(
    api_key=settings.OPENAI_API_KEY
)

MAX_RETRIES = 3
BACKOFF_SECONDS = 2


def generate_summary(
    transcript: str
):
    if not transcript.strip():
        raise ValidationException(
            "Transcript "
            "cannot be empty"
        )

    prompt = f"""
Analyze the following meeting transcript.

Return in exact format:

SUMMARY:
<summary>

KEY_DECISIONS:
<key decisions>

ACTION_ITEMS:
<action items>

Transcript:
{transcript}
"""

    for attempt in range(
        1,
        MAX_RETRIES + 1
    ):
        try:
            logger.info(
                f"Summary generation "
                f"attempt {attempt}"
            )

            response = (
                client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {
                            "role": "system",
                            "content":
                                "You are an "
                                "enterprise "
                                "meeting assistant."
                        },
                        {
                            "role": "user",
                            "content":
                                prompt
                        }
                    ],
                    temperature=0.3,
                    timeout=60
                )
            )

            output = (
                response
                .choices[0]
                .message
                .content
            )

            summary = ""
            key_decisions = ""
            action_items = ""

            if "SUMMARY:" in output:
                part = output.split(
                    "SUMMARY:"
                )[1]

                if (
                    "KEY_DECISIONS:"
                    in part
                ):
                    summary = (
                        part.split(
                            "KEY_DECISIONS:"
                        )[0]
                        .strip()
                    )

            if (
                "KEY_DECISIONS:"
                in output
            ):
                part = output.split(
                    "KEY_DECISIONS:"
                )[1]

                if (
                    "ACTION_ITEMS:"
                    in part
                ):
                    key_decisions = (
                        part.split(
                            "ACTION_ITEMS:"
                        )[0]
                        .strip()
                    )

            if (
                "ACTION_ITEMS:"
                in output
            ):
                action_items = (
                    output.split(
                        "ACTION_ITEMS:"
                    )[1]
                    .strip()
                )

            logger.info(
                "Summary generation "
                "successful"
            )

            return {
                "summary":
                    summary,
                "key_decisions":
                    key_decisions,
                "action_items":
                    action_items
            }

        except Exception as e:
            logger.warning(
                f"Summary retry "
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
                "Summary failed "
                "after retries"
            )

            raise ProcessingException(
                "Summary generation failed"
            )