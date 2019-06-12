from ..email_ import Search
from ..execute import Dns
from ..html_report import write_html
from ..logger_ import info, error
from .linkedin_class import FindPeople
from termcolor import colored
import threading
import json
import traceback


def linkedIna(params):
	print ('\nActive LinkedIn Check:\n')
	info('active linkedin initialised')
	args = params[0][0]
	q1 = params[0][1]
	people = []
	obj = FindPeople(args, page_limits='10:20', company_details='', company='', company_number='')
	
	obj.company()
	obj.people()
	
	results = obj.output.get()
	try:
		if results:
			for tup in results:
				tempDict = {}
				for elem in tup:
					elem = elem.split(":", 1)
					tempDict.update({elem[0]:elem[1]})
				people.append(tempDict)
			people = {'person':people}
			
			# ADD EMAIL GENERATION FROM RESULTS
			if args.debug:
				print (colored('\n\nOutput To HTML Module', 'magenta', attrs=['blink']))
				data = json.dumps(people, indent=6, sort_keys=True)
				print (colored(data, 'blue'))
				
			write_html(people, obj.company_name, args)
			
			q1.put(people)
			
	except Exception as e_rror:
		if args.debug:
			print(e_rror.args)
			print(traceback.print_exc())
		info('An unhandled exception has occured, please check the \'Error log\' for details')
		error('An Unhandled Exception Has Occured, Please Check The Log For Details' + ERROR_LOG_FILE, exc_info=True)	
		

def Email(args):
	threads = []
	email_list = []
	def merge_dicts(email_list):
		"""
		Given any number of dicts, shallow copy and merge into a new dict,
		precedence goes to key value pairs in latter dicts.
		"""
		seen = []	
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
		
		t1 = threading.Thread(target=search.baidu,)
		t2 = threading.Thread(target=search.exlead,)
		t3 = threading.Thread(target=search.bing,)
		t4 = threading.Thread(target=search.google,)
		
		if args[0][0].api:
			t5 = threading.Thread(target=search.hunter_io)
			threads.append(t5)
		else:
			print(colored('\tDon\'t forget to grab your free API key from "Huter IO" (https://hunter.io/api_keys)\n\n\tYou are likley to find far more results....', 'green'))
		threads.append(t1)
		threads.append(t2)
		threads.append(t3)
		threads.append(t4)
		
		for t in threads:
			t.start()
		
		for t in threads:
			t.join()
	
		
		email_list = search.EmailQue.get()
		email_json = merge_dicts(email_list) 
		
		print (colored(json.dumps(email_json, indent=6, sort_keys=True), 'blue'))
		
	except Exception:
		if args[0][0].verbose:
			print('An unhandled exception has occured, please check the \'Error log\' for details')
			print(traceback.print_exc())
		info('An unhandled exception has occured, please check the \'Error log\' for details')
		error('An unhandled exception has occured, please check the \'Error log\' for details', exc_info=1)


def dns_gather(args):
	obj = Dns(args)
	obj.records()
	
	
def zone_transfer(args):
	obj = Dns(args)
	obj.zone()


def enumerate_subdomains(args):
	obj = Dns(args)
	obj._brute()
	