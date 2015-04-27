import pymodbus.client.sync
import pymodbus.exceptions

from .resources import BaseProfile
from .decorators import *
from .decoders import decode

class TCPModbus(BaseProfile):

	required_arguments = set(['address', 'slave'])

	manufacturer = 'N/A'
	product = 'Generic TCP/Modbus Gateway'
	version = 2

	def configure(self):
		self.slave  = int(self.slave)
		self.client = pymodbus.client.sync.ModbusTcpClient(self.address)

		self.properties = [ self.to_property(data) for data in self.Property ]
		self.decoder    = decode[self.encoding]

	def munge(self, data):
		data['mode']    = int(data.get('mode'))
		data['words']   = int(data.get('words'))
		data['address'] = int(data.get('address'), 16)

	@requires_configuration
	def enumerate(self):
		for property in self.properties:
			self.queue(self.read, (property,))

		self.execute()

	@requires_configuration
	@attempts(3, 0.2, AttributeError, pymodbus.exceptions.ConnectionException)
	def read(self, property):
		if property.mode is 3:
			method = self.client.read_holding_registers
		elif property.mode is 4:
			method = self.client.read_input_registers

		response = method(property.address, property.words, unit=self.slave).registers
		property.populate(self.decoder(response))

profile = TCPModbus
