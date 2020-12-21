==============
PrivateBin API
==============

|Codacy Badge| |codecov| |Build Status| |Maintainability| |Code Climate issues| |Code Climate technical debt|
|GitHub repo size| |License badge|

PrivateBin API is a wrapper for API interactions with PrivateBin instances.
It allows you to send, get, and delete pastes from PrivateBin instances.

Installing PrivateBin API and Supported Versions
------------------------------------------------

PrivateBin API is available on PyPI: (not quite yet)

.. code:: console

   $ python -m pip install privatebinapi

PrivateBin API officially supports Python 3.6+.

Features
--------

-  Send, retrieve, and delete pastes on any PrivateBin instance
-  Officially supports PrivateBin 1.0 through 1.3
-  Full support for both synchronous and asynchronous code
-  Upload and download files
-  Proxy support

Examples
--------

Basic usage
~~~~~~~~~~~

PrivateBin API is designed to be as easy to use as possible. A quick
example of the most basic features is shown below:

.. code:: python

   >>> import privatebinapi
   >>> send_response = privatebinapi.send("https://vim.cx", text="Hello, world!")
   >>> get_response = privatebinapi.get(send_response["full_url"])
   >>> get_response['text'] == "Hello, world!"
   True
   >>> delete_response = privatebinapi.delete(send_response["full_url"], send_response["deletetoken"])

Each function returns a modified version of the JSON received from the PrivateBin instance.

All parameters shown in the docs below are optional and may be combined
in any way.

Sending a Paste
~~~~~~~~~~~~~~~

To send a paste containing nothing but text, do the following:

.. code:: python

   >>> import privatebinapi
   >>> response = privatebinapi.send("https://vim.cx", text="Hello, world!")

You can expect the send function to return something similar to the following:

.. code:: text

   {
       "deletetoken": "< paste delete token >",
       "full_url": "< direct link to paste> ",
       "id": "< paste ID >",
       "passcode": "< paste passcode >",
       "status": 0,
       "url": "/?< paste ID >"
   }

Setting an Expiration
^^^^^^^^^^^^^^^^^^^^^

There are a limited number of valid expiration times. You must select
one of the following:

.. code:: python

   ("5min", "10min", "1hour", "1day", "1week", "1month", "1year", "never")

The default is ``"1day"``.

.. code:: python

   >>> import privatebinapi
   >>> response = privatebinapi.send(
   ...     "https://vim.cx",
   ...     text="Hello, world!",
   ...     expiration="5min"
   ... )

Setting a password
^^^^^^^^^^^^^^^^^^

Putting a password on your paste is easy:

.. code:: python

   >>> import privatebinapi
   >>> response = privatebinapi.send(
   ...     "https://vim.cx",
   ...     text="Hello, world!",
   ...     password="Secure123!"
   ... )

Choosing Compression
^^^^^^^^^^^^^^^^^^^^

There are only two valid options for this parameter: ``"zlib"`` and
``None``. The default is ``"zlib"``.

.. code:: python

   >>> import privatebinapi
   >>> response = privatebinapi.send(
   ...     "https://vim.cx",
   ...     text="Hello, world!",
   ...     compression=None
   ... )

Choosing a Format
^^^^^^^^^^^^^^^^^

There are only three valid options for this parameter: ``"plaintext"``,
``"syntaxhighlighting"``, and ``"markdown"``. The default is
``"plaintext"``.

.. code:: python

   >>> import privatebinapi
   >>> response = privatebinapi.send(
   ...     "https://vim.cx",
   ...     text="Hello, world!",
   ...     formatting="markdown"
   ... )

Burn After Reading
^^^^^^^^^^^^^^^^^^

If you want a paste to be deleted immediately after being read, pass
``True`` to the *burn_after_reading* parameter. The default is
``False``.

.. code:: python

   >>> import privatebinapi
   >>> response = privatebinapi.send(
   ...     "https://vim.cx",
   ...     text="Hello, world!",
   ...     burn_after_reading=True
   ... )

Enable Discussion
^^^^^^^^^^^^^^^^^

To enable discussion, pass ``True`` to the *discussion* parameter. The
default is ``False``.

.. code:: python

   >>> import privatebinapi
   >>> response = privatebinapi.send(
   ...     "https://vim.cx",
   ...     text="Hello, world!",
   ...     discussion=True
   ... )

Getting a Paste
~~~~~~~~~~~~~~~

Getting a paste from a PrivateBin instance is very easy:

