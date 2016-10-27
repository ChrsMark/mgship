# -*- coding: utf-8 -*-
"""Mailgun event library.

Set an environment variable `MAILGUN_API_KEY` and then, for example:

    filters = {"event": "opened"}
    for event in mg_poll_events(max_age=10, sleep=5, limit=200, **filters):
        print event

    filters = {"message-id": "20160818145242.10544.2438@be15.transifex.com"}
    for event in mg_past_events(sleep=1, limit=200, max_retries=5, **filters):
        print event

    index = mg_index_events(mg_past_events(max_retries=5))
    print index['address']['john@hotmail.com']

"""
from __future__ import absolute_import
import logging

from urllib import urlencode
from mgship.util import utctimestamp, timeago
from mgship.page import Page

BASE_URL = 'https://api.mailgun.net/v3/transifex.com'
EVENTS_URL = BASE_URL + '/events'


log = logging.getLogger(__name__)


def events_url(**kwargs):
    return EVENTS_URL + "?" + urlencode(kwargs)


def mg_poll_events(client=None, max_age=1800, sleep=900, rewind=None,
                   max_retries=None, **kwargs):
    """Poll for events.

    Example:

        events = mg_poll_events(max_age=100, sleep=30, rewind=100)
        for e in itertools.islice(events, 1000):
            print "{}: {}".format(e['event'], get_recipient(e))

    """

    if rewind is None:
        rewind = max_age

    if 'begin' not in kwargs:
        begin = kwargs['begin'] = utctimestamp(timeago(seconds=rewind))
    else:
        begin = kwargs['begin']

    url = events_url(ascending="yes", **kwargs)

    log.debug("Polling for events")
    log.debug("max_age=%d, sleep=%d, begin=%d", max_age, sleep, begin)

    while True:
        page = Page(url, client=client, max_age=max_age, sleep=sleep,
                    max_retries=max_retries)
        for event in page:
            yield event
        if url == page.next:
            break
        url = page.next


def mg_past_events(begin=None, client=None, sleep=600,
                   max_retries=None, **kwargs):
    if begin is None:
        begin = utctimestamp()
    url = events_url(ascending="no", begin=begin, **kwargs)
    log.debug("Starting pager: %s", url)
    while True:
        page = Page(url, max_age=None, client=client, sleep=sleep,
                    max_retries=max_retries)
        for event in page:
            yield event
        if url == page.next:
            break
        url = page.next
