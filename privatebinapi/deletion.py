# -*- coding: utf-8 -*-

"""Provides functions to delete pastes from PrivateBin instances."""

import json
from typing import Tuple

import httpx
import requests

from privatebinapi.common import DEFAULT_HEADERS, verify_response
from privatebinapi.exceptions import PrivateBinAPIError, UnsupportedFeatureError

__all__ = ('delete', 'delete_async')


def process_url(url: str) -> Tuple[str, str]:
    """Extracts both the web address of the PrivateBin instance and the Paste ID from a URL.

    :param url: The full URL of a paste, including passphrase.
    :return: A tuple containing the server URL and the Paste ID.
    """
    if '?' not in url or '#' not in url:
        raise ValueError("url must be a full, valid PrivateBin link")
    paste_id = url[url.find('?') + 1:url.find('#')]
    server = url[:url.find('?')]

    return server, paste_id


def delete(url: str, token: str, *, proxies: dict = None):
    """Delete a paste from PrivateBin.

    :param url: The full URL of a paste, including passphrase.
    :param token: The delete token associated with a paste.
    :param proxies: A dict of proxies to pass to a requests.Session object.
    :return:The JSON component of a response from the a PrivateBin server.
    """
    server, paste_id = process_url(url)

    with requests.Session() as session:
        response = session.post(
            server,
            headers=DEFAULT_HEADERS,
            proxies=proxies,
            data=json.dumps({'pasteid': paste_id, 'deletetoken': token})
        )

    try:
        return verify_response(response)
    except PrivateBinAPIError as error:
        if error.args[0].startswith('Unable to parse response from '):
            raise UnsupportedFeatureError('%s does not support manually deleting pastes' % server) from error


async def delete_async(url: str, token: str, *, proxies: dict = None):
    """Asynchronously delete a paste from PrivateBin.

    :param url: The full URL of a paste, including passphrase.
    :param token: The delete token associated with a paste.
    :param proxies: A dict of proxies to pass to an httpx.AsyncClient object.
    :return: The JSON component of a response from the a PrivateBin server.
    """
    server, paste_id = process_url(url)

    async with httpx.AsyncClient(proxies=proxies, headers=DEFAULT_HEADERS) as client:
        response = await client.post(
            server,
            data=json.dumps({'pasteid': paste_id, 'deletetoken': token})
        )

    try:
        return verify_response(response)
    except PrivateBinAPIError as error:
        if error.args[0].startswith('Unable to parse response from '):
            raise UnsupportedFeatureError('%s does not support manually deleting pastes' % server) from error
