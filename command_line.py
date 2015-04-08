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

	device = config.instantiate_device(kwargs)
	device.enumerate()

	click.echo(
		config.formatter.device(device)
	)

@main.command()
@pass_config
def hammer(config):

	devices = config.instantiate_devices({})

	for device in devices:
		device.enumerate()
		click.echo(config.formatter.device(device) + "\n")

	pass # Enumerate all matching devices (TODO: filtering)

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