.. code:: python

   >>> import privatebinapi
   >>> response = privatebinapi.get("https://example.com/?fakePasteLink#1234567890")

You can expect the get function to return something similar to the following:

.. code:: text

   {
       "attachment": {
           "content": b"< attachment content in bytes >",
           "filename": "< name of attachment >"
       },
       "id": '< paste ID >",
       "meta": {
           "created": < UNIX timestamp >,
           "time_to_live": < seconds until deletion >
       },
       "status": 0,
       "text": "< text content of the paste >",
       "url": "/?< paste ID >",
       "v": < encryption version 1 or 2 >}
   }

Getting a Password Protected Paste
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If the paste is password protected, use the *password* parameter.

.. code:: python

   >>> import privatebinapi
   >>> response = privatebinapi.get(
   ...     "https://example.com/?fakePasteLink#1234567890",
   ...     password="Secure123!"
   ... )

Deleting a Paste
~~~~~~~~~~~~~~~~

You can expect the delete function to return something similar to the following:

.. code:: text

   {
       "id": '< paste ID >",
       "status": 0,
       "url": "/?< paste ID >",
   }

To delete a paste, you need its URL and delete token.

.. code:: python

   >>> import privatebinapi
   >>> response = privatebinapi.delete(
   ...     "https://example.com/?fakePasteLink#1234567890",
   ...     "fake1delete2token3"
   ... )

Using a Proxy
~~~~~~~~~~~~~

All functions have an optional keyword parameter, *proxies*, that
accepts a dictionary of proxies like you would see in the Requests
package.

.. code:: python

   >>> import privatebinapi
   >>> response = privatebinapi.send(
   ...     "https://vim.cx",
   ...     text="Hello, world!",
   ...     proxies={
   ...         "http": "http://example.com/proxy:80",
   ...         "https": "https://example.com/proxy:8080"
   ...     }
   ... )

Using Async Functions
~~~~~~~~~~~~~~~~~~~~~

``privatebinapi.send``, ``privatebinapi.get`` and
``privatebinapi.delete`` all have async analogs. They accept all the
same parameters that their synchronous counterparts do.

.. code:: python

   import asyncio

   import privatebinapi

   async def main():
       send_response = await privatebinapi.send_async(
           "https://vim.cx",
           text="Hello, world!"
       )
       get_response = await privatebinapi.get_async(send_response["full_url"])
       delete_response = await privatebinapi.delete_async(
           send_response["full_url"],
           send_response["deletetoken"]
       )

   loop = asyncio.get_event_loop()
   loop.run_until_complete(main())

Both ``privatebinapi.send`` and ``privatebinapi.get`` do encryption and
decryption using an executor_. It will use the default
executor for your event loop if *executor* is ``None``.

.. _executor: https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.Executor

License
~~~~~~~
PrivateBin API is offered under the `MIT license`_.

.. _MIT license: https://github.com/Pioverpie/privatebin-api/blob/master/LICENSE


.. |Codacy Badge| image:: https://app.codacy.com/project/badge/Grade/b0b11fa99727453eb219bcd0b03f5868
   :target: https://www.codacy.com/gh/Pioverpie/privatebin-api/dashboard
.. |codecov| image:: https://codecov.io/gh/Pioverpie/privatebin-api/branch/master/graph/badge.svg?token=5YE0802BC1
   :target: https://codecov.io/gh/Pioverpie/privatebin-api
.. |Build Status| image:: https://travis-ci.org/Pioverpie/privatebin-api.svg?branch=master
   :target: https://travis-ci.org/Pioverpie/privatebin-api
.. |Maintainability| image:: https://api.codeclimate.com/v1/badges/b6dcd84fe476440a1811/maintainability
   :target: https://codeclimate.com/github/Pioverpie/privatebin-api/maintainability
.. |Code Climate issues| image:: https://img.shields.io/codeclimate/issues/Pioverpie/privatebin-api
   :target: https://codeclimate.com/github/Pioverpie/privatebin-api/issues
.. |Code Climate technical debt| image:: https://img.shields.io/codeclimate/tech-debt/Pioverpie/privatebin-api
   :target: https://codeclimate.com/github/Pioverpie/privatebin-api/trends/technical_debt
.. |GitHub repo size| image:: https://img.shields.io/github/repo-size/Pioverpie/privatebin-api
   :target: https://github.com/Pioverpie/privatebin-api
.. |License badge| image:: https://img.shields.io/github/license/Pioverpie/privatebin-api
   :alt: GitHub
   :target: https://github.com/Pioverpie/privatebin-api/blob/master/LICENSE
