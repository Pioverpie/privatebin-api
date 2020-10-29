import asyncio
import json

import pytest

import privatebinapi
from privatebinapi import common, deletion, download, upload
from tests import MESSAGE, RESPONSE_DATA, SERVER


def test_full():
    url, delete_token = privatebinapi.send(
        SERVER, text=MESSAGE, file='tests/__init__.py', password='foobar', compression=None,
    )
    text = privatebinapi.get(url, password='foobar')
    assert text == MESSAGE
    data = privatebinapi.delete(url, delete_token)
    assert data['status'] == 0


def test_bad_compression():
    try:
        privatebinapi.send(SERVER, text=MESSAGE, compression='clearly-fake-compression')
    except privatebinapi.BadCompressionTypeError:
        pass


def test_bad_expiration():
    try:
        privatebinapi.send(SERVER, text=MESSAGE, expiration='clearly-incorrect-expiration')
    except privatebinapi.BadExpirationTimeError:
        pass


def test_bad_formatting():
    try:
        privatebinapi.send(SERVER, text=MESSAGE, formatting='clearly-incorrect-format')
    except privatebinapi.BadFormatError:
        pass


def test_send_nothing():
    try:
        privatebinapi.send(SERVER)
    except ValueError:
        pass


@pytest.mark.asyncio
async def test_async_full():
    url, delete_token = await privatebinapi.send_async(SERVER, text=MESSAGE)
    text = await privatebinapi.get_async(url)
    assert text == MESSAGE
    data = await privatebinapi.delete_async(url, delete_token)
    assert data['status'] == 0
    await asyncio.sleep(0.1)


def test_bad_server():
    try:
        privatebinapi.send('https://example.com', text=MESSAGE)
    except privatebinapi.BadServerResponseError:
        pass


class FakeResponse:
    url = SERVER

    def __init__(self, error=False):
        self.error = error

    def json(self):
        if self.error:
            raise json.JSONDecodeError('', '', 0)
        else:
            return RESPONSE_DATA


def test_bad_response_verification():
    try:
        common.verify_response(FakeResponse(error=True))  # noqa
    except privatebinapi.BadServerResponseError:
        pass


def test_bad_process_result():
    try:
        upload.process_result(FakeResponse(), '')  # noqa
    except privatebinapi.PrivateBinAPIError:
        pass


def test_bad_process_url():
    try:
        deletion.process_url('https://example.com')
    except ValueError:
        pass


def test_bad_decrypt():
    try:
        download.decrypt_paste(RESPONSE_DATA, '', '')
    except privatebinapi.PrivateBinAPIError:
        pass


def test_bad_extract_passphrase():
    try:
        download.extract_passphrase('https://www.example.com')
    except ValueError:
        pass
