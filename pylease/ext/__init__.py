from abc import ABCMeta, abstractmethod
from pylease.logger import LOGME as logme  # noqa


class Extension(object):
    """
    The entry point to implementing Pylease extensions. Pylease loads subclasses of this class and invokes the
    :func:`~pylease.ext.Extension.load` method.

    Attributes:
        _lizy (pylease.Pylease): The :class:`~pylease.Pylease` singleton, that is initialised and passed to all subclass instances.
    """
    # pylint: disable=abstract-class-not-used
    __metaclass__ = ABCMeta

    _IGNORE_ME_VAR_NAME = 'ignore_me'
    ignore_me = False

    def __init__(self, lizy):
        super(Extension, self).__init__()

        logme.debug("Initializing %s", self.__class__.__name__)

        self._lizy = lizy

        self.load()

    @abstractmethod
    def load(self):
        """
        This method is being called by Pylease when all the extensions are being loaded.  All the initialisation code must be implemented
        in the body of this method.
        """
        pass  # pragma: no cover

    @classmethod
    def init_all(cls, lizy):
        extensions = cls.__subclasses__()

        for extension in extensions:
            extension.init_all(lizy)
            if not getattr(extension, cls._IGNORE_ME_VAR_NAME):
                extension(lizy)
