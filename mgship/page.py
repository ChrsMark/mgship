# -*- coding: utf-8 -*-
"""Mailgun REST API Paging."""
from __future__ import absolute_import
import attr
import time
import logging

from itertools import count

from mgship.api import Client
from mgship.util import utctimestamp


__all__ = ['Page']


log = logging.getLogger(__name__)


@attr.s
class Page(object):
    url = attr.ib()
    max_retries = attr.ib(default=None)
    client = attr.ib(default=attr.Factory(Client))
    max_age = attr.ib(default=0)
    sleep = attr.ib(default=0)
    _seen = attr.ib(default=attr.Factory(set), init=False)
    _last = attr.ib(init=False, default=None)
    _next = attr.ib(init=False, default=None)

    @property
    def next(self):
        return self._next

    def _filter_seen(self, items):
        for item in items:
            if item['id'] in self._seen:
                continue
            self._seen.add(item['id'])
            self._last = max(item['timestamp'], self._last)
            yield item

    def _attempts(self):
        for attempt in count(1):
            if self.max_retries is not None and attempt > self.max_retries:
                break
            if attempt > 1 and self.sleep > 0:
                log.debug("sleeping %d seconds", self.sleep)
                time.sleep(self.sleep)
            log.debug("attempt %d/%s", attempt, self.max_retries)
            yield attempt
            if self.max_age is not None and self.age > self.max_age:
                break
            if self.max_age is None and self.next != self.url:
                break

    def __iter__(self):
        for _ in self._attempts():
            page = self.client.get(self.url)
            for item in self._filter_seen(page['items']):
                yield item
            self._next = page['paging']['next']
            if self.age > 0:
                log.debug("page last updated %d seconds ago", self.age)
            else:
                log.debug("no new results")

    @property
    def age(self):
        if self._last is None:
            return -1
        return utctimestamp() - self._last
