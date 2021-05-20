from settings.settings import Settings


class AWSSettings(Settings):

    def __init__(self):
        super().__init__()
        self.raw_bucket = 'devpira-raw'
        self.enriched_bucket = 'devpira-enriched'
