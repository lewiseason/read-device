import imp

from lib.helpers import locate_in_dir

class FormatterFactory:

	def __init__(self, config):
		self.config = config

	def get_formatter(self, name):
		path = self.locate_formatter(name)

		if path is None:
			raise Exception("TODO: Could not find formatter %s" % name)

		try:
			formatter = imp.load_source('formatter', path).formatter
			return formatter

		except AttributeError:
			raise Exception("Could not load formatter (ensure the file contains the 'formatter' variable)")

	def locate_formatter(self, formatter_name):
		return locate_in_dir('formatter', self.config.formatter_paths,
			join='%s.py' % formatter_name)
