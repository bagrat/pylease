from abc import ABCMeta, abstractmethod


class Extension(object):
    __metaclass__ = ABCMeta

    def __init__(self, arg_parser):
        super(Extension, self).__init__()

        self.arg_parser = arg_parser

    @abstractmethod
    def execute(self, args, version):
        pass

    @classmethod
    def init_all(cls, extensions, arg_parser):
        result = []

        for extension in extensions:
            result.append(extension(arg_parser))

        return result

    @classmethod
    def execute_all(cls, extensions, args, version):
        for extension in extensions:
            extension.execute(args, version)
