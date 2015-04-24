import sys
from threading import Thread
from functools import partial

try:
	import queue # Python 3
except ImportError:
	import Queue as queue # Python 2

def Worker(q, blocking=False):
	while True:
		try:
			item = q.get(blocking)
			item()
			q.task_done()
		except queue.Empty:
			break
		except:
			# If an exception is raised, mark the job as done (so that the queue empties instead of hanging forever)
			# And then trigger the exception as normal. This is a bit like a "finally" block, but we don't want to fire
			# if the exception raised was queue.Empty
			q.task_done()
			raise

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
