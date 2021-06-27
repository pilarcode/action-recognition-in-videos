import logging
import sys

class AppLogger:

    def __init__(self):
        self.logger = self.setup_custom_logger("app")

    def setup_custom_logger(self,name):
        formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s',
                                    datefmt='%Y-%m-%d %H:%M:%S')
        handler = logging.FileHandler('log.txt', mode='w')
        handler.setFormatter(formatter)
        screen_handler = logging.StreamHandler(stream=sys.stdout)
        screen_handler.setFormatter(formatter)
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(handler)
        logger.addHandler(screen_handler)
        return logger
        
    def info(self,message):
        self.logger.info(message)

    def error(self,message):
        self.logger.error(message)
