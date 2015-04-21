import imp
from lxml import etree

from . import helpers
from .errors import *

class FormatterFactory:

	def __init__(self, config):
		self.config = config

	def get_formatter(self, name):
		path = self.locate_formatter(name)

		if path is None:
			raise Exception("TODO: Could not find formatter %s" % name)

		try:
			formatter = imp.load_source('read_device.formatter', path).formatter
			return formatter

		except AttributeError:
			raise Exception("TODO: Could not load formatter (ensure the file contains the 'formatter' variable)")

	def locate_formatter(self, formatter_name):
		return helpers.locate_in_dir('formatter', self.config.formatter_paths,
			join='%s.py' % formatter_name)

class DeviceFactory(object):

	def __init__(self, config):
		self.config = config

	def from_config(self):
		# Load all the devices from profiles and apply mutators
		for node in self.config.tree.xpath('//Device'):
			# Look up the profile from the profile cache
			profile = self.config.profiles.get(node.get('profile'))

			# Get a dict of the arguments specified on the node
			# and pass them to a new instance of the profile
			arguments = self.config.walk(node)
			device    = self.from_arguments(profile, arguments)

			# Set the path on the new device
			device.path = self.build_path(node)

			# Apply mutators if applicable
			if device.mutator is not None:
				self.config.apply_mutator(device)

			yield device

	def from_arguments(self, profile, arguments):
		if profile:
			return profile(arguments)

	def build_path(self, node, path=[]):
		path = path + [node]
		if node.getparent() is not None:
			node = node.getparent()
			return self.build_path(node, path)

		return path

class ProfileFactory(object):

	def __init__(self, config):
		self.config = config

	def create(self, what):
		if type(what) in (list, map):
			return { w: self.create_one(w) for w in what }
		else:
			return self.create_one(what)

	def create_one(self, _from=None):
		"""
		Return a profile object from either a device node or profile name
		"""

		profile = None

		if type(_from) is str:
			profile = self._from_name(_from)
		elif type(_from) == etree._Element:
			profile = self._from_node(_from)

		return profile


	def _from_name(self, name):
		profile_path = self.locate_profile(name)

		if profile_path:
			# Try to import the specified file
			try:
				profile = imp.load_source('read_device.profile', profile_path).profile
			except AttributeError:
				raise ConfigurationError("Couldn't load profile from %s. Is the profile variable defined?" % profile_path)
		else:
			# Try to load the given mutator and attach it to the profile
			profile, mutator = self._from_mutator(name)
			profile.mutator = mutator
			self.config.apply_mutator(profile)

		try:
			profile.profile_name = name
			return profile
		except AttributeError:
			raise ConfigurationError('No profile was matched - does it exist?')

	def _from_node(self, node):
		name = node.get('profile')

		return self._from_name(name)

	def _from_mutator(self, name):
		mutator_path = self.locate_mutator(name)

		if mutator_path:
			mutator = etree.parse(mutator_path).getroot()
			profile = self.create(mutator.get('profile'))
			profile.parent_name = profile.profile_name

			return profile, mutator

	def locate_profile(self, profile_name):
		return helpers.locate_in_dir('profile', self.config.profile_paths,
			join='%s.py' % profile_name)

	def locate_mutator(self, profile_name):
		return helpers.locate_in_dir('mutator', self.config.profile_paths,
			join='%s.xml' % profile_name)
