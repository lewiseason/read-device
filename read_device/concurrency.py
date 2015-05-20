# Copyright 2015 University of Edinburgh
# Licensed under GPLv3 - see README.md for information

import sys
from threading import Thread
from functools import partial

try:
	import queue
except ImportError:
	import Queue as queue # Python 2

def Worker(q, blocking=False):
	"""!
	A worker for concurrency.WorkQueue. Will continue to accept jobs from the
	work queue until none are left. If non-blocking, the worker will then exit
	"""
	while True:
		item = None

		try:
			item = q.get(blocking)
		except queue.Empty:
			return

		try:
			item()
		except:
			# This perhaps isn't always the best thing to do.
			sys.excepthook(*sys.exc_info())
		finally:
			q.task_done()

class WorkQueue(object):
	def __init__(self, concurrency=3):
		self.queue = queue.Queue()
		self.workers = [ Thread(target=Worker, args=(self.queue,)) for _ in range(concurrency) ]

	def append(self, target, args=()):
		task = partial(target, *args)
		self.queue.put(task)

	def execute(self):
		for w in self.workers:
			w.daemon = True
			w.start()

		self.queue.join()

	def __len__(self):
		return self.queue.qsize()
