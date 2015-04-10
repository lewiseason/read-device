import imp
from lxml import etree

from lib.helpers import locate_in_dir
from lib.errors import *

class DeviceFinder:
	"""
	Responsible for returning an etree node given a set of facets.
	This class will attempt to do this on-the-fly, if "profile" is
	one of the facets.
	"""

	def __init__(self, tree, config):
		self.tree = tree
		self.config = config

	def find_or_create(self, facets):
		""" Try to find the existing node, if there is one. If not, attempt to create one. """
		nodes = self.where(facets)

		if not nodes:
			nodes = [self.create_from(facets)]

		return nodes

	def where(self, facets={}):
		""" Search for matching Device definitions """
		if facets:
			# Build a '@key = "value"' expression for each argument
			attributes = map(lambda attribute: '@%s="%s"' % (attribute, facets[attribute]), facets)
			expression = '//Device[%s]' % ' and '.join(attributes)
		else:
			expression = '//Device'

		return self.tree.xpath(expression)

	def create_from(self, facets):
		if facets.get('profile') is None:
			raise ConfigurationError("No devices were matched and no profile was specified for on-the-fly creation.")

		return etree.Element("Device", facets)

class DeviceFactory:
	"""
	Responsible for converting device node(s) into instance(s) of Profile classes.

	Most of the complexity/magic in this application lives here - and a refactor
	is probably a good idea in the long run.
	"""

	def __init__(self, tree, config):
		self.tree = tree
		self.config = config

	def create(self, data):
		""" Create one or more device objects """
		if type(data) is list:
			return [ self.create(node) for node in data ]
		else:
			return self.create_one(data)

	def create_one(self, node):
		profile = self.get_profile(node)
		arguments = self.walk(node)

		device = profile(arguments)
		device.path = self.build_path(node)

		return device

	def get_profile(self, node=None, profile_name=None):
		""" Actually map the node into a class """
		if node is None:
			node = etree.Element("Device")

		if profile_name is None:
			profile_name = node.get('profile')

		profile_path = self.locate_profile(profile_name)

		if profile_path:
			# Look inside the specified path (python file)
			# for the "profile" variable.
			profile = imp.load_source('profile', profile_path).profile

		else:
			# Otherwise, try xml mutators
			profile = self.profile_from_mutator(node, profile_name)

		try:
			profile.profile_name = profile_name

			return profile
		except AttributeError:
			raise ConfigurationError('No profile was matched - make sure it exists?')

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


	def locate_profile(self, profile_name):
		return locate_in_dir('profile', self.config.profile_paths,
			join='%s.py' % profile_name)

	def locate_mutator(self, profile_name):
		return locate_in_dir('mutator', self.config.profile_paths,
			join='%s.xml' % profile_name)

	def profile_from_mutator(self, node, profile_name):
		"""
		Given a profile name - try to find a mutator of that name,
		do the mutation and get_profile the resulting node.

		As this is called by get_profile, it's possible to nest mutators.
		"""
		mutator_path = self.locate_mutator(profile_name)

		if mutator_path:
			mutator_node = etree.parse(mutator_path).getroot()
			base_profile_name = mutator_node.get('profile')

			node = self.merge_node_mutator(node, mutator_node)

			profile = self.get_profile(node, base_profile_name)
			profile = self.merge_profile_mutator(profile, mutator_node)

			return profile

	def merge_node_mutator(self, node, mutator):
		"""
		Produce a single etree node from a node and a mutator.
		ie: perform the mutation
		"""
		data = self.walk(mutator, max_depth=1)

		# Add the additional Fields as attributes on the node
		for field in data['Field']:
			# field is a single-key dict - map it to variables
			(key, value), = field.items()
			# And update the node to reflect the new attribute
			node.set(key, value)

		for child_type in data['Children']:
			(tag, children), = child_type.items()
			for child in children:
				node.append(child)

		return node

	def merge_profile_mutator(self, profile, mutator):
		"""
		Map the Fields of a mutator onto a profile.

		As we probably want mutator fields to be available on both
		the profile and any device created from it, we need this
		method to map it onto the profile in addition to
		merge_node_mutator.
		"""

		data = self.walk(mutator, max_depth=1)

		profile.parent_name = profile.profile_name

		for field in data['Field']:
			(key, value), = field.items()
			setattr(profile, key, value)

		return profile

	def build_path(self, node, path=[]):
		"""
		Recurse up the tree to build a list of parents
		"""

		path = []

		while True:
			if node.getparent() is not None:
				path.append(node)
				node = node.getparent()
			else:
				break

		return path
		# path.append(node)

		# if node.getparent() is not None:
		# 	return self.build_path(node.getparent(), path)
		# else:
		# 	return path
