# -*- coding: utf-8 -*-

"""Provides functions to download pastes from PrivateBin hosts."""

import functools
from concurrent.futures import Executor

import httpx
import requests
from pbincli.format import Paste

from privatebinapi.common import DEFAULT_HEADERS, get_loop, verify_response

__all__ = ('get', 'get_async')


def decrypt_paste(data: dict, passphrase: str, password: str = None) -> dict:
    """Decrypt a paste.

    :param data: The JSON component of a response from a PrivateBin host.
    :param passphrase: The part of the URL trailing the '#'.
    :param password: Password for decrypting the paste.
    :return: The decrypted text content of the paste.
    """
    paste = Paste()
    if password:
        paste.setPassword(password)
    paste.setVersion(data['v'] if 'v' in data else 1)
    paste.setHash(passphrase)
    paste.loadJSON(data)

    paste.decrypt()

    attachment_bytes, attachment_name = paste.getAttachment()

    output = {
        'attachment': {
            'content': attachment_bytes or None,
            'filename': attachment_name or None
        },
        'id': data['id'],
        'meta': data['meta'],
        'status': data['status'],
        'text': paste.getText().decode('utf-8'),
        'url': data['url'],
        'v': data.get('v', 1)
    }

    return output


def extract_passphrase(url: str) -> str:
    """Extract the passphrase from a PrivateBin URL.

    :param url: The full URL of a paste, including passphrase.
    :return: The passphrase.
    :raises ValueError: The URL does not contain a passphrase.
    """
    split_link = url.rsplit('#', 1)
    if len(split_link) != 2:
        raise ValueError("Make sure you are entering a full, valid PrivateBin URL")
    passphrase = split_link[-1]
    return passphrase


def get(url: str, *, proxies: dict = None, password: str = None) -> dict:
    """Download a paste from a PrivateBin host.

    :param url: The full URL of a paste, including passphrase.
    :param proxies: A dict of proxies to pass to a requests.Session object.
    :param password: Password for decrypting the paste.
    :return: The decrypted text content of the paste.
    """
    with requests.Session() as session:
        response = session.get(
            url,
            headers=DEFAULT_HEADERS,
            proxies=proxies
        )
    return decrypt_paste(verify_response(response), extract_passphrase(url), password=password)


async def get_async(url: str, *, proxies: dict = None, password: str = None, executor: Executor = None, ):
    """Asynchronously download a paste from a PrivateBin host.

    :param url: The full URL of a paste, including passphrase.
    :param proxies: A dict of proxies to pass to an httpx.AsyncClient object.
    :param password: Password for decrypting the paste.
    :param executor: A concurrent.futures.Executor instance used for decryption.
    :return: The decrypted text content of the paste.
    """
    async with httpx.AsyncClient(proxies=proxies, headers=DEFAULT_HEADERS) as client:
        response = await client.get(url)
    func = functools.partial(decrypt_paste, verify_response(response), extract_passphrase(url), password=password)
    result = await get_loop().run_in_executor(executor, func)
    return result
