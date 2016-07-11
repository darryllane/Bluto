#!/usr/bin/python

import logging
import sys
import site
import os

working_dir = os.path.expanduser('~')
log_file = '/Bluto/log/bluto-warn.log'

if not os.path.exists(working_dir + '/Bluto/log'):
    os.makedirs(working_dir + '/Bluto/log')
    open(working_dir + log_file,'a').close()


WARNING_LOG_FILENAME = working_dir + '/Bluto/log/bluto-warn.log'

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
fh2 = logging.FileHandler(WARNING_LOG_FILENAME)
fh2.setLevel(logging.WARN)
fh2.setFormatter(formatter)

# create Logger object
mylogger = logging.getLogger('MyLogger')
mylogger.setLevel(logging.DEBUG)
#mylogger.addHandler(sh) #Uncomment to write to console
#mylogger.addHandler(fh) #Uncomment to create Debug Handler
mylogger.addHandler(fh2)

# create shortcut functions
#debug = mylogger.debug
#info = mylogger.info
warning = mylogger.warning
#error = mylogger.error
#critical = mylogger.critical
