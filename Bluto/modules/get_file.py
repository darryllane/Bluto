#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import traceback
import sys
import random
from termcolor import colored
from bluto_logging import warning

def get_user_agents(useragent_f):
    uas = []
    with open(useragent_f, 'rb') as uaf:
        for ua in uaf.readlines():
            if ua:
                uas.append(ua.strip()[1:-1-1])
    random.shuffle(uas)
    return uas


def get_subs(filename, domain):
    full_list = []
    try:
        subs = [line.rstrip('\n') for line in open(filename)]
        for sub in subs:
            full_list.append(str(sub.lower() + "." + domain))
    except Exception:
        print 'An Unhandled Exception Has Occured, Please Check The Log For Details\n'
        warning(traceback.print_exc())
        sys.exit()

    return full_list

def get_sub_interest(filename, domain):
    full_list = []
    try:
        subs = [line.rstrip('\n') for line in open(filename)]
        for sub in subs:
            full_list.append(str(sub.lower() + "." + domain))

    except Exception:
        print 'An Unhandled Exception Has Occured, Please Check The Log For Details\n'
        warning(traceback.print_exc())
        sys.exit()

    return full_list


def get_line_count(filename):
    lines = 0
    for line in open(filename):
        lines += 1
    return lines
