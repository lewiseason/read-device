import sys
import threading

class ChunkedQueue(object):
	"""
	This class provides basic concurrency with chunked operation.
	Units of work are executed concurrently in batches.

	This module also installs a monkey patch to address a bug in python
	which causes threads to ignore the syshook:
		http://bugs.python.org/issue1230540
	"""

	threads = []

	def __init__(self, max_threads=8):
		self.max_threads = max_threads
		self._install_thread_excepthook()

	def enqueue(self, target, args=(), name=None):
		thread = threading.Thread(target=target, args=args, name=name)
		self.threads.append(thread)

	def execute(self):
		while self.threads:
			if len(self.threads) > self.max_threads:
				# There are too many threads to run them all at once
				chunk = self.threads[0:self.max_threads]
			else:
				chunk = self.threads[:]

			# Start all threads in the chunk
			[ thread.start() for thread in chunk ]

			# Wait for them to finish
			[ thread.join()  for thread in chunk ]

			# And dequeue them
			del(self.threads[0:self.max_threads])

	def _install_thread_excepthook(self):
		# http://bugs.python.org/issue1230540
		old = threading.Thread.run

		def _run(*args, **kwargs):
			try:
				old(*args, **kwargs)
			except:
				sys.excepthook(*sys.exc_info())

		threading.Thread.run = _run


