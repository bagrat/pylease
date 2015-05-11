import inspect


def get_caller_module(depth=0):
    """Get the module from where this method was called

    If this method is wrapped into another one, and the client is calling the
    wrapper method, this will return the wrapper method. The solution to this
    situation is to specify the depth when calling this method. For that case
    it should be 1.
    Copied from pyflect 0.1.3, not to have any cross-dependence.

    :param depth: The depth of the call
    :return: The module instance
    """

    frame = inspect.stack()[1 + depth]
    return inspect.getmodule(frame[0])


class SubclassIgnoreMark(object):
    """
    This class is designed to mark particular classes for special purposes. It
    implements the Descriptor protocol, and the value of a property instance of
    this class is True only for the class where the property was originally assigned.
    """
    def __init__(self, cls_name):
        """
        :param cls_name: The class name to be marked.
        """
        super(SubclassIgnoreMark, self).__init__()
        self._cls_name = cls_name

    def __get__(self, instance, owner):
        return owner.__name__ == self._cls_name


def ignore_subclass(klass):
    """
    This decorator may be used in place of `IgnoreSubclass` in order to emit the parenthesis,
    and use the default property name for the Ignore Mark. It does not add any functionality.
    """
    decorator = IgnoreSubclass()

    return decorator(klass)


class IgnoreSubclass(object):
    """
    This decorator adds the Ignore Mark to the decorated class, without a need to specify
    the class name itself. This class requires to define the property name to be used for
    the Ignore Mark. To avoid this verbosity the mark has a default value of `"ignore"`.
    """
    DEFAULT_MARK_NAME = 'ignore'

    def __init__(self, mark_name=DEFAULT_MARK_NAME):
        super(IgnoreSubclass, self).__init__()

        self._mark_name = mark_name

    def __call__(self, klass):
        setattr(klass, self._mark_name, SubclassIgnoreMark(klass.__name__))

        return klass
