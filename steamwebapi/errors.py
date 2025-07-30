"""
Copyright 2025-present fretgfr

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from __future__ import annotations

from typing import Any

__all__ = (
    "SteamWebAPIError",
    "HTTPError",
    "UnhandledError",
    "BadRequest",
    "Forbidden",
    "NotFound",
    "RateLimited",
    "ServerError",
    "NotAuthenticated",
)


class SteamWebAPIError(Exception):
    """Base class for SteamWebAPI related errors."""

    pass


class HTTPError(SteamWebAPIError):
    """Base class for HTTP related exceptions.

    Attributes
    ----------
    error: Any
        The error given.
    code: :class:`int`
        The HTTP status code of the error.
    message: Any
        A descriptive message returned by the api for what caused the error.
    """

    def __init__(self, error: Any, code: int, message: Any):
        super().__init__(f"{code}: {message}")
        self.error = error
        self.code = code
        self.message = message


class UnhandledError(HTTPError):
    """Raised by the library if the server returns a status code not handled by the lib."""

    pass


class BadRequest(HTTPError):
    """Server returned a 400 response."""

    pass


class Forbidden(HTTPError):
    """Server returned a 401 or 403 response."""

    pass


class NotFound(HTTPError):
    """Server returned a 404 response."""

    pass


class RateLimited(SteamWebAPIError):
    """Server returned a 429 response. This does **not** subclass HTTPError."""

    pass


class ServerError(HTTPError):
    """Server returned a 5xx response code."""

    pass


class NotAuthenticated(HTTPError):
    """Requesting data without an Authorization header."""

    pass
