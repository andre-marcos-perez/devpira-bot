from settings.settings import Settings


class TelegramSettings(Settings):

    def __init__(self):
        super().__init__()
        self.chat_id = None
        self.access_token = None
        self.__setup()

    def __setup(self):
        self.chat_id = TelegramSettings._load_variable(variable='TELEGRAM_CHAT_ID', default=None, cast=int)
        self.access_token = TelegramSettings._load_variable(variable='TELEGRAM_ACCESS_TOKEN', default=None, cast=str)
