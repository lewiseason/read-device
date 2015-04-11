from time import sleep
from pymodbus.client.sync import ModbusTcpClient
import pymodbus.exceptions as mb_exceptions

from read_device.lib.resources import BaseProfile, Property, requires_configuration
from read_device.lib.decoders import decode
from read_device.lib.errors import *


class TCPModbus(BaseProfile):

	required_arguments = set(['address', 'slave'])

	manufacturer = 'N/A'
	product = 'Generic TCP/Modbus Gateway'
	version = 2

	def configure(self):
		self.slave = int(self.args.get('slave'))
		self.client = ModbusTcpClient(self.address)

		self.properties = [ self.munge(property) for property in self.args.get('Property')]

	def munge(self, property):
		property['mode']    = int(property['mode'])
		property['words']   = int(property['words'])
		property['address'] = int(property['address'], 16)

		return Property(property)

	@requires_configuration
	def enumerate(self):
		for property in self.properties:
			self.queue(self.read, (property,))

		self.execute()

	@requires_configuration
	def read(self, property):
		attempts  = 1
		response  = None
		exception = None

		while True:
			try:
				if property.mode is 3:
					response = self.client.read_holding_registers(property.address, property.words, unit=self.slave).registers
				elif property.mode is 4:
					response = self.client.read_input_registers(property.address, property.words, unit=self.slave).registers

			except Exception as e:
				exception = e
				sleep(0.2)

			finally:
				attempts += 1
				if response or attempts > 3:
					break

		if response:
			decoder = decode[self.encoding]
			property.populate(decoder(response))
		# TODO: Waiting for queued exceptions.
		# When an exception is raised, pop it on a queue and have the formatter
		# decide what to do with it *at the end*
		# else:
		# 	message = "The device did not respond while trying to retrieve %s" % property.name
		# 	if exception:
		# 		message += " (The original error was a %s)" % exception.__class__.__name__

		# 	raise ResponseError(message)

profile = TCPModbus
