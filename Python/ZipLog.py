#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os
from time import strftime

__author__  = 'Yuanze Wei'
__version__ = '0.1'
__doc__     = 'Module for zip/unzip log files'


def main():

    logDir = "C:\\0_Mine\\Github\\Python\\logs"

    # compress
    # >>> 7z x -tzip -y xx-13.zip
    # uncompress
    # >>> 7z a -tzip -r xx.zip a\* b\*

    zipProgram = "7z a -tzip -r"
    unzipProgram = "7z x -tzip -y"

    for files in os.listdir(logDir):
        if files.endswith('.log'):
            fileZip = files + "." + strftime("%Y-%m-%d") + ".zip"
            print(files, fileZip)
            os.chdir(logDir)
            os.system(zipProgram + " " +  fileZip +" "+ files)
            os.remove(files)


if __name__ == "__main__":
    main()
