"""Print events to the console as CSV."""
from __future__ import absolute_import
import sys
import csv


from contextlib import contextmanager

__all__ = ['Destination']


def print_events():
    eid = None
    writer = csv.writer(sys.stdout)
    while True:
        event = yield eid
        envelope = event.get('envelope', {})
        writer.writerow([
            ','.join(event.get('tags', [])),
            envelope.get('sender', ''),
            envelope.get('targets', ''),
            event.get('event', ''),
            event.get('timestamp', '')])


def make_sink():
    sink = print_events()
    next(sink)
    yield sink

Destination = contextmanager(make_sink)
