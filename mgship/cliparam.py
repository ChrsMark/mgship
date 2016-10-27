# -*- coding: utf-8 -*-
"""Custom parameter types for CLI."""
from __future__ import absolute_import

import click
import logging

from mgship.util import fromtimestamp
from mgship.email import is_email


class DateTime(click.ParamType):
    """Custom DateTime parameter type for the CLI.

    Currently only UNIX timestamps are supported as input.  Float values, with
    sub-second precision, are permitted but rounded to the nearest int.
    """
    name = "Timestamp"

    def convert(self, value, param, ctx):
        if value is None:
            return None
        try:
            num = float(value)
            return fromtimestamp(num)
        except ValueError:
            self.fail("{} is not a valid timestamp.".format(value))


class Loglevel(click.Choice):
    _LEVEL_NAMES = ['ERROR', 'WARNING', 'INFO', 'DEBUG']
    name = "Log level"

    def __init__(self, *args, **kwargs):
        super(Loglevel, self).__init__(self._LEVEL_NAMES, *args, **kwargs)

    def convert(self, value, param, ctx):
        value = super(Loglevel, self).convert(value, param, ctx)
        try:
            if value is not None:
                return getattr(logging, value)
        except AttributeError:
            self.fail("Unknown log level {}".format(value))


class Email(click.ParamType):
    """Validate an email address."""
    name = "Email"

    def convert(self, value, param, ctx):
        value = super(Email, self).convert(value, param, ctx)
        try:
            if value is not None:
                is_email(value)
                return value
        except ValueError as e:
            self.fail("Invalid email: {}".format(e))
