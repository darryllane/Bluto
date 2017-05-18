#!/usr/bin/python

import logging
import sys
import site
import os
LOG_DIR = os.path.expanduser('~/Bluto/log/')
INFO_LOG_FILE = os.path.expanduser(LOG_DIR + 'bluto-info.log')

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)
    os.chmod(LOG_DIR, 0o700)
    open(INFO_LOG_FILE,'a').close()

# set up formatting
formatter = logging.Formatter('[%(asctime)s] %(module)s: %(message)s')

# set up logging to a file for all levels WARNING and higher
fh2 = logging.FileHandler(INFO_LOG_FILE)
fh2.setLevel(logging.INFO)
fh2.setFormatter(formatter)

# create Logger object
mylogger = logging.getLogger('MyLogger')
mylogger.setLevel(logging.INFO)
mylogger.addHandler(fh2)

# create shortcut functions
info = mylogger.info
