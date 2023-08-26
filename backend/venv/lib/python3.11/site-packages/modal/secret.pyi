import modal.object
import typing

class _Secret(modal.object._Object):
    @staticmethod
    def from_dict(env_dict: typing.Dict[str, str] = {}, template_type=''):
        ...

    @staticmethod
    def from_dotenv(path=None):
        ...


class Secret(modal.object.Object):
    def __init__(self):
        ...

    @staticmethod
    def from_dict(env_dict: typing.Dict[str, str] = {}, template_type=''):
        ...

    @staticmethod
    def from_dotenv(path=None):
        ...
