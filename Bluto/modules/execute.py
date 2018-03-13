from multiprocessing import Queue as Queue
from itertools import repeat
from termcolor import colored
from itertools import chain
import progressbar
import re
import os
import sys
import random
import traceback
import string
import json
import socket
import dns.resolver
import dns.query
import dns.zone
import queue as Queue
from multiprocessing.dummy import Pool as ThreadPool
from .resolve import _set
from tqdm import *
import time
import datetime
from .in_out import gather
from .logger_ import info
from .descriptor_ import soa_build
from ._wildSanitise import main as wild_main

from.use_age import debug_out

global results
results = []


def NoZones():
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
	return d	


def convert(data):
	if isinstance(data, bytes):  return data.decode('ascii')
	if isinstance(data, dict):   return dict(map(convert, data.items()))
	if isinstance(data, tuple):  return map(convert, data)
	return data


def non_intrusive(subdomain, my_resolver):
	try:
		myAnswers = my_resolver.query(subdomain, raise_on_no_answer=False)

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
		info('An Unhandled Exception Has Occured, Please Check The Log For Details')
		info(traceback.print_exc())


def intrusive(subdomain, my_resolver):
	try:
		sub, domain = subdomain.split('.', 1)
		soa_answer = my_resolver.query(domain, 'SOA')
		master_answer = my_resolver.query(soa_answer[0].mname, 'A')
		soa_address = str(master_answer.response.answer[0]).split(' ')[4]
		default = dns.resolver.get_default_resolver()
		default.nameservers = [soa_address]

		nameserver = default.nameservers[0]
		query = dns.message.make_query(subdomain, dns.rdatatype.A)
		response_q = dns.query.udp(query, nameserver, timeout=5)
		rcode = response_q.rcode()
		if rcode == dns.rcode.NOERROR:
			addr = my_resolver.query(subdomain)
			address = str(addr.rrset[0])
			results.append(subdomain.lower() + '\t' + address)
	except dns.resolver.Timeout:
		pass
	except dns.resolver.NXDOMAIN:
		pass
	except dns.resolver.NoAnswer:
		pass
	except Exception:
		info('An Unhandled Exception Has Occured, Please Check The Log For Details')
		info(traceback.print_exc())


def zone_trans(args):
	print ('\nZoneTranfer Check:\n')
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
			z = dns.zone.from_xfr(dns.query.xfr(ns, domain, timeout=10, lifetime=10))
			vuln = '{"vuln":true}'
			info('vulnerable to zone transfers: {}'.format(soa_answer))
			names = list(z.nodes.keys())
			names.sort()
			info('zone dump')
			for n in names:
				try:
					info("{}.{}\t{}" .format(n, domain, addr))
					data1 = "{}.{}" .format(n,domain)
					addr = socket.gethostbyname(data1)
					dump_list.append("{}.{}\t{}" .format(n, domain, addr))
				except socket.gaierror as e:
					continue
				except dns.resolver.NoAnswer:
					continue
				except dns.resolver.NXDOMAIN:
					continue
				except Exception as e:
					print (traceback.print_exc())
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
			return d

	except dns.resolver.NoNameservers:
		pass
	except EOFError:
		d = NoZones()
		return d
	except dns.resolver.NoAnswer:
		pass
	except dns.resolver.NXDOMAIN:
		pass
	except dns.exception.Timeout:
		pass
	except ConnectionResetError:
		d = NoZones()
		return d
	except (socket.error, dns.exception.FormError) as e:
		d = NoZones()
		return d
	except Exception as e:
		info('An Unhandled Exception Has Occured, Please Check The Log For Details')
		info(traceback.print_exc())
		d = NoZones()
		return d
		

def _byteify(data, ignore_dicts = False):
	# if this is a unicode string, return its string representation
	if isinstance(data, str):
		return data.encode('utf-8')
	# if this is a list of values, return list of byteified values
	if isinstance(data, list):
		return [ _byteify(item.decode("utf-8"), ignore_dicts=True) for item  in data ]
	# if this is a dictionary, return dictionary of byteified keys and values
	# but only if we haven't already byteified it
	if isinstance(data, dict) and not ignore_dicts:
		return {
			_byteify(key, ignore_dicts=True): _byteify(value, ignore_dicts=True)
			for key, value in data.items()
		}
	# if it's anything else, return it in its original form
	return data


