# Copyright 2015 University of Edinburgh
# Licensed under GPLv3 - see README.md for information

import click

from ..config import MetersConfig as Config
from ..helpers import set_exception_handler

import peewee
from datetime import datetime
from .. import database

pass_config = click.make_pass_decorator(Config)

@click.group()
@click.option('-q', '--quiet', is_flag=True,
    default=False, help="Don't prompt or display errors")
@click.option('-d', '--debug', is_flag=True,
    default=False, help="Display full debugging information and stack traces")
@click.option('-d', '--database', 'dbname',
    default=None, type=click.Path(exists=True, dir_okay=False, writable=True),
    help="Path to alternate database file")
@click.pass_context
def main(ctx, **kwargs):
    """
    Store and query meter values

    read-device Copyright 2015 University of Edinburgh.
    See <https://github.com/lewiseason/read-device> for information
    """

    set_exception_handler(quiet=kwargs.get('quiet'), debug=kwargs.get('debug'))

    config  = Config(kwargs)
    ctx.obj = config

@main.command()
@click.option('-f', '--file', type=click.File('rb'), default='-')
@click.option('-i', '--id', default='E', help='Which property to record')
@pass_config
def store(config, file, id):

    config.load_data(file)
    db = config.db

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

@main.command()
@click.option('-s', '--start', help='Start of time range to summarise.', required=True)
@click.option('-e', '--end', help='End of time range - default is now.', default=datetime.now())
@pass_config
def usage(config, start, end):
    """ Show usage of all meters over a given date range """

    db = config.db

    results = db.db.execute_sql('''
        SELECT id, name, (
            SELECT value
            FROM (
              SELECT value, MIN(ABS(strftime('%s', (?)) - strftime('%s', timestamp)))
              FROM reading
              WHERE reading.meter_id = meter.id
              GROUP BY meter_id
              )
            ) AS openingValue, (
            SELECT value
            FROM (
              SELECT value, MIN(ABS(strftime('%s', (?)) - strftime('%s', timestamp)))
              FROM reading
              WHERE reading.meter_id = meter.id
              GROUP BY meter_id
              )
            ) AS closingValue
        FROM meter;

    ''', (start, end))

    for row in results:
        meter_id, name, openingValue, closingValue = row
        try:
            delta = closingValue - openingValue
        except TypeError:
            delta = '???'

        print ("%35s   %s kWh" % (name, delta))
