import decouple
from abc import ABC


class Settings(ABC):

    def __init__(self):
        self.is_local = None
        self.root_path = None
        self._setup()

    def _setup(self):
        self.is_local = Settings._load_variable(variable='IS_LOCAL', default=False, cast=bool)
        self.root_path = '.' if self.is_local else '/tmp'

    @staticmethod
    def _load_variable(variable: str, default=None, cast: type = str):
        try:
            return decouple.config(variable, default=default, cast=cast)
        except decouple.UndefinedValueError:
            return default
