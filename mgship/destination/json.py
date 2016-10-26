"""Print events to the console as JSON."""
from __future__ import absolute_import
import sys
import json


from contextlib import contextmanager

__all__ = ['Destination']


def print_events():
    eid = None
    while True:
        event = yield eid
        print json.dumps(event)


def make_sink():
    sink = print_events()
    next(sink)
    yield sink

Destination = contextmanager(make_sink)
