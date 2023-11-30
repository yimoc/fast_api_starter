import logging
import logging.config
import os


def set_logger(path: str):
    log_conf_path = os.path.join(path, "logging.conf")
    logging.config.fileConfig(log_conf_path)

def set_log(app_path: str):
    os.makedirs('./logs', exist_ok=True)
    os.makedirs('./logs/ray', exist_ok=True)
    path = os.path.join(app_path, 'app', 'conf')
    set_logger(path)

def logged(func, *args, **kwargs):
    '''
    @logged logging arguments
    '''
    logger = logging.getLogger()
    def new_func(*args, **kwargs):
        logger.debug("calling {} with args {} and kwargs {}".format(
                func.__name__, args, kwargs))
        return func(*args, **kwargs)
    return new_func

# logging
# https://docs.python.org/3/library/logging.config.html#logging.config.fileConfig