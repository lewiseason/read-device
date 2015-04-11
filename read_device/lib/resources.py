import sys
import threading

from .parser import Parser
from .queue import ChunkedQueue

class BaseProfile(object):
		"""
		A base class for every device profile.

		Provides:
				* property lookup on the arguments. eg: d = Device({args...}); p.arg
				* enforcement of required_arguments if specified on the subclass
		"""

		configured  = False
		properties  = []

		profile_name = None
		parent_name = None
		product = None
		manufacturer = None

		def __init__(self, arguments):
			self._queue = ChunkedQueue()
			self.args = arguments
			self._enforce_required_arguments()

		def configure(self):
				pass

		def enumerate(self):
				pass

		def queue(self, target, args=(), name=None):
			self._queue.enqueue(target=target, args=args, name=name or self.address)

		def execute(self):
			self._queue.execute()

		def __getattr__(self, key):
				return self.args.get(key)

		def _enforce_required_arguments(self):
				if self.required_arguments and not self.required_arguments.issubset(set(self.args)):
						raise Exception("TODO: The provided data is insufficient to match a single device with no ambiguity on the %s profile." % self.__class__.__name__)

class BaseFormatter(object):
		pass

class Property(object):
		"""
		Represents a property of a device

		Provides:
				* a "transform" option for basic math transformations
				* attribute lookup

		"""

		populated = False

		def __init__(self, args):
				self.__dict__ = args
				self.parser = Parser()

				if 'value' in args:
					self.populate(args['value'])

		def __getattr__(self, key):
				return None

		def populate(self, value):
				self.value = value
				self.populated = True
				return self

		@property
		def value(self):
				val = self._value
				if self.populated and self.transform:
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
