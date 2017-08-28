from multiprocessing import Queue as Queue
from itertools import repeat
from multiprocessing.dummy import Pool as ThreadPool
from termcolor import colored
import progressbar
import re
import random
import traceback
import string
import json
import socket
import dns.resolver
import dns.query
import dns.zone
import Queue
import resolve
from multiprocessing.dummy import Pool as ThreadPool
import resolve
from tqdm import *
import time
import datetime
from in_out import gather
from logger_ import info
import descriptor_
import _wildSanitise
from use_age import debug_out

global results
results = []


def non_intrusive(subdomain, my_resolver):
	try:
		myAnswers = my_resolver.query(subdomain, raise_on_no_answer=False)

		for data in myAnswers:
			results.append(subdomain.lower() + '\t' + str(data))

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
		print traceback.print_exc()
		print('An Unhandled Exception Has Occured, Please Check The Log For Details')


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
		print traceback.print_exc()


def zone_trans(args):
	print '\nZoneTranfer Check:\n'
	domain = args.domain
	dump_list = []

	try:
		soa_answer = dns.resolver.query(domain, 'SOA')
		master_answer = dns.resolver.query(soa_answer[0].mname, 'A')
		if soa_answer.rrset is not None:

			pattern= r'(%s)\.\s(\d{1,})\s(\w+)\sSOA\s(.*?)\.\s(.*?)\.\s(\d{1,})\s(\d{1,})\s(\d{1,})\s(\d{1,})\s(\d{1,})' % domain
			match = re.match(pattern, str(soa_answer.rrset))
			m_name, ttl, class_, ns, email, serial, refresh, retry, expiry, minim = match.groups()
			soa_data = (m_name, ttl, class_, ns, str(email).replace('\\', ''), serial, refresh, retry, expiry, minim)
			z = dns.zone.from_xfr(dns.query.xfr(ns, domain, timeout=5, lifetime=5))
			vuln = '{"vuln":"true"}'
			names = z.nodes.keys()
			names.sort()
			for n in names:
				try:
					data1 = "{}.{}" .format(n,domain)
					addr = socket.gethostbyname(data1)
					dump_list.append("{}.{}\t{}" .format(n, domain, addr))
				except socket.gaierror,e:
					continue
				except dns.resolver.NoAnswer:
					continue
				except dns.resolver.NXDOMAIN:
					continue
				except Exception,e:
					print traceback.print_exc()
		if vuln == '{"vuln":"true"}':
			_dump = sorted(set(dump_list))

			clean_dump = {'dump': [dict(item.split("\t",1) for item in _dump)] }
			vuln = json.loads(vuln)
			soa_json = descriptor_.soa_build(soa_data)
			soa_json = json.loads(soa_json)
			a = dict(vuln)
			b = dict(clean_dump)
			c = dict(soa_json)
			d = dict(a.items() + b.items() + c.items())
			print colored('\nVulnerable To ZoneTransfers:\t{}'.format(ns), 'red')
			return d

	except dns.resolver.NoNameservers:
		pass
	except dns.resolver.NoAnswer:
		pass
	except dns.resolver.NXDOMAIN:
		pass
	except dns.exception.Timeout:
		pass
	except (socket.error, dns.exception.FormError) as e:
		print colored('Not Vulnerable To ZoneTransfers', 'green')
		vuln = '{"vuln":"false"}'
		vuln = json.loads(vuln)

		dump_list = '{"dump":"false"}'
		dump_list = json.loads(dump_list)

		soa_json = '{"soa_json":"false"}'
		soa_json = json.loads(soa_json)

		a = dict(vuln)
		b = dict(dump_list)
		c = dict(soa_json)
		d = dict(a.items() + b.items() + c.items())
		return d
	except Exception,e:
		print traceback.print_exc()




