import logging

formatter = logging.Formatter('%(asctime)s %(levelname)s - %(name)s - %(message)s')
loggers = {}
__APP_LOGIN_LEVEL = logging.INFO


def __get_logger(logger_name="Domotica", loggin_level=logging.DEBUG):
    if logger_name not in loggers:
        logger = logging.getLogger(logger_name)
        logger.setLevel(__APP_LOGIN_LEVEL)
        #ch = logging.FileHandler(filename="/tmp/domotica/domotica.log")
        ch = logging.StreamHandler()
        ch.setLevel(loggin_level)
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        loggers[logger_name] = logger
    return loggers[logger_name]


def debug(logger_name="Domotica", msg=""):
    __get_logger(logger_name=logger_name, loggin_level=logging.DEBUG).debug(msg)


def info(logger_name="Domotica", msg=""):
    __get_logger(logger_name=logger_name, loggin_level=logging.INFO).info(msg)