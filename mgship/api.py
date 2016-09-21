# -*- coding: utf-8 -*-
"""Simple Mailgun REST API Client."""
from __future__ import absolute_import
import os
import attr
import requests
import logging


__all__ = ['Client']


log = logging.getLogger(__name__)


def mg_auth(api_key=None):
    if api_key is None:
        api_key = os.environ.get('MAILGUN_API_KEY')
    return ("api", api_key)


@attr.s
class Client(object):
    auth = attr.ib(default=attr.Factory(mg_auth), repr=False)

    def get(self, url):
        try:
            log.debug("%s.get(%s)", self, url)
            r = requests.get(url, auth=self.auth)
            r.raise_for_status()
        except Exception:
            log.exception("%s.get(%s) failed", self, url)
            raise
        return r.json()
