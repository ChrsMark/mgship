# -*- coding: utf-8 -*-
from __future__ import absolute_import

import click

from mgship import mgship
from mgship.destination import csv


@click.command()
def main(args=None):
    """Console script for mgship"""

    mgship.Archive(csv.Destination()).ship()


if __name__ == "__main__":
    main()
