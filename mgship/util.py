# -*- coding: utf-8 -*-
"""Various utilities for mgship."""

import calendar

from datetime import datetime, timedelta

__all__ = ['utctimestamp', 'timeago']


def utctimestamp(now=None):
    """Convert a UTC datetime object to a timestamp."""
    if now is None:
        now = datetime.utcnow()
    return int(calendar.timegm(now.timetuple()))


def timeago(**kwargs):
    return datetime.utcnow() - timedelta(**kwargs)
