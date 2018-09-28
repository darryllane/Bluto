#!/usr/local/bin/python


import traceback
import os
import collections
import re
import operator
from .logger_ import info, error

class Gather(object):
	
	
	def __init__(self, filename=None, search_results=None, time_spent=None, clean_dump=None, sub_intrest=None, domain=None, report_location=None, company=None, check_count=None, args=None):
		self.search_results = search_results
		self.time_spent = time_spent
		self.clean_dump = clean_dump
		self.sub_intrest = sub_intrest
		self.domain = domain
		self.report_location = report_location
		self.company = company
		self.check_count = check_count
		self.args = args



	def get_file(self, filename):
		try:
			lines = [line.rstrip('\n') for line in open(filename)]
			line_count = sum(1 for line in open(filename))
		except IOError as e:
			print('File not found, exiting')
			info('file not found: {}'.format(filename))
			info(traceback.print_exc())
			sys.exit()
		except Exception:
			print('An unhandled exception has occured, please check the \'Error log\' for details')
			info('An unhandled exception has occured, please check the \'Error log\' for details')
			error(traceback.print_exc())
			sys.exit()
		return (lines, line_count)


	def get_subs(self, filename, domain):
		info('gathering subdomains')
		full_list = []
		try:
			subs = [line.rstrip('\n') for line in open(filename)]
			for sub in subs:
				full_list.append(str(sub.lower() + "." + domain))
		except IOError as e:
			print('File not found, exiting')
			info('file not found: {}'.format(filename))
			error(traceback.print_exc())
			sys.exit()
		except Exception:
			print('An unhandled exception has occured, please check the \'Error log\' for details')
			info('An unhandled exception has occured, please check the \'Error log\' for details')
			error(traceback.print_exc())
			sys.exit()		

		info('completed gathering subdomains')
		return full_list


	def top_list(self, filename, args):
		lines = [line.rstrip('\n') for line in open(filename)]
		topValue = args.top
		dir_path = os.path.dirname(os.path.realpath(__file__))
		words = re.findall('\w+', str(lines))
		data = dict(collections.Counter(words).most_common(int(topValue)))
		sorted_data = sorted(data.items(), key=operator.itemgetter(1), reverse=True)
		top_list = []
		try:
			for row in sorted_data:
				top_list.append(row[0])
		except IOError as e:
			print('File not found, exiting')
			info('file not found: {}'.format(filename))
			error(traceback.print_exc())
			sys.exit()
		except Exception:
			print('An unhandled exception has occured, please check the \'Error log\' for details')
			info('An unhandled exception has occured, please check the \'Error log\' for details')
			error(traceback.print_exc())
			sys.exit()		
			
		return top_list	
