"""
Custom exceptions for the Healthsites API client.
"""


class HealthsitesError(Exception):
    """Base exception for all Healthsites API errors."""

    def __init__(self, message: str, status_code: int | None = None):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class AuthenticationError(HealthsitesError):
    """Raised when API authentication fails."""

    def __init__(self, message: str = "Invalid or missing API key"):
        super().__init__(message, status_code=401)


class NotFoundError(HealthsitesError):
    """Raised when a requested resource is not found."""

    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, status_code=404)


class RateLimitError(HealthsitesError):
    """Raised when API rate limit is exceeded."""

    def __init__(self, message: str = "Rate limit exceeded"):
        super().__init__(message, status_code=429)


class ValidationError(HealthsitesError):
    """Raised when request validation fails."""

    def __init__(self, message: str = "Validation error"):
        super().__init__(message, status_code=400)
