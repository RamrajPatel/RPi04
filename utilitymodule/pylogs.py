__author__ = 'Ramraj'

import logging
import logging.handlers

LOGGER_NAME = 'RPI_LOGGER'
LOG_FILENAME = 'H:\RPi_Params\Rpi_Logs\logging_rotatingfile_example.out'
LOG_FILE_MAX_SIZE = 500000000
LOG_FILE_MAX_BKPS = 10

'''
    Below given are different level of Logging.
    Select any of them based on Requirement
'''
# LOG_LEVEL = logging.DEBUG
LOG_LEVEL = logging.INFO
# LOG_LEVEL = logging.WARNING
# LOG_LEVEL = logging.ERROR
# LOG_LEVEL = logging.CRITICAL


class PyLogs(object):
    logg = None

    def __init__(self, name):
        # Set up a specific logger with our desired output level
        # print('Inside PyLogs init')

        # self.logg = logging.getLogger(LOGGER_NAME)
        self.logg = logging.getLogger(name)

        self.logg.setLevel(LOG_LEVEL)
        # Add the log message handler to the logger
        handler = logging.handlers.RotatingFileHandler(LOG_FILENAME,
                                                       maxBytes=LOG_FILE_MAX_SIZE, backupCount=LOG_FILE_MAX_BKPS, delay=None)

        # create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        handler.setFormatter(formatter)

        #adding handler
        self.logg.addHandler(handler)

        # print('Logger object creation Done')

    def get_pylogger(self):
        return self.logg