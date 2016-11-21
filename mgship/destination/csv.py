"""Print events to the console as CSV."""
from __future__ import absolute_import
import sys
import csv

from contextlib import contextmanager

from mgship.log import logger
from mgship.data.event import (
    get_recipient, get_subject, get_size)

__all__ = ['Destination']


def print_events(file):
    eid = None
    writer = csv.writer(file)
    while True:
        event = yield eid
        envelope = event.get('envelope', {})
        writer.writerow([
            event.get('id', ''),
            ','.join(event.get('tags', [])),
            envelope.get('sender', ''),
            get_recipient(event) or '',
            event.get('event', ''),
            event.get('timestamp', ''),
            get_size(event),
            get_subject(event)])


def make_sink(file=sys.stdout):
    try:
        sink = print_events(file)
        next(sink)
        yield sink
    except IOError:
        logger.exception("Couldn't write output")
    finally:
        file.flush()

Destination = contextmanager(make_sink)
