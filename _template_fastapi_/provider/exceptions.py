"""
Custom Exceptions
"""


class UpstreamProviderError(Exception):
    """
    Exception raised when the upstream provider encounters an error.
    """

    def __init__(self, message) -> None:
        self.message = message

    def __str__(self) -> str:
        return self.message
