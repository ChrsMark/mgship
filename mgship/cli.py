# -*- coding: utf-8 -*-
from __future__ import absolute_import

import click

from mgship import mgship
from mgship.destination import console


@click.command()
def main(args=None):
    """Console script for mgship"""

    mgship.Archive(console.Destination()).ship()


if __name__ == "__main__":
    main()
