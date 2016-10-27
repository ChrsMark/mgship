# -*- coding: utf-8 -*-
"""Various utilities for emails."""
from __future__ import absolute_import

from email_validator import validate_email, EmailNotValidError


def is_email(value):
    try:
        validate_email(value, check_deliverability=False)
    except EmailNotValidError as e:
        raise ValueError(str(e))
