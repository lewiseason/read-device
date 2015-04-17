import pymodbus.client.sync
import pymodbus.exceptions

from read_device.lib.resources import BaseProfile, Property, requires_configuration
from read_device.lib.decoders import decode
from read_device.lib.decorators import *

class TCPModbus(BaseProfile):

	required_arguments = set(['address', 'slave'])

	manufacturer = 'N/A'
	product = 'Generic TCP/Modbus Gateway'
	version = 2

	def configure(self):
		self.slave = int(self.slave)
		self.client = ModbusTcpClient(self.address)

		self.properties = [ self.munge(property) for property in self.Property ]

	def munge(self, property):
		property['mode']    = int(property.get('mode'))
		property['words']   = int(property.get('words'))
		property['address'] = int(property.get('address'), 16)

		return Property(property)

	@requires_configuration
	def enumerate(self):
		for property in self.properties:
			self.queue(self.read, (property,))

		self.execute()

	@requires_configuration
	@attempts(3, AttributeError, pymodbus.exceptions.ConnectionException)
	def read(self, property):
		if   property.mode is 3: method = self.client.read_holding_registers
		elif property.mode is 4: method = self.client.read_input_registers

		response = method(property.address, property.words, unit=self.slave).registers
		property.populate(self.decoder(response))

profile = TCPModbus
