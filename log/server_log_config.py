import os
import sys
from logging import Formatter, StreamHandler, INFO, getLogger, DEBUG
from logging.handlers import TimedRotatingFileHandler

LOG_FILE_PATH = os.path.join(os.getcwd(), 'log', 'logs', 'server.log')

formatter = Formatter('%(asctime)s %(levelname)s %(filename)s %(message)s')

stream_handler = StreamHandler(sys.stderr)
stream_handler.setFormatter(formatter)
stream_handler.setLevel(INFO)

file_handler = TimedRotatingFileHandler(LOG_FILE_PATH, encoding='utf-8', interval=1, when='d')
file_handler.setFormatter(formatter)

logger = getLogger('server')
logger.addHandler(stream_handler)
logger.addHandler(file_handler)
logger.setLevel(DEBUG)

if __name__ == '__main__':
    logger.debug('Debug info')
    logger.info('Info')
    logger.error('Error')
    logger.critical('Critical error')
