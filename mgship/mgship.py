# -*- coding: utf-8 -*-
"""Main action classes for mgship."""
from __future__ import absolute_import
import attr

from functools import wraps

from mgship.api import Client
from mgship.events import mg_past_events
from mgship.util import is_past
from mgship.log import logger


def mg_field_validator(wrapped):
    """Convert a simple validator method to a attr.ib validator.

    Given a method which accepts a value and possibly raises ValueError
    create a attr compatible validator that accepts empty values.
    """
    @attr.validators.optional
    @wraps(wrapped)
    def wrapper(*args, **kwargs):
        return wrapped(*args[2:], **kwargs)
    return wrapper


@attr.s
class Archive(object):
    """Ship all existing events."""
    dest = attr.ib()
    begin = attr.ib(default=None, validator=mg_field_validator(is_past))
    _client = attr.ib(default=attr.Factory(Client), repr=False)
    _filtered_params = ['dest', '_client']

    @classmethod
    def _filter_params(self, attr, value):
        if attr.name in self._filtered_params or value is None:
            return False
        return True

    def _iter_sink(self, sink):
        kwargs = attr.asdict(self, filter=self._filter_params)
        logger.info("starting archive ({})".format(kwargs))
        for event in mg_past_events(client=self._client, **kwargs):
            yield sink.send(event)

    def ship(self):
        with self.dest as sink:
            for _ in self._iter_sink(sink):
                pass


@attr.s
class Monitor(object):
    """Monitor current events."""
