# -*- coding: utf-8 -*-
"""Mailgun Event API Data Structure methods.

Based on: https://documentation.mailgun.com/api-events.html#event-structure
"""
import datetime


__all__ = ['get_date', 'get_recipient']


def get_date(event):
    """Get the calendar date of this event."""
    ts = datetime.fromtimestamp(event['timestamp'])
    return ts.date()


def get_recipient(event):
    """Get the recipient related to this event."""
    message = event.get('message', {})
    headers = message.get('headers', {})
    if 'to' in headers:
        return headers['to']
    return event.get('recipient')
