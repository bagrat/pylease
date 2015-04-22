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

    f = inspect.stack()[1 + depth]
    return inspect.getmodule(f[0])


class SubclassIgnoreMark(object):
    def __init__(self, cls_name):
        super(SubclassIgnoreMark, self).__init__()
        self._cls_name = cls_name

    def __get__(self, instance, owner):
        if owner.__name__ == self._cls_name:
            return True
        else:
            return False