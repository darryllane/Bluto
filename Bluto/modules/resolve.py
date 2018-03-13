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
from .logger_ import info


#Settings DNS Timout Values
def _set(args):
	ns_list= []
	timeout_value = args.timeo
	if not timeout_value:
		timeout_value = 5
	myResolver = dns.resolver.Resolver()
	myResolver.timeout = int(timeout_value)
	myResolver.lifetime = int(timeout_value)
	myResolver.nameservers = ['8.8.8.8', '8.8.4.4']

	return myResolver


#Gathers Record Types NS, MX
def dns_records(args):
	info('gathering dns records')
	my_resolver = _set(args)
	domain = args.domain
	ns_list = []
	zn_list =[]
	mx_list = []
	try:
		print ("\nName Server:\n")
		myAnswers = my_resolver.query(domain, "NS")
		for data in myAnswers.rrset:
			hostname = str(data.target).strip('.')
			answers = my_resolver.query(hostname)
			for rdata in answers:
				ns_list.append(hostname + '\t' + rdata.address)
			zn_list.append(hostname)
			list(set(ns_list))
			ns_list.sort()
		for i in ns_list:
			print (colored(i, 'green'))

	except dns.resolver.NoNameservers:
		print('\nNo Name Servers\nConfirm The Domain Name Is Correct\n')
		sys.exit()
	except dns.resolver.NoAnswer:
		print ("\tNo DNS Servers")
	except dns.resolver.NXDOMAIN:
		print("\tDomain Does Not Exist")
		sys.exit()
	except dns.resolver.Timeout:
		print('\nTimeout\nConfirm The Domain Name Is Correct\n')
		sys.exit()
	except Exception:
		print (traceback.print_exc())
		print('An Unhandled Exception Has Occured, Please Check The Log For Details\n')

	try:
		print ("\nMail Server:\n")
		myAnswers = my_resolver.query(domain, "MX")
		for data in myAnswers.rrset.items:
			hostname = str(data).split(' ')[1].strip('.')
			answers = my_resolver.query(hostname)
			for rdata in answers:
				mx_list.append(hostname + '\t' + rdata.address)
		if mx_list:
			list(set(mx_list))
			mx_list.sort()
			for i in mx_list:
				print (colored(i, 'green'))
		else:
			print (colored('\n\tNo Mail Servers', 'red'))
	except dns.resolver.Timeout:
		print (colored('Timeout', 'red'))
	except socket.gaierror:
		pass
	except dns.resolver.NoAnswer:
		print ("\tNo Mail Servers")
	except Exception:
		info('An Unhandled Exception Has Occured, Please Check The Log For Details')
		info(traceback.print_exc())
	return zn_list


#Checks Valid Domain Entry
def domain_check(args):
	try:
		domain = args.domain
		my_resolver = _set(args)
		myAnswers = my_resolver.query(domain, "NS")
		dom = str(myAnswers.canonical_name).strip('.')
		if dom:
			pass
	except dns.resolver.NoNameservers:
		print ('\nError: Domain Not Valid\n\nHave you typed the domain name correctly?\nYou Entered: {}'.format(domain))
		sys.exit()
	except dns.resolver.NXDOMAIN:
		print ('\nError: Domain Not Valid\n\nHave you typed the domain name correctly?\nYou Entered: {}'.format(domain))
		sys.exit()
	except dns.exception.Timeout:
		print ('\nError: Timeout\n\nAre you connected to the internet?\nHave you typed the domain name correctly?')
		sys.exit()
	except Exception:
		info('An Unhandled Exception Has Occured, Please Check The Log For Details')
		info(traceback.print_exc())

def main(args):
	domain_check(args)
	dns_records(args)

