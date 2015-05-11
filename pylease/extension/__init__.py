from abc import ABCMeta, abstractmethod
from pylease.logger import LOGME as logme  # noqa


class Extension(object):
    # pylint: disable=abstract-class-not-used
    __metaclass__ = ABCMeta

    _IGNORE_ME_VAR_NAME = 'ignore_me'
    ignore_me = False

    def __init__(self, lizy):
        super(Extension, self).__init__()

        logme.debug("Initializing {}".format(self.__class__.__name__))

        self._lizy = lizy

        self.load()

    @abstractmethod
    def load(self):
        pass  # pragma: no cover

    @classmethod
    def init_all(cls, lizy):
        extensions = cls.__subclasses__()

        for extension in extensions:
            extension.init_all(lizy)
            if not getattr(extension, cls._IGNORE_ME_VAR_NAME):
                extension(lizy)
