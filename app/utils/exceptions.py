class AppException(Exception):
    def __init__(
        self,
        message: str,
        status_code: int = 500
    ):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


# -----------------------------
# 400 - Validation
# -----------------------------
class ValidationException(AppException):
    def __init__(self, message: str):
        super().__init__(
            message=message,
            status_code=400
        )


# -----------------------------
# 404 - Not Found
# -----------------------------
class NotFoundException(AppException):
    def __init__(self, message: str):
        super().__init__(
            message=message,
            status_code=404
        )


# -----------------------------
# 500 - Processing / Service
# -----------------------------
class ProcessingException(AppException):
    def __init__(self, message: str):
        super().__init__(
            message=message,
            status_code=500
        )


# -----------------------------
# 503 - Database
# -----------------------------
class DatabaseException(AppException):
    def __init__(self, message: str):
        super().__init__(
            message=message,
            status_code=503
        )