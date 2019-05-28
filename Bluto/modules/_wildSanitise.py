import random
import threading
import string
import dns.resolver
import queue as queue
import traceback
from multiprocessing.dummy import Pool as ThreadPool


def _ramdomGet(myResolver, domain):
	q1 = Queue.Queue()
	random_addrs = []
	try:
		def gather(q1, random_addrs, myResolver):
			one = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
			try:
				myAnswers = myResolver.query(str(one) + '.' + str(domain))
				for item in myAnswers:
					random_addrs.append(str(item))
					q1.put(random_addrs)
			except Exception:
				pass

		for i in range(1,5,1):
			t1 = threading.Thread(target=gather, args=(q1,random_addrs, myResolver))
			t1.start()
		t1.join()
		data = list(set(q1.get()))
	except dns.resolver.Timeout:
		pass
	except dns.resolver.NoNameservers:
		pass
	except dns.resolver.NoAnswer:
		pass
	except dns.resolver.NXDOMAIN:
		pass
	except dns.name.EmptyLabel:
		pass
	except Exception:
		print('An Unhandled Exception Has Occured, Please Check The \'Error\' For Details')
		info('An Unhandled Exception Has Occured, Please Check The \'Error\' For Details')
		error(traceback.print_exc())
	return data


def _wildClean(sub_list, rand_response):
	global target_results
	global rand_response2

	rand_response2 = rand_response
	target_results = []
	q1 = Queue.Queue()
	q1.put(sub_list)

	def worker(host):
		try:
			host_host, host_addr = host.split('\t')
			if host_addr in rand_response2:
				pass
			else:
				target_results.append(host)
		except Exception:
			print('An Unhandled Exception Has Occured, Please Check The \'Error\' For Details')
			info('An Unhandled Exception Has Occured, Please Check The \'Error\' For Details')
			error(traceback.print_exc())
	try:
		while not q1.empty():
			pool = ThreadPool(100)
			pool.map(worker, q1.get())
		pool.close()

	except Exception:
		print('An Unhandled Exception Has Occured, Please Check The \'Error\' For Details')
		info('An Unhandled Exception Has Occured, Please Check The \'Error\' For Details')
		error(traceback.print_exc())

	return target_results

def main(sub_list, job_args):
	
	domain = job_args.domain
	myResolver = Dns._set(job_args)
	rand_response = _ramdomGet(myResolver, domain)
	target_results = _wildClean(sub_list, rand_response)
	return target_results
