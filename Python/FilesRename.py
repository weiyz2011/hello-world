#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os
import re
import sys

__author__  = 'Yuanze Wei'
__version__ = '0.1'
__doc__     = 'Module for rename files name'


def main():

    path = os.path.abspath('./logs/')
    for fileName in [name for name in os.listdir('./logs/') if name.endswith('.dat4.dat1')]:
        newFileName = fileName.replace('.dat4.dat1', '.dat4.dat')
        os.rename(os.path.join(path, fileName), os.path.join(path, newFileName))


if __name__ == "__main__":
    main()
