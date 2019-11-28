from ..email_ import Search
from ..execute import Dns
from ..html_report import write_html
from ..logger_ import info, error, INFO_LOG_FILE, ERROR_LOG_FILE
from ..html_report_BETA import Report, ReportDns
from ..tempalte_report import StaffEnumeration
from .linkedin_class import FindPeople 
from termcolor import colored
from bs4 import BeautifulSoup
import threading
import json
import traceback
import requests


def linkedIna(params):
	print ('\nActive LinkedIn Check:\n')
	info('active linkedin initialised')
	args = params[0][0]
	q1 = params[0][1]
	people = []
	obj = FindPeople(args, page_limits='2:20', company_details='', company='', company_number='', type_='linkedIna')
	
	obj.company()
	obj.people()
	
	results = obj.output.get()
	#results = [('name:Nigel Emmerson', 'role:IT Release Coordinator', 'location:Canterbury, United Kingdom', 'image:https://media.licdn.com/dms/image/C4D03AQFf0vmHuMI-Jg/profile-displayphoto-shrink_100_100/0?e=1576108800&amp;v=beta&amp;t=XvI7P1OhTyjbGOpb6nFpRCGq171ZNTN0s4E-MdyBD0U', 'email:none', 'confirmed: False', 'pwn_data:[]'), ('name:Bilal Nasir', 'role:Systems Consultant at Saga plc.', 'location:Canterbury, United Kingdom', 'image:https://media.licdn.com/dms/image/C4D03AQEUln5oa_C4yw/profile-displayphoto-shrink_100_100/0?e=1576108800&amp;v=beta&amp;t=NG-hcHHlha6a_aZ-DRezl3wmz6fjgoEHF3hm_fYwLsE', 'email:none', 'confirmed: False', 'pwn_data:[]'), ('name:Chris Butterworth', 'role:Web Designer', 'location:Canterbury, United Kingdom', 'image:https://media.licdn.com/dms/image/C4E03AQHW-faaMcsKAA/profile-displayphoto-shrink_100_100/0?e=1576108800&amp;v=beta&amp;t=qh-Gjn0WzbFg-228K4wbC20wGH7M8M_bbGEQcqb8SI8', 'email:none', 'confirmed: False', 'pwn_data:[]'), ('name:Matt Isaacs', 'role:IT Group Applications Team Manager at Saga plc.', 'location:Canterbury, United Kingdom', 'image:https://media.licdn.com/dms/image/C5103AQEafknnRU7Kvg/profile-displayphoto-shrink_100_100/0?e=1576108800&amp;v=beta&amp;t=Q6q6JL30NN4fTFf40sM-6SVWO7Lhi2YemaCN8Z9KNjk', 'email:none', 'confirmed: False', 'pwn_data:[]'), ('name:Lucy Weller', 'role:Customer Service & Team Management | Claims and Insurance | IT | Technically Proficient | Problem Solver | Business Minded', 'location:Canterbury, United Kingdom', 'image:None', 'email:none', 'confirmed: False', 'pwn_data:[]'), ('name:Nicholas Brett', 'role:Speech Analytics at Saga Group Ltd.', 'location:Canterbury, United Kingdom', 'image:https://media.licdn.com/dms/image/C4E03AQFVsgYl17PxLw/profile-displayphoto-shrink_100_100/0?e=1576108800&amp;v=beta&amp;t=P8rkKJcdcMq-k9Lrf70ciqgBJS1UJ4gTgkVB-xpwZag', 'email:none', 'confirmed: False', 'pwn_data:[]'), ('name:Ryan Bond', 'role:Desktop Support Engineer at Saga plc.', 'location:Canterbury, United Kingdom', 'image:https://media.licdn.com/dms/image/C5603AQHOq7mlpEEE3g/profile-displayphoto-shrink_100_100/0?e=1576108800&amp;v=beta&amp;t=ecFcEiH8BMUcKERTBqoMmrvT7d1Hw3K45s4HE2NaxgU', 'email:none', 'confirmed: False', 'pwn_data:[]'), ('name:Teresa Sutton', 'role:Senior IT Project Manager at SAGA', 'location:Canterbury, United Kingdom', 'image:None', 'email:none', 'confirmed: False', 'pwn_data:[]'), ('name:Glenn Goslin', 'role:Software Consultant at SAGA', 'location:Canterbury, United Kingdom', 'image:None', 'email:none', 'confirmed: False', 'pwn_data:[]'), ('name:Kester Hackney', 'role:Front End Developer', 'location:Canterbury, United Kingdom', 'image:https://media.licdn.com/dms/image/C5603AQFumkBtE8pwtQ/profile-displayphoto-shrink_100_100/0?e=1576108800&amp;v=beta&amp;t=U-YI8uv-MkHm4W45Rwjva4OIxEz3W9fi9Nd_Db9B22o', 'email:none', 'confirmed: False', 'pwn_data:[]'), ('name:Tim Firkins', 'role:Group Voice and Information Technologies at Saga Group Ltd.', 'location:Canterbury, United Kingdom', 'image:https://media.licdn.com/dms/image/C4D03AQHtrzgju1714g/profile-displayphoto-shrink_100_100/0?e=1576108800&amp;v=beta&amp;t=coliqytO8i4cspnDrWp5bvIRZetDOMUwjSAZIUTXqWg', 'email:none', 'confirmed: False', 'pwn_data:[]'), ('name:Robert Roberts', 'role:Underwriting Agent at SAGA', 'location:Canterbury, United Kingdom', 'image:None', 'email:none', 'confirmed: False', 'pwn_data:[]'), ('name:Stephen Gray', 'role:Group Programme Manager at SAGA', 'location:United Kingdom', 'image:https://media.licdn.com/dms/image/C4D03AQERKO1C7GByVw/profile-displayphoto-shrink_100_100/0?e=1576108800&amp;v=beta&amp;t=M3WXyCzB_V-sHiEv60FQO4-c8kCcmIzhR45sGeIGYV0', 'email:none', 'confirmed: False', 'pwn_data:[]'), ('name:Rob Huish', 'role:at', 'location:Canterbury, United Kingdom', 'image:None', 'email:none', 'confirmed: False', 'pwn_data:[]'), ('name:Arti Singh', 'role:Systems Consultant at Saga Group Ltd.', 'location:Canterbury, United Kingdom', 'image:None', 'email:none', 'confirmed: False', 'pwn_data:[]'), ('name:Paul Harrison', 'role:Sales And Service Executive. SOS Personal Alarm Systems at Saga plc.', 'location:Canterbury, United Kingdom', 'image:https://media.licdn.com/dms/image/C4D03AQEKXt3wqksBnQ/profile-displayphoto-shrink_100_100/0?e=1576108800&amp;v=beta&amp;t=29YZFmE48MKiRxQiMQTRW0lpxTcx0LGPDGP7GoHqnIU', 'email:none', 'confirmed: False', 'pwn_data:[]'), ('name:Sarah Mosley', 'role:Wintel Infrastructure Engineer at Saga plc.', 'location:Canterbury, United Kingdom', 'image:None', 'email:none', 'confirmed: False', 'pwn_data:[]'), ('name:Dawn Atkins', 'role:Assistant Product Manager - Health and Travel Insurance at Saga Group Ltd.', 'location:Canterbury, United Kingdom', 'image:None', 'email:none', 'confirmed: False', 'pwn_data:[]')]

	try:
		
		if results:
			for tup in results:
				tempDict = {}
				for elem in tup:
					elem = elem.split(":", 1)
					tempDict.update({elem[0]:elem[1]})
				people.append(tempDict)
			people = {'person':people}
			
			
			# REPORTING MODULES
			StaffEnumeration(people, args)
			#make_report.staff_enumeration()					
			#make_report = Report(people, args)
			#make_report.staff_enumeration()
			
			if args.debug:
				print (colored('\n\nOutput To HTML Module', 'magenta', attrs=['blink']))
				data = json.dumps(people, indent=6, sort_keys=True)
				print (colored(data, 'blue'))
			
			q1.put(people)
			
	except Exception as e_rror:
		if args.debug:
			print(e_rror.args)
			print(traceback.print_exc())
		info('An unhandled exception has occured, please check the \'Error log\' for details')
		error('An Unhandled Exception Has Occured, Please Check The Log For Details' + ERROR_LOG_FILE, exc_info=True)	
				


