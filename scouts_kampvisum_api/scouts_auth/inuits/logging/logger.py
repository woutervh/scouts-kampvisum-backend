import logging, logging.config


class InuitsLogger(logging.getLoggerClass()):
    name: str
    level: str

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def note(self, msg, *args, **kwargs):
        self.log(logging.NOTE, msg, *args, **kwargs)

    def trace(self, msg, *args, **kwargs):
        self.log(logging.TRACE, msg, *args, **kwargs)

    def api(self, msg, *args, **kwargs):
        self.log(logging.API, msg, *args, **kwargs)

    @staticmethod
    def setup_logging(config=None):
        logging.NOTE = logging.INFO + 5
        logging.TRACE = logging.DEBUG - 5
        logging.API = logging.DEBUG - 10

        logging.addLevelName(logging.INFO + 5, "NOTE")
        logging.addLevelName(logging.DEBUG - 5, "TRACE")
        logging.addLevelName(logging.DEBUG - 10, "API")

        logging.setLoggerClass(InuitsLogger)

        if config:
            logging.config.dictConfig(config)
