# -*- coding: utf-8 -*-
"""MgShip CLI classes."""
from __future__ import absolute_import

import click
import logging

from mgship import mgship
from mgship.destination import csv, json
from mgship.cliparam import DateTime, Loglevel
from mgship.util import utctimestamp, validate_past
from mgship.log import logger


@click.group()
@click.option('--log-level', default=None, type=Loglevel())
def main(log_level=None):
    """Console script for mgship"""
    if log_level is not None:
        logging.basicConfig(level=log_level)


def to_timestamp(ctx, param, value):
    if value is None:
        return None
    try:
        value = utctimestamp(value)
        if ctx.info_name == 'archive':
            validate_past(value)
        return value
    except (TypeError, ValueError) as e:
        logger.debug("bad timestamp parameter", exc_info=True)
        raise click.BadParameter(unicode(e))


@main.command()
@click.option('--format', default='csv', type=click.Choice(['json', 'csv']),
              help='the output format')
@click.option('--begin', default=None, type=DateTime(),
              callback=to_timestamp,
              help='when to start archiving, as unix timestamp')
def archive(format, *args, **kwargs):
    dest = csv.Destination() if format == 'csv' else json.Destination()
    mgship.Archive(dest, *args, **kwargs).ship()


if __name__ == "__main__":
    main()
