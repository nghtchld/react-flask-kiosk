import os
import time
import logging as log
from logging.handlers import RotatingFileHandler
from collections import namedtuple

from kiosk import app

def log_debug():
    # if not app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    log_filename = f"{time.strftime('%Y-%m-%d %H%M%S')}-kiosk.log"
    file_handler = RotatingFileHandler(os.path.join('logs',log_filename), maxBytes=20480,
                                        backupCount=10)
    file_handler.setFormatter(log.Formatter(
        '%(asctime)-15s %(levelname)-8s: %(message)-s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(log.DEBUG)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(log.DEBUG)
    app.logger.info(f'App name starting:{app.name}')


logger = log.getLogger("wrap_func_logger")

def log_func(pre, post):
    """ 
    Creates decorator for wrapping and logging functions.
    Usage: @log_func(entering,exiting)
    """
    def decorate(func):
        """ Decorator """
        def call(*args, **kwargs):
            """ Actual wrapping """
            pre(func, *args)
            result = func(*args, **kwargs)
            post(func)
            return result
        return call
    return decorate


def entering(func, *args):
    """ Pre function logging """
    logger.debug("Entered %s", func.__name__)
    logger.info(func.__doc__)
    logger.info("Function at line %d in %s" %
        (func.__code__.co_firstlineno, func.__code__.co_filename))
    try:
        if len(args) == 0:
            logger.warn("No arguments.")
        else:
             logger.warn("The argument %s is %s" % (func.__code__.co_varnames[0], *args))
    except IndexError:
        logger.warn("No arguments")
    except TypeError:
        logger.warn("No arguments")


def exiting(func):
    """ Post function logging """
    logger.debug("Exited  %s", func.__name__)


Item = namedtuple('Item','foodID, name, price, description, image, options')