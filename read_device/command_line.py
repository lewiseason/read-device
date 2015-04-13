import sys
import click
from .lib.config import Config
from .lib.errors import *

pass_config = click.make_pass_decorator(Config)

formatters = ['pretty', 'cacti']

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

	# If the quiet flag is passed, don't report exceptions.
	set_exception_handler(kwargs['quiet'])

	config  = Config(kwargs)
	ctx.obj = config

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

	devices = config.devices.find_or_create(kwargs)

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
	# TODO: Concurrency
	# TODO: Merge in with enumerate - and prompt yes/no if multiple matches
	# And in quiet mode either fail, assume yes or accept an argument
	devices = config.devices.find(kwargs)

	for device in devices:
		device.enumerate()
		click.echo(config.formatter.device(device))

@main.command()
@pass_config
def profiles(config):
	""" List all available profiles """

	names = config.profiles

	click.echo(
		config.formatter.profiles(config.profiles)
	)

# TODO: Pass arguments for filtering, including location, perhaps?
@main.command()
@pass_config
def list(config, **kwargs):
	""" List all known devices """

	devices = config.devices.all()

	click.echo(
		config.formatter.devices(devices)
	)
