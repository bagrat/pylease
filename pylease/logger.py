import logging


class ColorFormatter(logging.Formatter):  # pragma: no cover
    # pylint: disable=too-few-public-methods
    """
    Custom Formatter for Pylease logger that colors the log message depending on the log level.
    """
    color_end = "\x1b[1;0m"
    colors = dict(
        default='0',
        grey='30',
        green="32",
        red="31",
        yellow="33",
        purple="35",
        cyan="36"
    )
    level_map = {
        logging.DEBUG: ('cyan', False),
        logging.INFO: ('green', False),
        logging.WARNING: ('yellow', False),
        logging.ERROR: ('red', False),
        logging.CRITICAL: ('red', True)
    }

    def __init__(self, fmt=None, datefmt=None):
        super(ColorFormatter, self).__init__(fmt, datefmt)

    def format(self, record):
        lvl = int(record.levelno / 10) * 10
        record.msg = self._colorize(self.level_map.get(lvl)[0], record.msg, self.level_map.get(lvl)[1])
        return super(ColorFormatter, self).format(record)

    def _colorize(self, color, text, bold=False):
        """
        Borrowed from nosetests spec plugin by bitprophet https://github.com/bitprophet/spec/blob/master/spec/plugin.py
        """
        bold = 1 if bold else 0
        return "\x1b[%s;%sm%s%s" % (bold, self.colors.get(color, self.colors['default']), text, self.color_end)


class LevelFilter(logging.Filter):  # pragma: no cover
    # pylint: disable=too-few-public-methods
    def __init__(self, name='', level=logging.DEBUG):
        super(LevelFilter, self).__init__(name)

        self._level = level

    def filter(self, record):
        return int(record.levelno / 10) * 10 == self._level


_LOGGING_FMT = "%(message)s"

LOGME = logging.getLogger(__name__)
LOGME.setLevel(logging.DEBUG)

HANDLER = logging.StreamHandler()
HANDLER.setLevel(logging.INFO)
HANDLER.setFormatter(ColorFormatter(fmt=_LOGGING_FMT))

LOGME.addHandler(HANDLER)


def add_verbose_handler():  # pragma: no cover
    """
    Adds separate handler to the Pylease logger with level DEBUG.
    """
    verbose_handler = logging.StreamHandler()
    verbose_handler.setLevel(logging.DEBUG)
    verbose_handler.setFormatter(ColorFormatter(fmt=_LOGGING_FMT))

    verbose_handler.addFilter(LevelFilter(level=verbose_handler.level))

    LOGME.addHandler(verbose_handler)
