import pytest
import privatebinapi


SERVER = 'https://vim.cx'
MESSAGE = 'This is a test.'


def test_send():
    privatebinapi.send(SERVER, text=MESSAGE)


@pytest.mark.asyncio
async def test_async_send():
    await privatebinapi.send_async(SERVER, text=MESSAGE)
