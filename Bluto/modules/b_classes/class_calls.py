from ..email_ import Search
from ..execute import Dns
from ..html_report import write_html
from ..logger_ import info, error
from .linkedin_class import FindPeople
from termcolor import colored
import threading
import json
import traceback

global threads
threads = []

def linkedIna(params):
	print ('\nActive LinkedIn Check:\n')
	info('active linkedin initialised')
	args = params[0][0]
	q1 = params[0][1]
	people = []
	obj = FindPeople(args, page_limits='5:10', company_details='', company='', company_number='')
	obj.company()
	obj.people()
	results = obj.output.get()

	if results:
		for tup in results:
			tempDict = {}
			for elem in tup:
				elem = elem.split(":", 1)
				tempDict.update({elem[0]:elem[1]})
			people.append(tempDict)
		people = {'person':people}
		write_html(people, 'company name', args)
		print (colored('\n\nOutput To HTML Module', 'magenta', attrs=['blink']))
		data = json.dumps(people, indent=6, sort_keys=True)
		print (colored(data, 'blue'))
		q1.put(people)

	else:
		print('No Data')
		

def Email(args):
	
	email_list = []
	def merge_dicts(email_list):
		seen = []
		diction = {'email':[]}
		"""
		Given any number of dicts, shallow copy and merge into a new dict,
		precedence goes to key value pairs in latter dicts.
		"""
		result = {'email':[]}
		fields = ['url', 'address']
		email_list = [dict(zip(fields, d)) for d in email_list]
		for item in email_list:
			if item in seen:
				pass
			else:
				seen.append(item)
		for value in seen :
			result['email'].append(value)			
		
		result['count'] = len(result['email'])
		
		return result
	
	try:

		search = Search(args)
		print ("\nGathering Email Addresses:\n")
		
	
		def worker(engine):
			
			if engine == 'baidu':
				baidu_stash = search.baidu()
			elif engine == 'exlead':
				exlead_stash = search.exlead()
			elif engine == 'bing':
				bing_stash = search.bing()
			elif engine == 'google':
				google_stash = search.google()
						
							
		engines = ['baidu', 'google', 'bing', 'exlead']
		
		for engine in engines:
			thread = threading.Thread(target=worker, args=(engine,))
			threads.append(thread)
			thread.start()
			thread.join()
			
		
		
			
		email_list = bing_stash + baidu_stash + exlead_stash + google_stash
		email_json = merge_dicts(email_list) 
		
		print (colored(json.dumps(email_json, indent=6, sort_keys=True), 'blue'))
		
	except Exception:
		print(traceback.print_exc())
		print('An unhandled exception has occured, please check the \'Error log\' for details')
		info('An unhandled exception has occured, please check the \'Error log\' for details')
		error(traceback.print_exc())


def dns_gather(args):
	obj = Dns(args)
	obj.records()
	
	
def zone_transfer(args):
	obj = Dns(args)
	obj.zone()


def enumerate_subdomains(args):
	obj = Dns(args)
	obj._brute()
	