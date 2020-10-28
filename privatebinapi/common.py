# -*- coding: utf-8 -*-

"""This module provides functions and constants used in other modules in this package."""

import json
from typing import Union

import httpx
import requests

from privatebinapi.exceptions import BadServerResponseError

__all__ = ('verify_response', 'DEFAULT_HEADERS')

DEFAULT_HEADERS = {'X-Requested-With': 'JSONHttpRequest'}


def verify_response(response: Union[requests.Response, httpx.Response]) -> dict:
    """Checks a response to see it it contains JSON.

    :param response: An HTTP response from a PrivateBin host.
    :return: The JSON data included in the response.
    """
    try:
        data = response.json()
    except json.JSONDecodeError as error:
        raise BadServerResponseError('Unable to parse response from %s' % response.url) from error
    return data
