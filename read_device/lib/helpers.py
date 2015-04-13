import os
import glob
import itertools

from .errors import *

def locate_file(what, locations, quiet=False):
	"""
	Try and find a file in multiple locations.
	Return the path of the first one that exists
	"""

	locations = map(os.path.expanduser, locations)

	for location in locations:
		if os.path.exists(location):
			return location

	if quiet:
		return None

	raise ConfigurationError("The %s file could not be found in any of these locations: %s" % (what, ', '.join(locations)))

def locate_in_dir(what, locations, join=None, concat=None):
	locations = map(os.path.expanduser, locations)

	for location in locations:
		if join:
			path = os.path.join(location, join)
		elif concat:
			path = location + join
		else:
			path = location

		if os.path.isfile(path):
			return path

def multiglob(locations, patterns):
	"""
	Search in multiple directories for multiple globbing patterns
	and return a big iterator for all matches

	Example:
		# Search /etc/profiles and ./lib/profiles for .py and .xml files
		multiglob(['/etc/profiles', './lib/profiles'], ['*.py', '*.xml'])
	"""
	files = iter([])

	for location in locations:
		for pattern in patterns:
			path = os.path.join(location, pattern)
			matches = glob.iglob(path)

			files = itertools.chain(files, matches)

	return files

def path_to_profile_name(path):
	path = os.path.basename(path)
	name, _ = os.path.splitext(path)
	return name

import collections
import functools

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
