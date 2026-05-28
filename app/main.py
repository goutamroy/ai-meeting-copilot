from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

from app.config.settings import settings
from app.db.database import Base, engine
from app.db import models

from app.api.routes import (
    upload,
    chat,
    summary,
    health
)

from app.utils.logger import logger
from app.utils.exceptions import AppException

from app.middleware.request_logger import RequestLoggingMiddleware
from app.middleware.request_id import RequestIDMiddleware
from app.middleware.security_headers import SecurityHeadersMiddleware

# Validate settings
settings.validate()

app = FastAPI(
    title=settings.APP_NAME
)

# -----------------------------
# Allowed Hosts (AWS + Local)
# -----------------------------
allowed_hosts = [
    "*",
    "localhost",
    "127.0.0.1",
    "ai-meeting-copilot-env.eba-4m9cjwwy.eu-north-1.elasticbeanstalk.com",
    "*.elasticbeanstalk.com"
]

# -----------------------------
# Security Middleware
# -----------------------------
# Keep disabled for now (previous Invalid Host issue)
# Can enable later once stable
# app.add_middleware(
#     TrustedHostMiddleware,
#     allowed_hosts=allowed_hosts
# )

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.add_middleware(
    SecurityHeadersMiddleware
)

# -----------------------------
# Request Middleware
# -----------------------------
app.add_middleware(
    RequestIDMiddleware
)

app.add_middleware(
    RequestLoggingMiddleware
)

# -----------------------------
# App Lifecycle
# -----------------------------
@app.get("/")
def root():
    return {
        "message": "AI Meeting Copilot Backend is running successfully"
    }

@app.on_event("startup")
async def startup_event():
    """
    Initialize database tables on startup.
    This fixes AWS SQLite 'no such table: meetings' issue.
    """
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)

        logger.info(
            "Database tables initialized successfully"
        )

        logger.info(
            "AI Meeting Copilot API starting..."
        )

    except Exception as e:
        logger.exception(
            f"Database startup failed: {str(e)}"
        )
        raise


@app.on_event("shutdown")
async def shutdown_event():
    logger.info(
        "AI Meeting Copilot API shutting down..."
    )


# -----------------------------
# Exception Handlers
# -----------------------------
@app.exception_handler(AppException)
async def app_exception_handler(
    request: Request,
    exc: AppException
):
    logger.error(
        f"AppException: {exc.message}"
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.message
        }
    )


@app.exception_handler(Exception)
async def global_exception_handler(
    request: Request,
    exc: Exception
):
    logger.exception(
        f"Unhandled Error: {str(exc)}"
    )

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Internal server error"
        }
    )


# -----------------------------
# Routes
# -----------------------------
app.include_router(upload.router)
app.include_router(chat.router)
app.include_router(summary.router)
app.include_router(health.router)

logger.info(
    "Routes loaded successfully"
)