def linkedInp(params):
	args = params[0][0]
	print ('\nPassive LinkedIn Check:\n')
	info('passive linkedin initialised')
	entries_tuples = []
	seen = set()
	results = []
	who_error = False
	people_details = []
	confirmed_email = []
	people = []
	
	obj = FindPeople(args, page_limits='2:20', company_details='', company='', company_number='', type_='linkedInp')
	obj.linkedin_pa()
	results = obj.output.get()
	#results = [('name:Nigel Emmerson', 'role:IT Release Coordinator', 'location:Canterbury, United Kingdom', 'image:https://media.licdn.com/dms/image/C4D03AQFf0vmHuMI-Jg/profile-displayphoto-shrink_100_100/0?e=1576108800&amp;v=beta&amp;t=XvI7P1OhTyjbGOpb6nFpRCGq171ZNTN0s4E-MdyBD0U', 'email:none', 'confirmed: False', 'pwn_data:[]'), ('name:Bilal Nasir', 'role:Systems Consultant at Saga plc.', 'location:Canterbury, United Kingdom', 'image:https://media.licdn.com/dms/image/C4D03AQEUln5oa_C4yw/profile-displayphoto-shrink_100_100/0?e=1576108800&amp;v=beta&amp;t=NG-hcHHlha6a_aZ-DRezl3wmz6fjgoEHF3hm_fYwLsE', 'email:none', 'confirmed: False', 'pwn_data:[]'), ('name:Chris Butterworth', 'role:Web Designer', 'location:Canterbury, United Kingdom', 'image:https://media.licdn.com/dms/image/C4E03AQHW-faaMcsKAA/profile-displayphoto-shrink_100_100/0?e=1576108800&amp;v=beta&amp;t=qh-Gjn0WzbFg-228K4wbC20wGH7M8M_bbGEQcqb8SI8', 'email:none', 'confirmed: False', 'pwn_data:[]'), ('name:Matt Isaacs', 'role:IT Group Applications Team Manager at Saga plc.', 'location:Canterbury, United Kingdom', 'image:https://media.licdn.com/dms/image/C5103AQEafknnRU7Kvg/profile-displayphoto-shrink_100_100/0?e=1576108800&amp;v=beta&amp;t=Q6q6JL30NN4fTFf40sM-6SVWO7Lhi2YemaCN8Z9KNjk', 'email:none', 'confirmed: False', 'pwn_data:[]'), ('name:Lucy Weller', 'role:Customer Service & Team Management | Claims and Insurance | IT | Technically Proficient | Problem Solver | Business Minded', 'location:Canterbury, United Kingdom', 'image:None', 'email:none', 'confirmed: False', 'pwn_data:[]'), ('name:Nicholas Brett', 'role:Speech Analytics at Saga Group Ltd.', 'location:Canterbury, United Kingdom', 'image:https://media.licdn.com/dms/image/C4E03AQFVsgYl17PxLw/profile-displayphoto-shrink_100_100/0?e=1576108800&amp;v=beta&amp;t=P8rkKJcdcMq-k9Lrf70ciqgBJS1UJ4gTgkVB-xpwZag', 'email:none', 'confirmed: False', 'pwn_data:[]'), ('name:Ryan Bond', 'role:Desktop Support Engineer at Saga plc.', 'location:Canterbury, United Kingdom', 'image:https://media.licdn.com/dms/image/C5603AQHOq7mlpEEE3g/profile-displayphoto-shrink_100_100/0?e=1576108800&amp;v=beta&amp;t=ecFcEiH8BMUcKERTBqoMmrvT7d1Hw3K45s4HE2NaxgU', 'email:none', 'confirmed: False', 'pwn_data:[]'), ('name:Teresa Sutton', 'role:Senior IT Project Manager at SAGA', 'location:Canterbury, United Kingdom', 'image:None', 'email:none', 'confirmed: False', 'pwn_data:[]'), ('name:Glenn Goslin', 'role:Software Consultant at SAGA', 'location:Canterbury, United Kingdom', 'image:None', 'email:none', 'confirmed: False', 'pwn_data:[]'), ('name:Kester Hackney', 'role:Front End Developer', 'location:Canterbury, United Kingdom', 'image:https://media.licdn.com/dms/image/C5603AQFumkBtE8pwtQ/profile-displayphoto-shrink_100_100/0?e=1576108800&amp;v=beta&amp;t=U-YI8uv-MkHm4W45Rwjva4OIxEz3W9fi9Nd_Db9B22o', 'email:none', 'confirmed: False', 'pwn_data:[]'), ('name:Tim Firkins', 'role:Group Voice and Information Technologies at Saga Group Ltd.', 'location:Canterbury, United Kingdom', 'image:https://media.licdn.com/dms/image/C4D03AQHtrzgju1714g/profile-displayphoto-shrink_100_100/0?e=1576108800&amp;v=beta&amp;t=coliqytO8i4cspnDrWp5bvIRZetDOMUwjSAZIUTXqWg', 'email:none', 'confirmed: False', 'pwn_data:[]'), ('name:Robert Roberts', 'role:Underwriting Agent at SAGA', 'location:Canterbury, United Kingdom', 'image:None', 'email:none', 'confirmed: False', 'pwn_data:[]'), ('name:Stephen Gray', 'role:Group Programme Manager at SAGA', 'location:United Kingdom', 'image:https://media.licdn.com/dms/image/C4D03AQERKO1C7GByVw/profile-displayphoto-shrink_100_100/0?e=1576108800&amp;v=beta&amp;t=M3WXyCzB_V-sHiEv60FQO4-c8kCcmIzhR45sGeIGYV0', 'email:none', 'confirmed: False', 'pwn_data:[]'), ('name:Rob Huish', 'role:at', 'location:Canterbury, United Kingdom', 'image:None', 'email:none', 'confirmed: False', 'pwn_data:[]'), ('name:Arti Singh', 'role:Systems Consultant at Saga Group Ltd.', 'location:Canterbury, United Kingdom', 'image:None', 'email:none', 'confirmed: False', 'pwn_data:[]'), ('name:Paul Harrison', 'role:Sales And Service Executive. SOS Personal Alarm Systems at Saga plc.', 'location:Canterbury, United Kingdom', 'image:https://media.licdn.com/dms/image/C4D03AQEKXt3wqksBnQ/profile-displayphoto-shrink_100_100/0?e=1576108800&amp;v=beta&amp;t=29YZFmE48MKiRxQiMQTRW0lpxTcx0LGPDGP7GoHqnIU', 'email:none', 'confirmed: False', 'pwn_data:[]'), ('name:Sarah Mosley', 'role:Wintel Infrastructure Engineer at Saga plc.', 'location:Canterbury, United Kingdom', 'image:None', 'email:none', 'confirmed: False', 'pwn_data:[]'), ('name:Dawn Atkins', 'role:Assistant Product Manager - Health and Travel Insurance at Saga Group Ltd.', 'location:Canterbury, United Kingdom', 'image:None', 'email:none', 'confirmed: False', 'pwn_data:[]')]
	
	
	if results:
		for tup in results:
			tempDict = {}
			for elem in tup:
				elem = elem.split(":", 1)
				tempDict.update({elem[0]:elem[1]})
			people.append(tempDict)
		people = {'person':people}	

		
	StaffEnumeration(people, args)
	info('LinkedInp Search Completed')

		

