import time
from starlette.middleware.base import (
    BaseHTTPMiddleware
)
from fastapi import Request

from app.utils.logger import (
    log_with_request_id
)


class RequestLoggingMiddleware(
    BaseHTTPMiddleware
):
    async def dispatch(
        self,
        request: Request,
        call_next
    ):
        start_time = time.time()

        method = request.method
        path = request.url.path

        request_id = getattr(
            request.state,
            "request_id",
            "unknown"
        )

        log_with_request_id(
            request_id,
            "info",
            (
                f"Incoming Request | "
                f"{method} | {path}"
            )
        )

        try:
            response = await call_next(
                request
            )

            duration = round(
                time.time() - start_time,
                4
            )

            log_with_request_id(
                request_id,
                "info",
                (
                    f"Completed Request | "
                    f"{method} | "
                    f"{path} | "
                    f"{response.status_code} | "
                    f"{duration}s"
                )
            )

            return response

        except Exception as e:
            duration = round(
                time.time() - start_time,
                4
            )

            log_with_request_id(
                request_id,
                "error",
                (
                    f"Failed Request | "
                    f"{method} | "
                    f"{path} | "
                    f"500 | "
                    f"{duration}s | "
                    f"{str(e)}"
                )
            )

            raise