import os
import glob
import itertools

import click

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

	# Remove any files which contain __init__.py
	files = [ f for f in files if '__init__.py' not in f ]
	return files

def path_to_profile_name(path):
	path = os.path.basename(path)
	name, _ = os.path.splitext(path)
	return name

def handle_exception_normally(exctype, value, traceback):
	if issubclass(exctype, DefinedError):
		click.echo("%s: %s" % (exctype.__name__, value), err=True)
	else:
		# If the exception isn't one of ours, handle it in the default way
		sys.__excepthook__(exctype, value, traceback)

def handle_exception_quietly(exctype, value, traceback):
	# Obviously, if the exception occurs in a thread (which is quite likely)
	# this exit code will never go anywhere.
	sys.exit(255)

def set_exception_handler(quiet):
	if quiet:
		sys.excepthook = handle_exception_quietly
	else:
		sys.excepthook = handle_exception_normally
