import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    APP_NAME = "AI Meeting Copilot API"

    OPENAI_API_KEY = os.getenv(
        "OPENAI_API_KEY"
    )

    AZURE_STORAGE_CONNECTION_STRING = os.getenv(
        "AZURE_STORAGE_CONNECTION_STRING"
    )

    AZURE_CONTAINER_NAME = os.getenv(
        "AZURE_CONTAINER_NAME",
        "meeting-files"
    )

    PINECONE_API_KEY = os.getenv(
        "PINECONE_API_KEY"
    )

    PINECONE_INDEX_NAME = os.getenv(
        "PINECONE_INDEX_NAME",
        "meeting-index"
    )

    DATABASE_URL = os.getenv(
        "DATABASE_URL"
    )

    MAX_UPLOAD_SIZE = int(
        os.getenv(
            "MAX_UPLOAD_SIZE",
            10485760
        )
    )  # 10MB

    ALLOWED_MIME_TYPES = [
        "audio/m4a",
        "audio/wav",
        "audio/mp3",
        "audio/x-m4a",
        "audio/mpeg"
    ]

    ALLOWED_HOSTS = [
        "localhost",
        "127.0.0.1",
        "*.azurewebsites.net",
        "*.amazonaws.com"
    ]

    ALLOWED_ORIGINS = [
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ]

    def validate(self):
        required = {
            "OPENAI_API_KEY":
                self.OPENAI_API_KEY,
            "AZURE_STORAGE_CONNECTION_STRING":
                self.AZURE_STORAGE_CONNECTION_STRING,
            "PINECONE_API_KEY":
                self.PINECONE_API_KEY,
            "DATABASE_URL":
                self.DATABASE_URL
        }

        missing = [
            key for key, value
            in required.items()
            if not value
        ]

        if missing:
            raise ValueError(
                "Missing env vars: "
                + ", ".join(missing)
            )


settings = Settings()