import click

from ..config import MetersConfig as Config
from ..helpers import set_exception_handler

import peewee
from datetime import datetime
from .. import database

pass_config = click.make_pass_decorator(Config)

@click.group()
@click.option('-q', '--quiet', is_flag=True, default=False, help="Don't prompt or display errors")
@click.option('-d', '--database', 'dbname', default=None, type=click.Path(exists=True, dir_okay=False, writable=True), help="Path to alternate database file")
@click.pass_context
def main(ctx, **kwargs):

	set_exception_handler(quiet=kwargs.get('quiet'))

	config  = Config(kwargs)
	ctx.obj = config

@main.command()
@click.option('-f', '--file', type=click.File('rb'), default='-')
@click.option('-i', '--id', default='E', help='Which property to record')
@pass_config
def store(config, file, id):

	config.load_data(file)
	db = config.db

	# TODO: This definitely doesn't belong in read_device.commands
	for data in config.data:
		meter, created = db.Meter.get_or_create(
			name=data['name'],
			location=db.Location(data['path']),
		)

		try:
			value = data['properties'][id]['value']
			db.Reading.create(meter=meter, value=value, property=id)
		except peewee.IntegrityError:
			# Value was probably null
			pass
		except KeyError:
			# Meter didn't return the property we were looking for
			pass
