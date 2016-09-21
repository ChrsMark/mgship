# -*- coding: utf-8 -*-
from __future__ import absolute_import
import attr

from mgship.api import Client
from mgship.events import mg_past_events


@attr.s
class Archive(object):
    """Ship all existing events."""
    dest = attr.ib()
    _client = attr.ib(default=attr.Factory(Client), repr=False)

    def _iter_sink(self, sink):
        for event in mg_past_events(client=self._client):
            yield sink.send(event)

    def ship(self):
        with self.dest as sink:
            for _ in self._iter_sink(sink):
                pass
