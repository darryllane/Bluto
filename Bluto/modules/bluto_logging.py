#!/usr/bin/python

import logging
import sys
import site
import os
LOG_DIR = os.path.expanduser('~/Bluto/log/')
INFO_LOG_FILE = os.path.expanduser(LOG_DIR + 'bluto-info.log')
ERROR_LOG_FILE = os.path.expanduser(LOG_DIR + 'bluto-error.log')

if not os.path.exists(os.path.expanduser('~/Bluto/log')):
    os.makedirs(os.path.expanduser('~/Bluto/log'))
    open(INFO_LOG_FILE,'a').close()
    open(ERROR_LOG_FILE,'a').close()


# set up formatting
formatter = logging.Formatter('[%(asctime)s] %(module)s: %(message)s')

# set up logging to STDOUT for all levels DEBUG and higher (Uncomment section to write to console)
#sh = logging.StreamHandler(sys.stdout)
#sh.setLevel(logging.DEBUG)
#sh.setFormatter(formatter)

# set up logging to a file for all levels DEBUG and higher
#fh = logging.FileHandler(DEBUG_LOG_FILENAME)
#fh.setLevel(logging.DEBUG)
#fh.setFormatter(formatter)

# set up logging to a file for all levels WARNING and higher
fh2 = logging.FileHandler(INFO_LOG_FILE)
fh2.setLevel(logging.INFO)
fh2.setFormatter(formatter)

# set up logging to a file for ERROR
fh3 = logging.FileHandler(ERROR_LOG_FILE)
fh3.setLevel(logging.ERROR)
fh3.setFormatter(formatter)

# create Logger object
mylogger = logging.getLogger('MyLogger')
mylogger2 = logging.getLogger('MyLoggerError')

mylogger.setLevel(logging.INFO)
mylogger2.setLevel(logging.ERROR)
#mylogger.addHandler(sh) #Uncomment to write to console
#mylogger.addHandler(fh) #Uncomment to create Debug Handler
mylogger.addHandler(fh2)
mylogger2.addHandler(fh3)

# create shortcut functions
#debug = mylogger.debug
info = mylogger.info
#warning = mylogger.warning
error = mylogger2.error
#critical = mylogger.critical
