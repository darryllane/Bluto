import threading
from multiprocessing import Queue
from ..logger_ import error, info, INFO_LOG_FILE, ERROR_LOG_FILE
from .class_calls import linkedIna, Email, dns_gather, zone_transfer, enumerate_subdomains


class MakeThread():
	"""

	MakeThread calls functions from the 'class_calls' module

	Initiates a thread to the function.

	The func_list value must contain must include:

	The function call,
	The function args,
	The function name.

	The function args must contain all relevant args including a queue to place the data into.
	"""

	def __init__(self, func_list, args):
		"""

		"""
		self.func_list = func_list
		self.func_args = args
		

	def unordered_exe(self):
		"""

		"""
		threads = []
		for func in self.func_list:
			self.arg_list = []
			self.func_name = func
			
			
			if self.func_name == 'LinkedInp':
				pass
			else:
				if self.func_name == 'Email':
					self.function = Email
				elif self.func_name == 'Brute':
					self.function = enumerate_subdomains
				
				self.queue = Queue()
				self.arg_list.append((self.func_args,self.queue))
				
				self.thread = threading.Thread(target=self.function, args=(self.arg_list,), name=self.func_name)
				threads.append(self.thread)

		return threads
	
	def order_exe(self):
		
		try:
			threads = []
			for func in self.func_list:
				self.arg_list = []
				self.func_name = func
			
				if self.func_name == 'Dns':
					self.function = dns_gather
				elif self.func_name == 'LinkedIna':
					self.function = linkedIna
				elif self.func_name == 'Zone':
					self.function = zone_transfer				
				
				self.queue = Queue()
				self.arg_list.append((self.func_args,self.queue))
			
				self.thread = threading.Thread(target=self.function, args=(self.arg_list,), name=self.func_name)
				threads.append(self.thread)
		except Exception:
			info('An unhandled exception has occured, please check the \'Error log\' for details')
			error('An Unhandled Exception Has Occured, Please Check The Log For Details' + ERROR_LOG_FILE, exc_info=True)			
		return threads
		
		



