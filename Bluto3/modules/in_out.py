#!/usr/local/bin/python


import traceback
import os
import collections
import re
import operator

class gather:
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
		except IOError, e:
			print e
		except Exception:
			print traceback.print_exc()
			print('An Unhandled Exception Has Occured, Please Check The Log For Details')
			sys.exit()
		return (lines, line_count)

	def get_subs(self, filename, domain):
		print('Gathering SubDomains')
		full_list = []
		try:
			subs = [line.rstrip('\n') for line in open(filename)]
			for sub in subs:
				full_list.append(str(sub.lower() + "." + domain))
		except Exception:
			print('An Unhandled Exception Has Occured, Please Check The Log For Details' + INFO_LOG_FILE)
			sys.exit()

		print('Completed Gathering SubDomains')
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
		except IOError:
			print 'FileError'
		return top_list


