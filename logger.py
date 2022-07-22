import logging
import pathlib
import os
import sys
from datetime import datetime
from datetime import date
from logging.handlers import TimedRotatingFileHandler

class Logger:
    
    def __init__(self):
        self.base_folder = f'logs'
        self.__set_logger()

    def __set_logger(self):
        """[logger]
        Set logger configuration 
        
        1. log_ (main log file)
        2. sub log file (day basis) -> log_imnosmt._%Y_%m_%d
        Raises:
            ValueError: [on Invalid log level]
        """
        try:
            loglevel='debug'

            # Folder path to save log
            log_folder = './logs'
            # log File path
            log_filename = 'log_'
             
            log_file_path = f'{log_folder}/{log_filename}'
            # create folder
            pathlib.Path(log_folder).mkdir(parents=True, exist_ok=True)

            numeric_level = getattr(logging, loglevel.upper(), None)
            if not isinstance(numeric_level, int):
                raise ValueError('Invalid log level: %s' % loglevel)

            handler = TimedRotatingFileHandler(log_file_path, when="midnight", interval=1)
            handler.suffix = "_%Y_%m_%d_.txt"
            formatter = logging.Formatter(
                '%(asctime)s | %(levelname)s |%(module)s -> %(funcName)s -> %(lineno)d :\n%(message)s\n')
            handler.setFormatter(formatter)

            logger = logging.getLogger('my_logger')
            logger.setLevel(numeric_level)
            logger.addHandler(handler)

            # return logger
        except Exception as e:
            # print(e)
            sys.stderr.write(f'Printing error to apache log : {e}')
