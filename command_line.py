import sys
import click
from lib.config import Config
from lib.errors import *

pass_config = click.make_pass_decorator(Config)

formatters = ['pretty', 'cacti', 'csv']

@click.group()
@click.option('-q', '--quiet', is_flag=True,
	default=False, help="Don't prompt or display errors")
@click.option('-f', '--format', type=click.Choice(formatters),
	default='pretty', help='Specify an output format. Default: pretty')
@click.pass_context
def main(ctx, **kwargs):
	"""
	Query the state of various types of hardware.
	"""

	config  = Config(kwargs)
	ctx.obj = config

	# If the quiet flag is passed, don't report exceptions.
	set_exception_handler(config.quiet)

@main.command()
@click.option('-n', '--name',
	default=None, help='Preconfigured device name')
@click.option('-a', '--address',
	default=None, help='Address/hostname of the device')
@click.option('-s', '--sub-id', '--slave',
	default=None, help='Device-specific sub/slave id')
@click.option('-p', '--profile',
	default=None, help='Device profile')
@pass_config
def enumerate(config, **kwargs):
	""" Query all properties of a given device """

	devices = config.instantiate_devices(kwargs)

	if len(devices) == 1:
		device = devices[0]
		device.enumerate()

		click.echo(
			config.formatter.device(device)
		)
	elif len(devices) == 0:
		raise RuntimeError('TODO: No devices matched')
	else:
		raise RuntimeError('TODO: Ambiguous request - %i devices matched' % len(devices))

@main.command()
@click.option('-p', '--profile',
	default=None, help="Device profile")
@click.option('-t', '--type',
	default=None, help="Device type")
@pass_config
def hammer(config, **kwargs):
	"""
	Query all known devices (optionally filtering by profile or type)
	"""
	# The way this command filters is a little different to the others.
	# Because instantiate_devices does a find_or_create THEN asks DeviceFactory
	# to actually create the Device, fields loaded from mutators are not available
	# during the initial query. So we pass an empty dictionary and do the filtering
	# once all the Devices have been created.
	#
	# TODO: A better way would be to load the entire tree (cached in the config
	# object) with all the created nodes rather than creating the nodes on the fly.
	# This would mean you could search by all possible fields
	# searching it with xpath. At that point, the only difference between enumerate
	# and hammer is that enumerate will only display one result at a time. Some
	# semantic juggling required.
	# TODO: Concurrency
	devices = config.instantiate_devices({})

	if kwargs['profile'] is not None:
		devices = filter(lambda device: device.profile == kwargs['profile'], devices)

	if kwargs['type'] is not None:
		devices = filter(lambda device: device.type == kwargs['type'], devices)

	for device in devices:
		device.enumerate()
		click.echo(config.formatter.device(device) + "\n")

@main.command()
@pass_config
def profiles(config):
	""" List all available profiles """

	names = config.list_profiles()
	profiles = [ config.instantiate_profile(name) for name in names ]

	click.echo(
		config.formatter.profiles(profiles)
	)

# TODO: Pass arguments for filtering, including location, perhaps?
@main.command()
@pass_config
def list(config, **kwargs):
	""" List all known devices """

	devices = config.list_devices()

	click.echo(
		config.formatter.devices(devices)
	)
