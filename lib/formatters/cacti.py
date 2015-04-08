from lib.resources import BaseFormatter

"""
Formatter for Cacti data input method.
http://docs.cacti.net/manual:087:3a_advanced_topics.1_data_input_methods
"""
class CactiFormatter(BaseFormatter):
	def device(self, device):
		parts = []

		for property in device.properties:
			part = "%s:%s" % (property.id, property.value)
			# Cacti format is space-separated
			part.replace(' ', '_')
			parts.append(part)

		return ' '.join(parts)

formatter = CactiFormatter
