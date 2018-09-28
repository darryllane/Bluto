import logging
import sys
import os


LOG_ROOT = os.path.expanduser('~/Bluto/')
LOG_DIR = (LOG_ROOT + 'log/')
INFO_LOG_FILE = (LOG_DIR + 'bluto3-info.log')
ERROR_LOG_FILE = (LOG_DIR + 'bluto3-error.log')


if not os.path.exists(LOG_DIR):
	os.makedirs(LOG_DIR)
	os.chmod(LOG_DIR, 0o700)	
if not os.path.exists(LOG_ROOT):
	os.makedirs(LOG_ROOT)
	os.chmod(LOG_ROOT, 0o700)
	if not os.path.exists(LOG_DIR):
		os.makedirs(LOG_DIR)
		os.chmod(LOG_DIR, 0o700)

open(INFO_LOG_FILE,'a').close()
open(ERROR_LOG_FILE,'a').close()

# set up formatting
formatter = logging.Formatter('[%(asctime)s] %(module)s: %(message)s')
formatter2 = logging.Formatter('[%(asctime)s] %(message)s')

# set up logging for INFO
fh1 = logging.FileHandler(INFO_LOG_FILE)
fh1.setLevel(logging.INFO)
fh1.setFormatter(formatter)

# set up logging for ERROR
fh2 = logging.FileHandler(ERROR_LOG_FILE)
fh2.setLevel(logging.ERROR)
fh2.setFormatter(formatter2)

# create Loggers object
mylogger = logging.getLogger('MyLogger')
mylogger.setLevel(logging.INFO)
mylogger.addHandler(fh1)

mylogger2 = logging.getLogger('MyLogger2')
mylogger2.setLevel(logging.ERROR)
mylogger2.addHandler(fh2)

# create shortcut functions
info = mylogger.info
error = mylogger2.error
