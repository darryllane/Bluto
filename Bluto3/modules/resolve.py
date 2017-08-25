#!/usr/local/bin/python

# -*- coding: utf-8 -*-

import sys
import re
import traceback
import socket
import dns.resolver
import random
import string
from termcolor import colored
from logger_ import info


#Settings DNS Timout Values
def _set(args):
	ns_list= []
	info('Setting Up Resolver')
	timeout_value = args.timeo
	if not timeout_value:
		timeout_value = 5
	myResolver = dns.resolver.Resolver()
	myResolver.timeout = int(timeout_value)
	myResolver.lifetime = int(timeout_value)
	myResolver.nameservers = ['8.8.8.8', '8.8.4.4']

	return myResolver


#Gathers Record Types NS, MX
def dns_records(domain, myResolver):
	info('Gathering DNS Details')
	ns_list = []
	zn_list =[]
	mx_list = []
	try:
		print "\nName Server:\n"
		myAnswers = myResolver.query(domain, "NS")
		for data in myAnswers.rrset:
			data = (str(data).rstrip('.'))
			addr = socket.gethostbyname(data)
			ns_list.append(data + '\t' + addr)
			zn_list.append(data)
			list(set(ns_list))
			ns_list.sort()
		for i in ns_list:
			print colored(i, 'green')

	except dns.resolver.NoNameservers:
		print('\tNo Name Servers\nConfirm The Domain Name Is Correct.')
		sys.exit()
	except dns.resolver.NoAnswer:
		print "\tNo DNS Servers"
	except dns.resolver.NXDOMAIN:
		print("\tDomain Does Not Exist")
		sys.exit()
	except dns.resolver.Timeout:
		print('\tTimeouted\nConfirm The Domain Name Is Correct.')
		sys.exit()
	except Exception:
		info(traceback.print_exc())
		print('An Unhandled Exception Has Occured, Please Check The Log For Details\n')

	try:
		print "\nMail Server:\n"
		myAnswers = myResolver.query(domain, "MX")
		for data in myAnswers:
			data = (str(data).split(' ',1)[1].rstrip('.'))
			addr = socket.gethostbyname(data)
			mx_list.append(data + '\t' + addr)
		list(set(mx_list))
		mx_list.sort()
		for i in mx_list:
			print colored(i, 'green')
	except dns.resolver.Timeout:
		pass
	except socket.gaierror:
		pass
	except dns.resolver.NoAnswer:
		print "\tNo Mail Servers"
	except Exception:
		info(traceback.print_exc())
		info('An Unhandled Exception Has Occured, Please Check The Log For Details\n')
	info('\nCompleted Gathering DNS Details')
	return zn_list


#Checks Valid Domain Entry
def domain_check(domain, myResolver):
	try:
		myAnswers = myResolver.query(domain, "NS")
		dom = str(myAnswers.canonical_name).strip('.')
		if dom:
			pass
	except dns.resolver.NoNameservers:
		print '\nError: Domain Not Valid\n\nHave you typed the domain name correctly?\nYou Entered: {}'.format(domain)
		sys.exit()
	except dns.resolver.NXDOMAIN:
		print '\nError: Domain Not Valid\n\nHave you typed the domain name correctly?\nYou Entered: {}'.format(domain)
		sys.exit()
	except dns.exception.Timeout:
		print '\nError: Timeout\n\nAre you connected to the internet?\nHave you typed the domain name correctly?'
		sys.exit()
	except Exception:
		info(traceback.print_exc())
		info('An Unhandled Exception Has Occured, Please Check The Log For Details\n')


def main(args):
	domain = args.domain
	my_resolver = _set(args)
	domain_check(domain, my_resolver)
	dns_records(domain, my_resolver)

