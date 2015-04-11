import click
from texttable import Texttable

from read_device.lib.resources import BaseFormatter

class PrettyFormatter(BaseFormatter):

  def device(self, device):
    # TODO: Way of loading additional fields (web interface version etc)
    table = Texttable(max_width=self._termwidth())

    table.set_deco(0)
    # table.header(['Name', 'ID', 'Value', 'Unit'])
    table.set_cols_align(['l', 'r', 'l', 'l'])

    for property in device.properties:
      label = "%s (%s)" % (property.name, property.id)
      if property.populated:
        value = "{:>12} {:<}".format(property.value, property.unit)
      else:
        value = "{:>12}".format('Error')

      table.add_row([label, value])

    return "%s\n\n%s" % (device.name, table.draw())

  def profiles(self, profiles):
    table = Texttable(max_width=self._termwidth())

    table.set_deco(Texttable.VLINES | Texttable.HEADER)
    table.header(['Name', 'Product', 'Manufacturer', 'Version'])
    table.set_cols_dtype(['t', 't', 't', 'i'])

    for profile in profiles:
      # Add an asterisk to the name if the profile has a parent profile
      name = profile.profile_name if profile.parent_name is None else "%s*" % profile.profile_name
      table.add_row([name, profile.product, profile.manufacturer, profile.version])

    return "\n" + table.draw() + "\n\n* Mutator profile \n"

  def devices(self, devices):
    table = Texttable(max_width=self._termwidth())

    table.set_deco(Texttable.VLINES | Texttable.HEADER)
    table.header(['Name', 'Address', 'Slave', 'Profile', 'Location'])

    for device in devices:
      table.add_row([device.name, device.address, device.slave, device.profile, self.location(device.path)])

    return "\n" + table.draw() + "\n"


  def location(self, path):
    if len(path) > 1:
      return path[1].get('name')
    else:
      return ""

  def _termwidth(self):
    return click.get_terminal_size()[0]

formatter = PrettyFormatter
