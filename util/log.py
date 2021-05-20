import logging


class Log(object):

    @staticmethod
    def setup(name: str) -> logging.Logger:
        formatter = logging.Formatter(fmt='%(levelname)s | %(module)s.%(funcName)s: %(message)s')
        handler = logging.StreamHandler()
        handler.setFormatter(fmt=formatter)
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)
        logger.addHandler(hdlr=handler)
        return logger

    @staticmethod
    def get_logger(name: str):
        return logging.getLogger(name=name)
