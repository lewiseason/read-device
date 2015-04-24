from os import path
from lxml import etree

from . import helpers
from .decorators import cached
from .finder import DeviceFinder
from .factories import ProfileFactory, DeviceFactory, FormatterFactory

HERE = path.dirname(__file__)

class Config(object):

	config_paths = [
		'~/.read_device/site.xml',
		'/etc/read_device/site.xml',
		# TODO: This probably shouldn't exist
		path.join(HERE, '../config/site.xml'),
	]

	profile_paths = [
		'/etc/read_device/profiles',
		path.join(HERE, 'profiles'),
	]

	formatter_paths = [
		'/etc/read_device/formatters',
		path.join(HERE, 'formatters'),
	]

	_formatter = None

	def __init__(self, kwargs):
		config_file = helpers.locate_file('configuration', self.config_paths)

		self.load_interactive(kwargs)
		self.load_factories()
		self.load_profiles()
		self.load_config(config_file)
		self.load_devices()
		self.devices = DeviceFinder(self)

	def load_interactive(self, arguments):
		"""
		Adjust configuration based on command-line arguments
		"""

		for argument, value in arguments.items():
			setattr(self, argument, value)

	def load_factories(self):
		self.profile_factory = ProfileFactory(self)
		self.device_factory  = DeviceFactory(self)

	def load_config(self, file):
		self.tree = etree.parse(file)

	def load_profiles(self):
		files = helpers.multiglob(self.profile_paths, ['*.py', '*.xml'])
		names = map(helpers.path_to_profile_name, files)

		self.profiles = self.profile_factory.create(names)

	def load_devices(self):
		self._devices = list(self.device_factory.from_config())

	def create_device(self, profile, arguments):
		return self.device_factory.from_arguments(profile, arguments)

	def apply_mutator(self, device):
		"""
		Map the Fields and Children of a mutator onto the device.
		"""
		data = self.walk(device.mutator, max_depth=1)

		for field in data['Field']:
			(key, value), = field.items()
			setattr(device, key, value)

		for child_type in data['Children']:
			(tag, children), = child_type.items()
			children = map(lambda c: dict(c.items()), children)
			setattr(device, tag, children)

	def walk(self, node, max_depth=None, depth=0):
		"""
		Recursively walk the xml tree of a node, and build
		lists of the child objects
		"""
		data = dict(node.items())

		if node.getchildren():
			for child in node.getchildren():
				if not data.get(child.tag):
					data[child.tag] = []

				if max_depth and depth >= max_depth:
					data[child.tag].append(child)
				else:
					data[child.tag].append(self.walk(child, max_depth=max_depth, depth=depth+1))

		return data

	@classmethod
	def formatters(klass):
		files = helpers.multiglob(klass.formatter_paths, ['*.py'])
		return list(map(helpers.path_to_profile_name, files))

	@property
	@cached
	def formatter(self):
		return FormatterFactory(self).get_formatter(self.format)()

class DeviceConfig(Config):
	pass

import json

from . import database

class MetersConfig(Config):

	def load_data(self, file):
		self.data = json.loads(file.read().decode('utf-8'))

	@property
	def db(self):
		database.connect(self.dbpath)
		return database

	@property
	@cached
	def dbpath(self):
		if self.dbname is not None:
			return self.dbname

		return 'a.db'
