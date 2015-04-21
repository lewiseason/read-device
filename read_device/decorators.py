import sys
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

	def __init__(self, attempts=3, *exceptions):
		self.max_attempts = attempts
		self.exceptions   = exceptions

	def __call__(self, func):
		@functools.wraps(func)
		def wrap(target, *args, **kwargs):
			self.attempt(target, func, *args, **kwargs)

		return wrap

	def attempt(self, target, func, *args, **kwargs):
		info = None
		for _ in range(self.max_attempts):
			try:
				return func(target, *args, **kwargs)
			except self.exceptions as exception:
				info = sys.exc_info()
			else:
				break
		else:
			if info:
				# sys.excepthook(*info)
				raise RuntimeError('TODO: Controller failed after %%i attempts')

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
