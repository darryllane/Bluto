#!/usr/bin/python

import logging
import sys
import site
import os

sites = site.getsitepackages()

for item in sites:
    if os.path.exists(item + "/Bluto/doc/subdomains-top1mil-20000.txt"):
        path = item
    else:
        pass

WARNING_LOG_FILENAME = path + '/Bluto/log/bluto-warn.log'

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
