"""Exceptions related to roboquote."""


class CannotFetchBackgroundError(Exception):
    """Exception when roboquote cannot fetch a background image."""

    pass


class CannotGenerateQuoteError(Exception):
    """Exception when roboquote cannot generate the quote."""
