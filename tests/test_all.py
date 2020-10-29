import asyncio

import pytest

import privatebinapi
from privatebinapi import common
from tests import MESSAGE, SERVER


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
    @staticmethod
    def json():
        return ''


def test_bad_response():
    try:
        privatebinapi.common.verify_response(FakeResponse())  # noqa
    except privatebinapi.BadServerResponseError:
        pass
