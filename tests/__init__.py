FILE = 'tests/__init__.py'
MESSAGE = 'This is a test.'
RESPONSE_DATA = {'status': 1, 'message': 'fail'}
SERVERS_AND_FILES = (
    ('https://vim.cx', FILE),  # PrivateBin 1.3
    ('https://privatebin.gittermann1.de/', FILE),  # PrivateBin 1.2
    ('https://paste.carrade.eu/', FILE),  # PrivateBin 1.1
    ('https://paste.nikul.in/', None)  # PrivateBin 1.0
)

__all__ = ('MESSAGE', 'RESPONSE_DATA', 'SERVERS_AND_FILES')
