# -*- coding: utf-8 -*-
"""Various utilities for mgship."""
from __future__ import absolute_import

import calendar

from datetime import datetime, timedelta

__all__ = ['utctimestamp', 'timenow', 'timeago', 'fromtimestamp',
           'validate_past']


def utctimestamp(now=None):
    """Convert a UTC datetime object to a timestamp."""
    if now is None:
        now = datetime.utcnow()
    return int(calendar.timegm(now.timetuple()))


def fromtimestamp(timestamp):
    return datetime.utcfromtimestamp(int(timestamp))


timenow = datetime.utcnow


def timeago(**kwargs):
    return timenow() - timedelta(**kwargs)


def validate_past(value):
    """Validator for timestamps in the past.

    Raises ValueError if value is not a timestamp that represents
    a time in the past.
    """
    if value >= utctimestamp():
        raise ValueError("argument must be in the past")