def _byteify(data, ignore_dicts = False):
	# if this is a unicode string, return its string representation
	if isinstance(data, unicode):
		return data.encode('utf-8')
	# if this is a list of values, return list of byteified values
	if isinstance(data, list):
		return [ _byteify(item, ignore_dicts=True) for item in data ]
	# if this is a dictionary, return dictionary of byteified keys and values
	# but only if we haven't already byteified it
	if isinstance(data, dict) and not ignore_dicts:
		return {
			_byteify(key, ignore_dicts=True): _byteify(value, ignore_dicts=True)
			for key, value in data.iteritems()
		}
	# if it's anything else, return it in its original form
	return data


def json_loads_byteified(json_text):
	return _byteify(
		json.loads(json_text, object_hook=_byteify),
		ignore_dicts=True
	)

def wild_check(args):
	info('Checking Wild Cards')
	print '\nWild Card Check:'
	domain = args.domain
	try:
		my_resolver = resolve._set(args)
		one = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
		myAnswers = my_resolver.query(str(one) + '.' + str(domain))

	except dns.resolver.Timeout:
		pass
	except dns.resolver.NoNameservers:
		pass
	except dns.resolver.NoAnswer:
		pass
	except dns.resolver.NXDOMAIN:
		info('Wild Cards False')
		print colored('\nWild Cards False!', 'red')
		return {'wild': False}
	except Exception,e:
		print e
	else:
		info('Wild Cards True')
		print colored('\nWild Cards True!','green')
		return {'wild': True}

def start_brute(subdomain):

	global job_args
	global brute_q
	my_resolver = resolve._set(job_args)
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
	if d is None:
		print 'ZoneTransfer Checks Failed, Try again'
		sys.exit()
	z_data = json.dumps(d)
	z_data = json.loads(z_data)
	vuln = z_data["vuln"]
	if not 'true' in vuln:

		if job_arg_in.top:
			fileObj = '/Users/laned/Python/Projects/Bluto3/docs/Subdomains-Raw.txt'
			subdomains = data_.top_list(fileObj, job_args)
			joined_subs = [sub + '.' + domain for sub in subdomains]
			if job_args.debug:
				print colored('Debug Enabled:','red', 'on_yellow')
				print colored('SubDomains Output', 'red', 'on_yellow')
				debug_out(subdomains)

		else:
			filename = '/Users/laned/Python/Projects/Bluto3/docs/subdomains-top1mil-20000.txt'
			subdomains = data_.get_subs(filename, domain)
			joined_subs = subdomains

		start_time_total = time.time()
		wild = wild_check(job_args)
		print '\nBrute-Forcing Top {} Subdomains:\n'.format(len(subdomains))
		if job_args.intrusive:
			print colored('Intrusive Mode Enabled!', 'yellow')
		pool = ThreadPool(processes=100)
		max_ = len(joined_subs)
		with tqdm(total=max_) as pbar:
			for i, _ in tqdm(enumerate(pool.imap_unordered(start_brute, joined_subs))):
				pbar.update()

		if str(wild) == "{'wild': True}":
			results = _wildSanitise.main(results, job_args)
		time_spent_total = time.time() - start_time_total
		time_spent_total_f = str(datetime.timedelta(seconds=(time_spent_total))).split('.')[0]

		results_f = sorted(list(set(results)))
		results_f = {'hosts': [dict(item.split("\t",1) for item in results_f)] }

		wild = _byteify(wild)
		a = '{{"brute":"{}"}}'.format(time_spent_total_f)
		time_spent_total_f = json_loads_byteified(a)
		b = dict(time_spent_total_f)
		c = dict(wild)

		d = dict(results_f.items() + b.items() + c.items())
		output = json.dumps(d)
		parsed = json.loads(output)
		print colored('\n\nOutput To HTML Module', 'magenta', attrs=['blink'])
		data = json.dumps(parsed, indent=4, sort_keys=True)
		print colored(data, 'blue')

	else:
		output = json.dumps(d)
		parsed = json.loads(output)
		print colored('\n\nOutput To HTML Module', 'magenta', attrs=['blink'])
		data = json.dumps(parsed, indent=4, sort_keys=True)
		print colored(data, 'blue')
		return d
