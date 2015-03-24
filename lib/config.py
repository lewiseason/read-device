from lxml import etree

from lib.device import DeviceFinder, DeviceFactory
from lib.formatters import FormatterFactory
import lib.helpers as h

class Config(object):

	# TODO: Make this configurable
	profile_paths = [
		'/etc/read_device/profiles',
		'lib/profiles',
	]

	formatter_paths = [
		'/etc/read_device/formatters',
		'lib/formatters',
	]

	_formatter = None

	def __init__(self):
		config_path = h.locate_file('configuration', [
			'~/.read_device/site.xml',
			'/etc/read_device/site.xml',
			'config/site.xml',
		])

		self.tree = etree.parse(config_path)
		self.finder = DeviceFinder(self.tree, self)
		self.factory = DeviceFactory(self.tree, self)

	def load_interactive(self, arguments):
		"""
		Adjust configuration based on command-line arguments
		"""

		for argument in arguments:
			setattr(self, argument, arguments[argument])

	def instantiate_devices(self, facets, allow_multiple=True):
		# Exclude arguments which aren't defined
		facets = dict([ [k, facets[k]] for k in facets if facets.get(k) ])

		nodes = self.finder.find_or_create(facets, allow_multiple=allow_multiple)
		devices = self.factory.create(nodes)

		return devices

	def instantiate_device(self, facets):
		devices = self.instantiate_devices(facets, allow_multiple=False)
		return devices[0]

	def instantiate_profile(self, profile_name):
		return self.factory.get_profile(profile_name=profile_name)

	def list_profiles(self):
		files = h.multiglob(self.profile_paths, ['*.py', '*.xml'])
		names = map(h.path_to_profile_name, files)

		return names

	def list_devices(self, facets={}):
		nodes = self.finder.where(facets)
		return self.factory.create(nodes)


	def instantiate_formatter(self, format):
		return FormatterFactory(self).get_formatter(format)

	@property
	def formatter(self):
		if self._formatter is None:
			self._formatter = self.instantiate_formatter(self.format)()
		return self._formatter