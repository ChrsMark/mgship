"""Print events to the console as CSV."""
from __future__ import absolute_import
import sys
import csv

from contextlib import contextmanager

from mgship.log import logger
from mgship.data.event import get_recipient

__all__ = ['Destination']


def print_events():
    eid = None
    writer = csv.writer(sys.stdout)
    while True:
        event = yield eid
        envelope = event.get('envelope', {})
        writer.writerow([
            event.get('id', ''),
            ','.join(event.get('tags', [])),
            envelope.get('sender', ''),
            get_recipient(event) or '',
            event.get('event', ''),
            event.get('timestamp', '')])


def make_sink():
    try:
        sink = print_events()
        next(sink)
        yield sink
    except IOError:
        logger.exception("Couldn't write output")

Destination = contextmanager(make_sink)
