
import logging
import sys


logger = logging.getLogger('nhentai')

FORMATTER = logging.Formatter("\r[%(asctime)s] [%(levelname)s] %(message)s", "%H:%M:%S")

LOGGER_HANDLER = logging.StreamHandler(sys.stdout)
LOGGER_HANDLER.setFormatter(FORMATTER)

logger.addHandler(LOGGER_HANDLER)
logger.setLevel(logging.DEBUG)


if __name__ == '__main__':

    logger.log(15, 'nhentai')
    logger.info('info')
    logger.warning('warning')
    logger.debug('debug')
    logger.error('error')
    logger.critical('critical')
