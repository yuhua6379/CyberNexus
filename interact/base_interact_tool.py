from abc import abstractmethod


class BaseInteractTool:

    @abstractmethod
    def call(self, message):
        pass

    def __call__(self, *args, **kwargs):
        return self.call(args[0])
