import threading
import click

import sys
import time
import functools
import collections

class requires_configuration(object):
		"""
		Use this decorator on device subclass methods
		which require the configure() method to have been
		run at least once beforehand.
		"""

		def __init__(self, func):
				self.func = func

		def __get__(self, obj, type=None):
				return self.__class__(self.func.__get__(obj, type))

		def __call__(self, *args, **kwargs):
			@functools.wraps(self.func)
			def wrap(*args, **kwargs):
				self.execute(*args, **kwargs)

			return wrap(*args, **kwargs)

		def execute(self, *args, **kwargs):
			profile = self.func.__self__
			if not profile.configured:
				profile.configure()
				profile.configured = True

			return self.func(*args, **kwargs)

class attempts(object):
	"""
	A decorator which will attempt to run the decorated function. If it fails with
	any of the specified exceptions, it will be reattempted (up to a maximum number
	of attempts as specified). It is also possible to specify a delay between
	attempts.

		@attempts(3, 1, KeyError)
		def f(self, x):
			# ...

	If f raises a KeyError, the decorator will try again after 1 second, for up
	to 3 attempts in total.

	If a KeyError is raised on the 3rd attempt, the original exception will be
	re-raised in the normal way.
	"""

	def __init__(self, attempts=3, delay=0, *exceptions):
		self.max_attempts = attempts
		self.delay        = delay
		self.exceptions   = exceptions

	def __call__(self, func):
		@functools.wraps(func)
		def wrap(target, *args, **kwargs):
			self.attempt(target, func, *args, **kwargs)

		return wrap

	def attempt(self, target, func, *args, **kwargs):
		for step in range(self.max_attempts):
			try:
				return func(target, *args, **kwargs)

			except self.exceptions:
				if (step + 1) >= self.max_attempts:
					# Failed too many times - no more attempts
					raise

				# Otherwise We've failed less than max_attempts times
				# Wait and try again
				time.sleep(self.delay)

class cached(object):
	"""
	Cache a property value instead of re-evaluating it every time.

	https://wiki.python.org/moin/PythonDecoratorLibrary#Memoize
	"""

	def __init__(self, func):
		self.func  = func
		self.cache = {}

	def __call__(self, *args):
		if not isinstance(args, collections.Hashable):
			# We can't cache this effectively
			return self.func(*args)
		if args in self.cache:
			return self.cache[args]
		else:
			value = self.func(*args)
			self.cache[args] = value
			return value

	def __repr__(self):
		return self.func.__doc__

	def __get__(self, obj, objtype):
		# Support for instance methods
		return functools.partial(self.__call__, obj)
