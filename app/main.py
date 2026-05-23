from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from starlette.middleware.cors import (
    CORSMiddleware
)
from starlette.middleware.trustedhost import (
    TrustedHostMiddleware
)

from app.config.settings import settings
from app.api.routes import (
    upload,
    chat,
    summary,
    health
)

from app.utils.logger import logger
from app.utils.exceptions import AppException

from app.middleware.request_logger import (
    RequestLoggingMiddleware
)
from app.middleware.request_id import (
    RequestIDMiddleware
)
from app.middleware.security_headers import (
    SecurityHeadersMiddleware
)

settings.validate()

app = FastAPI(
    title=settings.APP_NAME
)

# -----------------------------
# Security Middleware
# -----------------------------
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.ALLOWED_HOSTS
)

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


@app.on_event("startup")
async def startup_event():
    logger.info(
        "AI Meeting Copilot API starting..."
    )


@app.on_event("shutdown")
async def shutdown_event():
    logger.info(
        "AI Meeting Copilot API shutting down..."
    )


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
            "message":
                "Internal server error"
        }
    )


app.include_router(upload.router)
app.include_router(chat.router)
app.include_router(summary.router)
app.include_router(health.router)

logger.info(
    "Routes loaded successfully"
)