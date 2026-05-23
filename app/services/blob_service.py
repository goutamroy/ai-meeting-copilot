import time
from azure.storage.blob import (
    BlobServiceClient
)

from app.config.settings import settings
from app.utils.logger import logger
from app.utils.exceptions import (
    ProcessingException
)

connection_string = (
    settings
    .AZURE_STORAGE_CONNECTION_STRING
)

container_name = (
    settings
    .AZURE_CONTAINER_NAME
)

blob_service_client = (
    BlobServiceClient
    .from_connection_string(
        connection_string
    )
)

MAX_RETRIES = 3
BACKOFF_SECONDS = 2


def upload_file(
    file_obj,
    filename
):
    for attempt in range(
        1,
        MAX_RETRIES + 1
    ):
        try:
            logger.info(
                f"Azure upload "
                f"attempt {attempt}"
            )

            blob_client = (
                blob_service_client
                .get_blob_client(
                    container=
                        container_name,
                    blob=filename
                )
            )

            blob_client.upload_blob(
                file_obj,
                overwrite=True,
                timeout=60
            )

            logger.info(
                "Azure upload "
                "successful"
            )

            return (
                blob_client.url
            )

        except Exception as e:
            logger.warning(
                f"Azure retry "
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
                "Azure upload "
                "failed after retries"
            )

            raise ProcessingException(
                "Azure Blob upload failed"
            )