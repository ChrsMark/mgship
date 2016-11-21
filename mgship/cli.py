# -*- coding: utf-8 -*-
"""MgShip CLI classes."""
from __future__ import absolute_import

import os
import click
import logging

from mgship import mgship
from mgship.destination import csv, json
from mgship.cliparam import DateTime, Loglevel, Email
from mgship.util import utctimestamp, is_past
from mgship.log import logger


def to_timestamp(ctx, param, value):
    if value is None:
        return None
    try:
        value = utctimestamp(value)
        if ctx.info_name == 'archive':
            is_past(value)
        return value
    except (TypeError, ValueError) as e:
        logger.debug("bad timestamp parameter", exc_info=True)
        raise click.BadParameter(unicode(e))


@click.command()
@click.option('--log-level', default=None, type=Loglevel())
@click.option('--format', default='csv', type=click.Choice(['json', 'csv']),
              help='the output format')
@click.option('--past', is_flag=True,
              help='search past events instead of new ones.')
@click.option('--output', default='-', type=click.File('wb'))
@click.option('--event', default=None, type=str, help='event type')
@click.option('--sleep', default=None, type=int,
              help='how much to wait before repeating requests')
@click.option('--begin', default=None, type=DateTime(),
              callback=to_timestamp,
              help='when to start the process, as unix timestamp')
@click.option('--recipient', default=None, type=Email(),
              help='email address of recipient')
@click.option('--filter', default=None,
              help='key value filters')
def main(log_level, format, past, output, *args, **kwargs):
    output = os.fdopen(output.fileno(), 'wb', 0)

    if log_level is not None:
        logging.basicConfig(level=log_level)
    dest = csv.Destination if format == 'csv' else json.Destination
    if past is True:
        mgship.Archive(dest(output), *args, **kwargs).ship()
    else:
        mgship.Monitor(dest(output), *args, **kwargs).ship()


if __name__ == "__main__":
    main()
