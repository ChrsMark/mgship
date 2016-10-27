# -*- coding: utf-8 -*-
"""Main action classes for mgship."""
from __future__ import absolute_import
import attr

from mgship.api import Client
from mgship.events import mg_past_events
from mgship.util import validate_past
from mgship.log import logger


@attr.s
class Archive(object):
    """Ship all existing events."""
    dest = attr.ib()
    begin = attr.ib(default=None,
                    validator=attr.validators.optional(
                        lambda i, a, v: validate_past(v)))
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
