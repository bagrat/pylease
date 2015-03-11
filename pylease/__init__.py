import logging

__author__ = 'bagrat'
__version__ = '0.2'

_LOGGING_FMT = "%(levelname)s: %(message)s"

logme = logging.getLogger(__name__)
logme.setLevel(logging.ERROR)

handler = logging.StreamHandler()
handler.setLevel(logging.ERROR)
handler.setFormatter(logging.Formatter(fmt=_LOGGING_FMT))

logme.addHandler(handler)
