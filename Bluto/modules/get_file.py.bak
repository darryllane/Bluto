#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import traceback
import sys
import random
from termcolor import colored
from bluto_logging import info, INFO_LOG_FILE

def get_user_agents(useragent_f):
    info('Gathering UserAgents')
    uas = []
    with open(useragent_f, 'rb') as uaf:
        for ua in uaf.readlines():
            if ua:
                uas.append(ua.strip()[1:-1-1])
    random.shuffle(uas)
    info('Completed Gathering UserAgents')
    return uas


def get_subs(filename, domain):
    info('Gathering SubDomains')
    full_list = []
    try:
        subs = [line.rstrip('\n') for line in open(filename)]
        for sub in subs:
            full_list.append(str(sub.lower() + "." + domain))
    except Exception:
        info('An Unhandled Exception Has Occured, Please Check The Log For Details' + INFO_LOG_FILE)
        sys.exit()

    info('Completed Gathering SubDomains')
    return full_list

def get_sub_interest(filename, domain):
    info('Gathering SubDomains Of Interest')
    full_list = []
    try:
        subs = [line.rstrip('\n') for line in open(filename)]
        for sub in subs:
            full_list.append(str(sub.lower() + "." + domain))

    except Exception:
        info('An Unhandled Exception Has Occured, Please Check The Log For Details' + INFO_LOG_FILE)
        sys.exit()

    info('Completed Gathering SubDomains Of Interest')
    return full_list


def get_line_count(filename):
    info('Gathering SubDomains Count')
    lines = 0
    for line in open(filename):
        lines += 1

    info('Completed Gathering SubDomains Count')
    return lines
