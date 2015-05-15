# Copyright 2015 University of Edinburgh
# Licensed under GPLv3 - see README.md for information

import sys
import click

from ..config import DeviceConfig as Config
from ..concurrency import WorkQueue
from ..helpers import set_exception_handler

pass_config = click.make_pass_decorator(Config)
formatters = Config.formatters()

@click.group()
@click.option('-q', '--quiet', is_flag=True,
	default=False, help="Don't prompt or display errors")
@click.option('-f', '--format', type=click.Choice(formatters),
	default='pretty', help='Specify an output format. Default: pretty')
@click.option('-y', '--assumeyes', is_flag=True,
	default=False, help='Assume yes to any prompts')
@click.pass_context
def main(ctx, **kwargs):
	"""
	Query the state of various types of hardware.

	read-device Copyright 2015 University of Edinburgh
	See <https://github.com/lewiseason/read-device> for information
	"""

	# If the quiet flag is passed, don't report exceptions.
	set_exception_handler(quiet=kwargs['quiet'])

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
@click.option('-t', '--type',
	default=None, help='Device type')
@pass_config
@click.pass_context
def enumerate(ctx, config, **kwargs):
	""" Query all properties of a given device """

	devices = config.devices.find_or_create(kwargs)
	queue   = WorkQueue(concurrency=12)

	if not devices and not config.quiet:
		click.echo('No devices were matched')
		ctx.exit(1)

	if len(devices) > 1:
		message = "Parameters specified match %i devices. Are you sure?" % len(devices)
		if not config.assumeyes:
			click.confirm(message, default=False, abort=True)

	[ queue.append(device.enumerate) for device in devices]

	queue.execute()

	click.echo(config.formatter.devices(devices, summary=False))

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

	click.echo(config.formatter.devices(devices, summary=True))
