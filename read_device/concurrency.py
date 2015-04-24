import sys
from threading import Thread
from functools import partial

try:
	import queue
except ImportError:
	import Queue as queue

class Worker(object):

	def __init__(self, q, blocking=False):
		self.queue = q

		while True:
			try:
				item = self.queue.get(blocking)
				item()
				self.queue.task_done()
			except queue.Empty:
				break

class WorkQueue(object):
	def __init__(self, concurrency=3):
		self.queue = queue.Queue()
		self.workers = [ Thread(target=Worker, args=(self.queue,)) for _ in range(concurrency) ]

	def append(self, target, args=[]):
		task = partial(target, *args)
		self.queue.put(task)

	def execute(self):
		for w in self.workers:
			w.daemon = True
			w.start()

		self.queue.join()

	def __len__(self):
		return self.queue.qsize()
