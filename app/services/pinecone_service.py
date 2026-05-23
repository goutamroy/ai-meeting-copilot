from pinecone import Pinecone
import os
from dotenv import load_dotenv
from app.config.settings import settings

load_dotenv()

pc = Pinecone(
    api_key=settings.PINECONE_API_KEY
)

index = pc.Index(
    settings.PINECONE_INDEX_NAME
)


def store_embedding(meeting_id, embedding, transcript):
    try:
        index.upsert(
            vectors=[
                {
                    "id": meeting_id,
                    "values": embedding,
                    "metadata": {
                        "transcript": transcript
                    }
                }
            ]
        )

        print("Embedding stored successfully in Pinecone")

    except Exception as e:
        print(f"Pinecone Store Error: {e}")


def search_embedding(query_embedding):
    try:
        results = index.query(
            vector=query_embedding,
            top_k=3,
            include_metadata=True
        )

        return results.matches

    except Exception as e:
        print(f"Pinecone Search Error: {e}")
        return []