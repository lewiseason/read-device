import sys
import threading

from lib.parser import Parser

class BaseProfile(object):
	"""
	A base class for every device profile.

	Provides:
		* a very basic model for threading through queue() and execute()
		* property lookup on the arguments. eg: d = Device({args...}); p.arg
		* enforcement of required_arguments if specified on the subclass
	"""

	configured  = False
	max_threads = 8
	threads     = []
	properties  = []

	profile_name = None
	parent_name = None
	product = None
	manufacturer = None

	def __init__(self, arguments):
		self.args = arguments
		self._enforce_required_arguments()
		self._install_thread_excepthook()

	def configure(self):
		pass

	def enumerate(self):
		pass

	def queue(self, target, args=(), name=None):
		thread = threading.Thread(target=target, args=args, name=name or self.address)
		self.threads.append(thread)

	def execute(self):
		while self.threads:
			if len(self.threads) > self.max_threads:
				# There are too many threads to run at once, split into chunks
				chunk = self.threads[0:self.max_threads]
			else:
				chunk = self.threads[:]

			# Start all the threads in the chunk
			[ thread.start() for thread in chunk ]
			# And wait for them to complete,
			# before proceeding to the next chunk, if there is one
			[ thread.join() for thread in chunk ]
			del(self.threads[0:self.max_threads])

	def __getattr__(self, key):
		return self.args.get(key)

	def _enforce_required_arguments(self):
		if self.required_arguments and not self.required_arguments.issubset(set(self.args)):
			raise Exception("TODO: The provided data is insufficient to match a single device with no ambiguity on the %s profile." % self.__class__.__name__)


		def _enforce_required_arguments(self):
				if self.required_arguments and not self.required_arguments.issubset(set(self.args)):
						raise Exception("TODO: The provided data is insufficient to match a single device with no ambiguity on the %s profile." % self.__class__.__name__)

		def _install_thread_excepthook(self):
			# Python bug: http://bugs.python.org/issue1230540
			# Threads don't use the excepthook
			old = threading.Thread.run

			def run(*args, **kwargs):
				try:
					old(*args, **kwargs)
				except:
					sys.excepthook(*sys.exc_info())

			threading.Thread.run = run

		def run(*args, **kwargs):
			try:
				old(*args, **kwargs)
			except:
				sys.excepthook(*sys.exc_info())

		threading.Thread.run = run

class BaseFormatter(object):
	pass

class Property(object):
	"""
	Represents a property of a device

	Provides:
		* a "transform" option for basic math transformations
		* attribute lookup

	"""

	def __init__(self, args):
		self.__dict__ = args
		self.parser = Parser()

		if 'value' in args:
			self.value = args['value']

	def __getattr__(self, key):
		return None

	def populate(self, value):
		self.value = value
		return self

	@property
	def value(self):
		val = self._value
		if self.transform:
			# Use the parser to transform the value, based on
			# a simple math expression.
			val = self.parser.eval(self.transform, { 'value': val })

		return val

	@value.setter
	def value(self, value):
		self._value = value

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
		profile = self.func.__self__
		if not profile.configured:
			profile.configure()
			profile.configured = True

		return self.func(*args, **kwargs)
