# PrivateBin API
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/b0b11fa99727453eb219bcd0b03f5868)](https://www.codacy.com/gh/Pioverpie/privatebin-api/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Pioverpie/privatebin-api&amp;utm_campaign=Badge_Grade)
[![codecov](https://codecov.io/gh/Pioverpie/privatebin-api/branch/master/graph/badge.svg?token=5YE0802BC1)](undefined)
[![Build Status](https://travis-ci.org/Pioverpie/privatebin-api.svg?branch=master)](https://travis-ci.org/Pioverpie/privatebin-api)
[![Maintainability](https://api.codeclimate.com/v1/badges/b6dcd84fe476440a1811/maintainability)](https://codeclimate.com/github/Pioverpie/privatebin-api/maintainability)
![Code Climate issues](https://img.shields.io/codeclimate/issues/Pioverpie/privatebin-api)
![Code Climate technical debt](https://img.shields.io/codeclimate/tech-debt/Pioverpie/privatebin-api)
![GitHub repo size](https://img.shields.io/github/repo-size/Pioverpie/privatebin-api)

PrivateBin API is a wrapper for API interactions with PrivateBin hosts. It allows you to send, get, and delete pastes
from PrivateBin hosts.

## Installing PrivateBin API and Supported Versions

PrivateBin API is available on PyPI: (not quite yet)

```console
$ python -m pip install privatebinapi
```

PrivateBin API officially supports Python 3.6+.

## Supported Features 

  - Full support for both synchronous and asynchronous code
  - Fill out rest later
 
## Examples

### Basic usage

PrivateBin API is designed to be as easy to use as possible. A quick example of the most basic features is shown below:
```python
>>> import privatebinapi
>>> paste_url, delete_token = privatebinapi.send("https://vim.cx", text="Hello, world!")
>>> paste_text = privatebinapi.get(paste_url)
>>> paste_text == "Hello, world!"
True
>>> paste_id = privatebinapi.delete(paste_url, delete_token)
```
All parameters shown in the docs below are optional and may be combined in any way.

### Sending a Paste

To send a paste containing nothing but text, do the following:
```python
>>> import privatebinapi
>>> paste_url, delete_token = privatebinapi.send("https://vim.cx", text="Hello, world!")
```

#### Setting an Expiration

There are a limited number of valid expiration times. You must select one of the following:
```python
("5min", "10min", "1hour", "1day", "1week", "1month", "1year", "never")
```
The default is `"1day"`.
```python
>>> import privatebinapi
>>> paste_url, delete_token = privatebinapi.send(
...     "https://vim.cx",
...     text="Hello, world!",
...     expiration="5min"
... )
```
 
#### Setting a password

Putting a password on your paste is easy:
```python
>>> import privatebinapi
>>> paste_url, delete_token = privatebinapi.send(
...     "https://vim.cx",
...     text="Hello, world!",
...     password="Secure123!"
... )
```

#### Choosing Compression

There are only two valid options for this parameter: `"zlib"` and `None`. The default is `"zlib"`.
```python
>>> import privatebinapi
>>> paste_url, delete_token = privatebinapi.send(
...     "https://vim.cx",
...     text="Hello, world!",
...     compression=None
... )
```

#### Choosing a Format

There are only three valid options for this parameter: `"plaintext"`, `"syntaxhighlighting"`, and `"markdown"`. The default is `"plaintext"`.
```python
>>> import privatebinapi
>>> paste_url, delete_token = privatebinapi.send(
...     "https://vim.cx",
...     text="Hello, world!",
...     formatting="markdown"
... )
```

#### Burn After Reading

If you want a paste to be deleted immediately after being read, pass `True` to the `burn_after_reading` parameter. The default is `False`.
```python
>>> import privatebinapi
>>> paste_url, delete_token = privatebinapi.send(
...     "https://vim.cx",
...     text="Hello, world!",
...     burn_after_reading=True
... )
```

#### Enable Discussion

To enable discussion, pass `True` to the `discussion` parameter. The default is `False`.
```python
>>> import privatebinapi
>>> paste_url, delete_token = privatebinapi.send(
...     "https://vim.cx",
...     text="Hello, world!",
...     discussion=True
... )
```

### Getting a Paste

Getting a paste from a PrivateBin host is very easy:
```python
>>> import privatebinapi
>>> paste_text = privatebinapi.get("https://example.com/?fakePasteLink#1234567890")
```

#### Getting a Password Protected Paste

If the paste is password protected, use the `password` parameter.
```python
>>> import privatebinapi
>>> paste_text = privatebinapi.get(
...     "https://example.com/?fakePasteLink#1234567890",
...     password="Secure123!"
... )
```

### Deleting a Paste

To delete a paste, you need its URL and delete token.
```python
>>> import privatebinapi
>>> paste_id = privatebinapi.delete(
...     "https://example.com/?fakePasteLink#1234567890",
...     "fake1delete2token3"
... )
```

### Using a Proxy

All functions have an optional keyword parameter, `proxies`, that accepts a dictionary of proxies like you would see in
the Requests package.
```python
>>> import privatebinapi
>>> paste_url, delete_token = privatebinapi.send(
...     "https://vim.cx",
...     text="Hello, world!",
...     proxies={
...         "http": "http://example.com/proxy:80",
...         "https": "https://example.com/proxy:8080"
...     }
... )
```

### Using Async Functions
`privatebinapi.send`, `privatebinapi.get` and `privatebinapi.delete` all have async analogs. They accept all the same
parameters that their synchronous counterparts do.
```python
import asyncio

import privatebinapi

async def main():
    paste_url, delete_token = await privatebinapi.send_async("https://vim.cx", text="Hello, world!")
    paste_text = await privatebinapi.get_async(paste_url)
    paste_id = await privatebinapi.delete_async(paste_url, delete_token)
    
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```
Both `privatebinapi.send` and `privatebinapi.get` do encryption and decryption using an executor. By default it will
use the default executor for your loop, but you can pass a custom one by way of the `executor` parameter.
