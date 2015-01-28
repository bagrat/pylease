from abc import ABCMeta, abstractmethod


class Extension(object):
    __metaclass__ = ABCMeta

    def __init__(self, arg_parser):
        super(Extension, self).__init__()

        self.arg_parser = arg_parser

    @abstractmethod
    def execute(self):
        pass