import threading
from multiprocessing import Queue

from .class_calls import linkedIn

class MakeThread(object):
	"""

	MakeThread calls functions from the 'class_calls' module

	Initiates a thread to the function.

	The func_list value must contain must include:

	The function call,
	The function args,
	The function name.

	The function args must contain all relevant args including a queue to place the data into.
	"""

	def __init__(self, func_list):
		"""

		"""

		for func in func_list:
			self.function = func[0]
			self.func_args = func[1]
			self.func_name = func[0]

	def execute(self):
		"""

		"""
		threads = []
		if self.function.lower() == 'linkedin':
			self.function = linkedIn
			q1 = Queue()
			arg_list = []
			arg_list.append((self.func_args,q1))

			t1 = threading.Thread(target=self.function, args=(arg_list,))
			threads.append(t1)

		return threads



