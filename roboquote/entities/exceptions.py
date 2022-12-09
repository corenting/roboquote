"""Exceptions related to roboquote."""


class CannotFetchBackgroundException(Exception):
    """Exception when roboquote cannot fetch a background image."""

    pass


class CannotGenerateQuoteException(Exception):
    """Exception when roboquote cannot generate the quote."""