def Email(args):
	args = args[0][0]
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
		
		
		if args.api:
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
		search.EmailQue.close()
		#search.EmailQue.join_thread()
		
		email_json = merge_dicts(email_list) 
		if args.debug:
			print (colored('\n\nOutput To HTML Module', 'magenta', attrs=['blink']))
			data = json.dumps(email_json, indent=6, sort_keys=True)
			print (colored(data, 'blue'))
		
	except Exception:
		if args[0][0].verbose:
			print('An unhandled exception has occured, please check the \'Error log\' for details')
			print(traceback.print_exc())
		info('An unhandled exception has occured, please check the \'Error log\' for details')
		error('An unhandled exception has occured, please check the \'Error log\' for details', exc_info=1)


def dns_gather(args):
	args = args[0][0]
	obj = Dns(args)
	obj.records()
	results = obj.dns_records_output.get()
	
	if args.debug:
		print (colored('\n\nOutput To HTML Module', 'magenta', attrs=['blink']))
		data = json.dumps(results, indent=6, sort_keys=True)
		print (colored(data, 'blue'))	
	
	
def zone_transfer(args):
	args = args[0][0]
	obj = Dns(args)
	obj.zone()
	results = obj.zone_records_output.get()
	
	if args.debug:
		print (colored('\n\nOutput To HTML Module', 'magenta', attrs=['blink']))
		data = json.dumps(results, indent=6, sort_keys=True)
		print (colored(data, 'blue'))


