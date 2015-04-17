import re
from decimal import Decimal
from lxml import etree
import requests
from collections import namedtuple

from read_device.lib.resources import BaseProfile, Property
from read_device.lib.decoders import decode
from read_device.lib.decorators import *

Module = namedtuple('Module', ['name', 'prefix', 'transforms', 'fields'])

class TrendIQ3(BaseProfile):

	required_arguments = set(['address'])

	manufacturer = 'Trend Controls'
	product = 'IQ3xite'
	version = 1
	type = 'BEMS Controller'

	properties = []

	known_modules = [
		Module('Sensor',        'S', ['to_decimal', 'strip_no_units'], ['id', 'name', 'value', 'unit', None]),
		Module('Knob',          'K', ['to_decimal'],                   ['id', 'name', 'value', 'unit']),
		Module('Digital Input', 'I', ['to_boolean'],                   ['id', 'name', 'value', None]),
		Module('Driver',        'D', [],                               ['id', 'name', 'value', 'status', None, None])
	]

	def configure(self):
		# TODO: self.meta['controller_version'] = ...
		pass

	@requires_configuration
	def enumerate(self, properties=None):
		# TODO: Do something with properties instead of scraping the whole thing
		# TODO: Check if the module exists before trying to read it
		for module in self.known_modules:
			self.queue(self.read_module, (module,))

		self.execute()

	def read_module(self, module):
		reads = 0
		start = 0

		while True:
			records, start = self.get_page(module, start)

			[ self.create_property(data) for data in records ]

			if reads > 0 and start == 0:
				break

			reads += 1

	def get_page(self, module, start=0):
		resp = requests.get('http://%s/%s.htm?ovrideStart=%s' % (self.address, module.prefix, start))
		tree = etree.HTML(resp.text)
		rows = tree.xpath('//*[@id="maindata"]//*[@class="data "]')

		data = [ self._nodes_to_dict(module, row) for row in rows ]

		next_string = tree.xpath('//map[@name="m_forwardbutton"]/area/@href')[1]
		next_page   = int(re.search(r'(\d+)', next_string).group(0))

		return data, next_page

	def create_property(self, data):
		property = Property(data)

		self.properties.append(property)

	def _nodes_to_dict(self, module, nodes):
		values = nodes.xpath('td/text() | td/a/text() | td/input[@type="text"]/@value')
		# Combine the values (list) with the list of fields for this module
		values = dict(zip(module.fields, values))
		# Remove any mapped to "None" from the list
		values.pop(None, None)
		# Apply any transforms defined in the module (in order, obviously)
		for name in module.transforms:
			transform = getattr(self, name)
			values = transform(values)

		return values

	def to_boolean(self, values):
		value  = values['value'].lower()
		truthy = ['on', 'true', 'yes']
		falsey = ['off', 'false', 'no']

		if value in truthy:
			values['value'] = True

		elif value in falsey:
			values['value'] = False

		return values

	def to_decimal(self, values):
		d = Decimal(values['value'])

		if d.is_normal():
			values['value'] = d
		else:
			values['value'] = None

		return values

	def strip_no_units(self, values):
		no_units = ['no', 'no.']

		if values['unit'].lower() in no_units:
			values['unit'] = ''

		return values

profile = TrendIQ3
