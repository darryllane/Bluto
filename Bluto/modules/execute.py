# -*- coding: utf-8 -*-

from ._wildSanitise import main as wild_main
from .descriptor_ import soa_build
from .in_out import Gather
from .logger_ import info, error
from itertools import chain
from itertools import repeat
from multiprocessing import Queue as Queue
from multiprocessing.dummy import Pool as ThreadPool
from termcolor import colored
from tqdm import *
from.use_age import debug_out
import datetime
import dns.query
import dns.resolver
import dns.zone
import json
import os
import progressbar
import queue as Queue
import random
import re
import socket
import string
import sys
import time
import traceback

global results
results = []

class Dns:
	"""

	DNS STUFF
	
	
	"""

	def __init__(self, args):
		"""

		INIT
		
		"""
		info('dns module init')
		self.args = args[0][0]
		

		#Settings DNS Timout Values
		if not self.args.timeo:
			self.args.timeo = 5
		self.myResolver = dns.resolver.Resolver()
		self.myResolver.timeout = int(self.args.timeo)
		self.myResolver.lifetime = int(self.args.timeo)
		self.myResolver.nameservers = ['8.8.8.8', '8.8.4.4']				
		
		
	
	

	#Gathers Record Types NS, MX
	def records(self):
		info('gathering dns records')
		domain = self.args.domain
		ns_list = []
		zn_list =[]
		mx_list = []
		print("Name Server:\n")
		try:
			myAnswers = self.myResolver.query(self.args.domain, "NS")
			for data in myAnswers.rrset:
				hostname = str(data.target).strip('.')
				answers = self.myResolver.query(hostname)
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
			myAnswers = self.myResolver.query(domain, "MX")
			for data in myAnswers.rrset.items:
				hostname = str(data).split(' ')[1].strip('.')
				answers = self.myResolver.query(hostname)
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
	def domain_check(self):
		try:
			domain = self.args.domain
			myAnswers = self.myResolver.query(domain, "NS")
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
			

	def NoZones(self):
		print (colored('Not Vulnerable To ZoneTransfers', 'green'))
		vuln = '{"vuln":false}'
		vuln = json.loads(vuln)
	
		dump_list = '{"dump":false}'
		dump_list = json.loads(dump_list)
	
		soa_json = '{"soa_json":false}'
		soa_json = json.loads(soa_json)
	
		a = dict(vuln)
		b = dict(dump_list)
		c = dict(soa_json)
		d = dict(a.items() | b.items() | c.items())
		self.args.ZONE_RESULT = d
		return d	
	

	def non_intrusive(self, subdomain):
		try:
			myAnswers = self.myResolver.query(subdomain, raise_on_no_answer=False)
	
			for data in myAnswers:
				results.append(subdomain.lower() + '\t' + str(data))
	
		except ValueError:
			pass
		except dns.resolver.NoNameservers:
			pass
		except dns.resolver.NXDOMAIN:
			pass
		except dns.resolver.NoAnswer:
			pass
		except dns.exception.SyntaxError:
			pass
		except dns.exception.Timeout:
			pass
		except dns.resolver.Timeout:
			pass
		except Exception:
			info('An nnhandled exception has occured, please check the \'Error log\' for details')
			error(traceback.print_exc())
	
	
	def intrusive(self, subdomain):
		try:
			sub, domain = subdomain.split('.', 1)
			soa_answer = self.myResolver.query(domain, 'SOA')
			master_answer = self.myResolver.query(soa_answer[0].mname, 'A')
			soa_address = str(master_answer.response.answer[0]).split(' ')[4]
			default = dns.resolver.get_default_resolver()
			default.nameservers = [soa_address]
	
			nameserver = default.nameservers[0]
			query = dns.message.make_query(subdomain, dns.rdatatype.A)
			response_q = dns.query.udp(query, nameserver, timeout=5)
			rcode = response_q.rcode()
			if rcode == dns.rcode.NOERROR:
				addr = self.myResolver.query(subdomain)
				address = str(addr.rrset[0])
				results.append(subdomain.lower() + '\t' + address)
		except dns.resolver.Timeout:
			pass
		except dns.resolver.NXDOMAIN:
			pass
		except dns.resolver.NoAnswer:
			pass
		except OSError:
			pass
		except Exception:
			info('An nnhandled exception has occured, please check the \'Error log\' for details')
			error(traceback.print_exc())
	
	
	def soa_only(args):
		domain = args.domain
		dump_list = []
	
		try:
			soa_answer = dns.resolver.query(domain, 'SOA')
			info('soa enumerated')
			master_answer = dns.resolver.query(soa_answer[0].mname, 'A')
			if soa_answer.rrset is not None:
	
				pattern= r'(%s)\.\s(\d{1,})\s(\w+)\sSOA\s(.*?)\.\s(.*?)\.\s(\d{1,})\s(\d{1,})\s(\d{1,})\s(\d{1,})\s(\d{1,})' % domain
				match = re.match(pattern, str(soa_answer.rrset))
				m_name, ttl, class_, ns, email, serial, refresh, retry, expiry, minim = match.groups()
				soa_data = (m_name, ttl, class_, ns, str(email).replace('\\', ''), serial, refresh, retry, expiry, minim)				
				print ('\nSOA Details:\n')
				soa_json = soa_build(soa_data)
				soa_json = json.loads(soa_json)
				data = json.dumps(soa_json, indent=6, sort_keys=True)
				print (colored(data, 'blue'))
		except Exception:
			print(traceback.print_exc())
			info('An unhandled exception has occured, please check the \'Error log\' for details')
			error('An Unhandled Exception Has Occured, Please Check The Log For Details', exc_info=True)  			
		
		
	def zone(self):
		print ('\nZoneTranfer Check:\n')
		domain = self.args.domain
		dump_list = []
	
		try:
			soa_answer = dns.resolver.query(domain, 'SOA')
			info('soa enumerated')
			master_answer = dns.resolver.query(soa_answer[0].mname, 'A')
			if soa_answer.rrset is not None:
	
				pattern= r'(%s)\.\s(\d{1,})\s(\w+)\sSOA\s(.*?)\.\s(.*?)\.\s(\d{1,})\s(\d{1,})\s(\d{1,})\s(\d{1,})\s(\d{1,})' % domain
				match = re.match(pattern, str(soa_answer.rrset))
				m_name, ttl, class_, ns, email, serial, refresh, retry, expiry, minim = match.groups()
				soa_data = (m_name, ttl, class_, ns, str(email).replace('\\', ''), serial, refresh, retry, expiry, minim)
				z = dns.zone.from_xfr(dns.query.xfr(ns, domain, timeout=10, lifetime=10))
				vuln = '{"vuln":true}'
				info('vulnerable to zone transfers: {}'.format(soa_answer))
				names = list(z.nodes.keys())
				names.sort()
				info('zone dump')
				for n in names:
					try:
						data1 = "{}.{}" .format(n,domain)	
						addr = socket.gethostbyname(data1)
						info("{}.{}\t{}" .format(n, domain, addr))			
						dump_list.append("{}.{}\t{}" .format(n, domain, addr))
					except socket.gaierror as e:
						continue
					except dns.resolver.NoAnswer:
						continue
					except dns.resolver.NXDOMAIN:
						continue
					except Exception:
						info('An nnhandled exception has occured, please check the \'Error log\' for details')
						error(traceback.print_exc())
			if vuln == '{"vuln":true}':
				d = {}
				_dump = sorted(set(dump_list))
				clean_dump = {'dump': dict(item.split("\t",1) for item in _dump) }
				vuln = json.loads(vuln)
				soa_json = soa_build(soa_data)
				soa_json = json.loads(soa_json)
				a = dict(vuln)
				b = dict(clean_dump)
				c = dict(soa_json)
				d.update(a)
				d.update(b)
				d.update(c)
				print (colored('\nVulnerable To ZoneTransfers:\n\n{}'.format(ns), 'red'))
				self.args.ZONE_RESULT = d
				return d
	
		except dns.resolver.NoNameservers:
			pass
		except EOFError:
			d = self.NoZones()
			return d
		except dns.resolver.NoAnswer:
			pass
		except dns.resolver.NXDOMAIN:
			pass
		except dns.exception.Timeout:
			pass
		except ConnectionResetError:
			d = self.NoZones()
			return d
		except (socket.error, dns.exception.FormError) as e:
			d = self.NoZones()
			return d
		except Exception:
			info('An unhandled exception has occured, please check the \'Error log\' for details')
			error(traceback.print_exc())
			d = NoZones()
			return d
			
	
	def _byteify(self, data, ignore_dicts = False):
		# if this is a unicode string, return its string representation
		if isinstance(data, str):
			return data.encode('utf-8')
		# if this is a list of values, return list of byteified values
		if isinstance(data, list):
			return [ self._byteify(item.decode("utf-8"), ignore_dicts=True) for item  in data ]
		# if this is a dictionary, return dictionary of byteified keys and values
		# but only if we haven't already byteified it
		if isinstance(data, dict) and not ignore_dicts:
			return {
				self._byteify(key, ignore_dicts=True): self._byteify(value, ignore_dicts=True)
				for key, value in data.items()
			}
		# if it's anything else, return it in its original form
		return data
	
	
	def json_loads_byteified(self, json_text):
		return self._byteify(
			json.loads(json_text, object_hook=self._byteify),
			ignore_dicts=True
		)
	
	def wild_check(self):
		info('checking wild cards')
		print ('\nWild Card Check:')
		domain = self.args.domain
		while True:
			try:
				one = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
				myAnswers = self.myResolver.query(str(one) + '.' + str(domain))
	
			except dns.resolver.Timeout:
				info('Timed Out')
				print('\nTimeout...trying again')
	
			except dns.resolver.NoNameservers:
				pass
			except dns.resolver.NoAnswer:
				pass
			except dns.resolver.NXDOMAIN:
				info('wild cards false')
				print (colored('\nWild Cards False!', 'red'))
				return {'wild': False}
			except Exception:
				info('An nnhandled exception has occured, please check the \'Error log\' for details')
				error(traceback.print_exc())
			else:
				info('wild cards true')
				print (colored('\nWild Cards True!','green'))
				return {'wild': True}
	
	def start_brute(self, subdomain):
		global brute_q
		time.sleep(0.1)
		if self.args.intrusive:
			self.intrusive(subdomain)
		else:
			self.non_intrusive(subdomain)
	
		return
	
	
	def _brute(self):
		global results
		sub_joined = []
		data_ = Gather()
		domain = self.args.domain
		topValue = self.args.top
		
		fileObj = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../doc/Subdomains-Raw.txt'))
		if not self.args.ZONE_RESULT:
			self.zone()
		if self.args.ZONE_RESULT['vuln']:
			d = self.zone()
			z_data = json.dumps(d)
			z_data = json.loads(z_data)
			vuln = z_data["vuln"]
			if d is None:
				print ('ZoneTransfer Checks Failed, Try again')
				sys.exit()					

				print (colored('\n\nOutput To HTML Module', 'magenta', attrs=['blink']))
				data = json.dumps(d, indent=6, sort_keys=True)
				print (colored(data, 'blue'))
				return d
		else:				
			if self.args.top:
	
				subdomains = data_.top_list(fileObj, self.args)
				joined_subs = [sub + '.' + domain for sub in subdomains]
				if self.args.debug:
					print (colored('Debug Enabled:','red', 'on_yellow'))
					print (colored('SubDomains Output', 'red', 'on_yellow'))
					debug_out(subdomains)
	
			else:
				self.args.top = '1000'
				subdomains = data_.top_list(fileObj, self.args)
				joined_subs = [sub + '.' + domain for sub in subdomains]
				if self.args.debug:
					print (colored('Debug Enabled:','red', 'on_yellow'))
					print (colored('SubDomains Output', 'red', 'on_yellow'))
					debug_out(subdomains)
					
			info('top {} subs selected'.format(self.args.top))
			start_time_total = time.time()
			wild = self.wild_check()
			print ('\nBrute-Forcing Top {} Subdomains:\n'.format(len(subdomains)))
			if self.args.intrusive:
				print (colored('Intrusive Mode Enabled!', 'yellow'))
			pool = ThreadPool(processes=100)
			max_ = len(joined_subs)
			with tqdm(total=max_) as pbar:
				for i, _ in tqdm(enumerate(pool.imap_unordered(self.start_brute, joined_subs))):
					pbar.update()
			
			if str(wild) == "{'wild': True}":
				results = wild_main(results, self.args)
			time_spent_total = time.time() - start_time_total
			time_spent_total_f = str(datetime.timedelta(seconds=(time_spent_total))).split('.')[0]
	
			results_f = sorted(list(set(results)))
			results_f = {"hosts": dict(item.split("\t",1) for item in results_f) }
	
			wild = self._byteify(wild)
			a = '{{"brute":"{}"}}'.format(time_spent_total_f)
			time_spent_total_f = self.json_loads_byteified(a)
	
			b = dict(time_spent_total_f)
			c = dict(wild)
	
			d = dict(chain(results_f.items(), b.items(), c.items()))
	
			d = self.convert(d)
			# FROM HERE OUTPUT IS RETURN TO MAIN THREAD
			print (colored('\n\nOutput To HTML Module', 'magenta', attrs=['blink']))
			data = json.dumps(d, indent=6, sort_keys=True)
			print (colored(data, 'blue'))
			
			
	
	
	def bluto_use(self):
		now = datetime.datetime.now()
		try:
			link = "https://darryllane.co.uk/bluto/log_use.php"
			payload = {'country': self.countryID, 'Date': now}
			requests.post(link, data=payload)
		except Exception:
			info('An Unhandled Exception Has Occured, Please Check The Log For Details' + INFO_LOG_FILE)
			pass
		
	
	def convert(self, data):
		if isinstance(data, bytes):  return data.decode('ascii')
		if isinstance(data, dict):   return dict(map(self.convert, data.items()))
		if isinstance(data, tuple):  return map(self.convert, data)
		return data		