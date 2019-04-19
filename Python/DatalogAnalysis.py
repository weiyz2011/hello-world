#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os
import re
import sys

__author__  = 'Yuanze Wei'
__version__ = '0.1'
__doc__     = 'Module for datalog analysis'


class Die(object):
    """ Define a NAND Die having FBC data

    Arguments
    ----------
    fname: fileName
        Full path of filename

    detailInfo: dict
        Any additional attributes to add to the Die definition.
        e.g. {'fab':'SDSS', 'date':'2018-07-31'}

    Note
    ----------
    At the time of defining Die, either fname or bics number should be given

    """
    def __init__(self, fileName = None, detailInfo = None):
        assert fileName or detailInfo, 'fileName or detailInfo must be given.'
        ## no file name, but bics number is given
        if not fileName:
            if detailInfo:
                assert isinstance(detailInfo, dict), 'detailInfo must be dictionary.'
                for progKey, progValue in detailInfo.items():
                    setattr(self, progKey, progValue)

        ## when a file name is given
        else:
            pass

    def getInfo(self, fileName = None):
        pass