def json_loads_byteified(json_text):
	return _byteify(
		json.loads(json_text, object_hook=_byteify),
		ignore_dicts=True
	)

def wild_check(args):
	info('checking wild cards')
	print ('\nWild Card Check:')
	domain = args.domain
	while True:
		try:
			my_resolver = _set(args)
			one = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
			myAnswers = my_resolver.query(str(one) + '.' + str(domain))

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
		except Exception as e:
			print (e)
		else:
			info('wild cards true')
			print (colored('\nWild Cards True!','green'))
			return {'wild': True}

def start_brute(subdomain):

	global job_args
	global brute_q
	my_resolver = _set(job_args)
	time.sleep(0.1)
	if job_args.intrusive:
		intrusive(subdomain, my_resolver)
	else:
		non_intrusive(subdomain, my_resolver)

	return


def _brute(job_arg_in):
	global job_args
	global results
	sub_joined = []
	job_args = job_arg_in
	data_ = gather()
	domain = job_arg_in.domain
	topValue = job_arg_in.top
	d = zone_trans(job_args)
	fileObj = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../doc/Subdomains-Raw.txt'))
	if d is None:
		print ('ZoneTransfer Checks Failed, Try again')
		sys.exit()
	z_data = json.dumps(d)
	z_data = json.loads(z_data)
	vuln = z_data["vuln"]

	if not vuln:

		if job_arg_in.top:

			subdomains = data_.top_list(fileObj, job_args)
			joined_subs = [sub + '.' + domain for sub in subdomains]
			if job_args.debug:
				print (colored('Debug Enabled:','red', 'on_yellow'))
				print (colored('SubDomains Output', 'red', 'on_yellow'))
				debug_out(subdomains)

		else:
			job_args.top = '1000'
			subdomains = data_.top_list(fileObj, job_args)
			joined_subs = [sub + '.' + domain for sub in subdomains]
			if job_args.debug:
				print (colored('Debug Enabled:','red', 'on_yellow'))
				print (colored('SubDomains Output', 'red', 'on_yellow'))
				debug_out(subdomains)
		info('top {} subs selected'.format(job_args.top))
		start_time_total = time.time()
		wild = wild_check(job_args)
		print ('\nBrute-Forcing Top {} Subdomains:\n'.format(len(subdomains)))
		if job_args.intrusive:
			print (colored('Intrusive Mode Enabled!', 'yellow'))
		pool = ThreadPool(processes=100)
		max_ = len(joined_subs)
		with tqdm(total=max_) as pbar:
			for i, _ in tqdm(enumerate(pool.imap_unordered(start_brute, joined_subs))):
				pbar.update()
		
		if str(wild) == "{'wild': True}":
			results = wild_main(results, job_args)
		time_spent_total = time.time() - start_time_total
		time_spent_total_f = str(datetime.timedelta(seconds=(time_spent_total))).split('.')[0]

		results_f = sorted(list(set(results)))
		results_f = {"hosts": dict(item.split("\t",1) for item in results_f) }

		wild = _byteify(wild)
		a = '{{"brute":"{}"}}'.format(time_spent_total_f)
		time_spent_total_f = json_loads_byteified(a)

		b = dict(time_spent_total_f)
		c = dict(wild)

		d = dict(chain(results_f.items(), b.items(), c.items()))

		d = convert(d)
		#FROM HERE OUTPUT IS RETURN TO MAIN THREAD
		output = json.dumps(str(d))
		parsed = json.loads(output)
		print (colored('\n\nOutput To HTML Module', 'magenta', attrs=['blink']))
		data = json.dumps(parsed, indent=4, sort_keys=True)
		print (colored(data, 'blue'))

	else:
		output = json.dumps(d)
		parsed = json.loads(output)
		print (colored('\n\nOutput To HTML Module', 'magenta', attrs=['blink']))
		data = json.dumps(parsed, indent=4, sort_keys=True)
		print (colored(data, 'blue'))
		return d
