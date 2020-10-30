# -*- coding: utf-8 -*-

"""Contains privatebinapi's exceptions."""


class PrivateBinAPIError(Exception):
    """An ambiguous error has occurred while handling your request."""


class BadCompressionTypeError(PrivateBinAPIError):
    """Indicates that an invalid compression type has been passed as an argument."""


class BadExpirationTimeError(PrivateBinAPIError):
    """Indicates that an invalid expiration time has been passed as an argument."""


class BadFormatError(PrivateBinAPIError):
    """Indicates than an invalid format name has been passes as an argument."""


class BadServerResponseError(PrivateBinAPIError):
    """Indicates that the server sent a response that could not be decoded.

    This could mean that the url that was passed as an argument is not a valid PrivateBin host, or that it simply
    sent an empty response.
    """


class UnsupportedFeatureError(PrivateBinAPIError):
    """Indicates that a PrivateBin host does not support the operation attempted"""
