# -*- coding: utf-8 -*-

"""This module provides functions to download pastes from PrivateBin hosts."""

import asyncio
import functools
from concurrent.futures import Executor

import httpx
import requests
from pbincli.format import Paste

from privatebinapi.common import DEFAULT_HEADERS, verify_response
from privatebinapi.exceptions import PrivateBinAPIError

__all__ = ('get', 'get_async')


def decrypt_paste(data, passphrase: str, password: str = None) -> str:
    """Decrypt a paste.

    :param data: The JSON component of a response from a PrivateBin host.
    :param passphrase: The part of the URL trailing the '#'.
    :param password: Password for decrypting the paste.
    :return: The decrypted text content of the paste.
    """
    if data['status'] != 0:
        raise PrivateBinAPIError(data['message'])
    paste = Paste()
    if password:
        paste.setPassword(password)
    paste.setVersion(data['v'] if 'v' in data else 1)
    paste.setHash(passphrase)
    paste.loadJSON(data)

    paste.decrypt()
    return paste.getText().decode('utf-8')


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


def get(url: str, *, proxies: dict = None, password: str = None) -> str:
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
    return await asyncio.get_running_loop().run_in_executor(executor, func)
