import logging
import sys


class info_debug_filter(logging.Filter):
    @staticmethod
    def filter(record: logging.LogRecord):
        if record.levelno <= logging.INFO:
            return True
        return False


class warning_filter(logging.Filter):
    @staticmethod
    def filter(record: logging.LogRecord):
        if record.levelno == logging.WARNING:
            return True
        return False


class error_filter(logging.Filter):
    @staticmethod
    def filter(record: logging.LogRecord):
        if record.levelno >= logging.ERROR:
            return True
        return False


def setup_logging():
    logger = logging.getLogger()
    sh = logging.StreamHandler(sys.stderr)
    sh.addFilter(info_debug_filter)
    wh = logging.StreamHandler(sys.stderr)
    wh.addFilter(warning_filter)
    wh.setFormatter(logging.Formatter(fmt="\033[93m%(message)s\033[0m"))
    eh = logging.StreamHandler(sys.stderr)
    eh.addFilter(error_filter)
    eh.setFormatter(logging.Formatter(fmt="\033[31m%(message)s\033[0m"))
    logger.addHandler(sh)
    logger.addHandler(wh)
    logger.addHandler(eh)
