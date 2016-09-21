"""Index events into python dicts."""
from __future__ import absolute_import
import attr

from mgship.data.event import get_date, get_recipient


__all__ = ['Destination']


INDEX_FUNCTION = {
   'date': get_date,
   'address': get_recipient
}


def mg_index_events(cache):
    """Create an index of mailgun events.

    Example to print the type for each event related to 'john@hotmail.com':

        from itertools import islice
        index = mg_index_events(islice(mg_past_events(), 1000))
        events = index['address']['john@hotmail.com'].values()
        for event in events:
            print "{} at {}".format(event['event'], event['timestamp'])

    Prints:

        delivered at 1471365467.82
        accepted at 1471365467.06

    """

    eid = None
    while True:
        event = yield eid
        eid = event['id']
        for name, func in INDEX_FUNCTION.items():
            key = func(event)
            if key is not None:
                index = cache.setdefault(name, {})
                index.setdefault(key, {})[eid] = event


@attr.s
class Destination(object):
    _cache = attr.ib(default=dict, repr=False)

    def open(self):
        return mg_index_events(self._cache)

    def __enter__(self):
        return self.open()

    def __exit__(self, type, value, traceback):
        return
