import sys
import queue
from threading import Thread
from functools import partial

class Worker(object):

	def __init__(self, queue):
		self.queue = queue

		while True:
			item = self.queue.get()

			try:
				item()
			finally:
				self.queue.task_done()

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