def enumerate_subdomains(args):
	args = args[0][0]
	obj = Dns(args)
	obj._brute()
	if obj.args.ZONE_RESULT['vuln']:
		results = obj.zone_records_output.get()
	else:
		results = obj.brute_records_output.get()		
	
	if args.debug:
		print (colored('\n\nOutput To HTML Module', 'magenta', attrs=['blink']))
		data = json.dumps(results, indent=6, sort_keys=True)
		print (colored(data, 'blue'))


def action_netcraft(domain, myResolver):
	info('NetCraft Search Started')
	netcraft_list = []
	print("\nPassive Gatherings From NetCraft\n")
	try:
		link = "http://searchdns.netcraft.com/?restriction=site+contains&host=*.{}&lookup=wait..&position=limited" .format (domain)
		response = requests.get(link, verify=False)
		soup = BeautifulSoup(response.content, 'lxml')
		pattern = 'rel="nofollow">([a-z\.\-A-Z0-9]+)<FONT COLOR="#ff0000">'
		sub_results = re.findall(pattern, response.content)
	except dns.exception.Timeout:
		pass
	except Exception:
		info('An Unhandled Exception Has Occured, Please Check The Log For Details\n' + INFO_LOG_FILE, exc_info=True)

	if sub_results:
		for item in sub_results:
			try:
				netcheck = myResolver.query(item + '.' + domain)
				for data in netcheck:
					netcraft_list.append(item + '.' + domain + ' ' + str(data))
					print(colored(item + '.' + domain, 'red'))
			except dns.exception.Timeout:
				pass
			except dns.resolver.NXDOMAIN:
				pass
			except Exception:
				info('An Unhandled Exception Has Occured, Please Check The Log For Details\n' + INFO_LOG_FILE, exc_info=True)
	else:
		print('\tNo Results Found')

	info('NetCraft Completed')
	return netcraft_list