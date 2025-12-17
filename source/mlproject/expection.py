import sys
import logging
from typing import Any


def error_message_detail(error: Any, error_detail: sys) -> str:
    """Build a single-line error message with filename and line number.

    Args:
        error: The original exception instance or message.
        error_detail: The `sys` module (so callers pass `sys`).

    Returns:
        A formatted error message string.
    """
    _, _, exc_tb = error_detail.exc_info()
    if exc_tb is None:
        return str(error)

    file_name = exc_tb.tb_frame.f_code.co_filename
    line_no = exc_tb.tb_lineno
    error_message = f"Error occurred in script [{file_name}] at line [{line_no}]: {error}"
    return error_message


class CustomException(Exception):
    """Custom exception that stores a formatted error message with context."""

    def __init__(self, error_message: Any, error_detail: sys):
        # keep original message for base Exception
        super().__init__(error_message)
        # store a detailed message produced by helper
        self.error_message = error_message_detail(error_message, error_detail)

    def __str__(self) -> str:
        return self.error_message