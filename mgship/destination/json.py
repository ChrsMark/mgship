"""Print events to the console as JSON."""
from __future__ import absolute_import
import sys
import json


from contextlib import contextmanager

__all__ = ['Destination']


def print_events(file):
    eid = None
    while True:
        event = yield eid
        json.dump(event, file, indent=2)


def make_sink(file=sys.stdout):
    try:
        sink = print_events(file)
        next(sink)
        yield sink
    finally:
        file.flush()

Destination = contextmanager(make_sink)
