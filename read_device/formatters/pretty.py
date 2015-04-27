import click
from texttable import Texttable

class PrettyFormatter:

	def devices(self, devices, summary=True):
		if summary:
			return self._devices_list(devices)
		else:
			return '\n'.join([ self.device(device) for device in devices ])

	def device(self, device):
		# TODO: Way of loading additional fields (web interface version etc - META)
		table = Texttable(max_width=self._termwidth())

		table.set_deco(0)
		table.set_cols_align(['l', 'r', 'l'])

		table.header([device.name, '', ''])

		for property in device.properties:
			if property.populated:
				if type(property.value) is bool:
					value = 'On' if property.value else 'Off'
				else:
					value = property.value
			else:
				value = '-'

			table.add_row(["%s (%s)" % (property.name, property.id), value, property.unit or ''])

		return table.draw()

	def profiles(self, profiles):
		table = Texttable(max_width=self._termwidth())

		table.set_deco(Texttable.VLINES | Texttable.HEADER)
		table.header(['Name', 'Product', 'Manufacturer', 'Version', 'Type'])
		table.set_cols_dtype(['t', 't', 't', 'i', 't'])

		for profile in profiles.values():
			# Add an asterisk to the name if the profile has a parent profile
			name = profile.profile_name if profile.parent_name is None else "%s*" % profile.profile_name
			table.add_row([name, profile.product, profile.manufacturer, profile.version, profile.type])

		return "\n" + table.draw() + "\n\n* Mutator profile \n"

	def _devices_list(self, devices):
		table = Texttable(max_width=self._termwidth())

		table.set_deco(Texttable.VLINES | Texttable.HEADER)
		table.header(['Name', 'Address', 'Slave', 'Profile', 'Location'])

		for device in devices:
			table.add_row([device.name, device.address, device.slave, device.profile, self._location(device.path)])

		return "\n" + table.draw() + "\n"


	def _location(self, path):
		if len(path) > 1:
			# ?
			return "%s[%s]" % (path[1].tag, path[1].get('name'))
			# return path[1].get('name')
		else:
			return ""

	def _termwidth(self):
		return click.get_terminal_size()[0]

formatter = PrettyFormatter
