#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os
import re
import sys

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

__author__  = 'Yuanze Wei'
__version__ = '0.1'
__doc__     = 'Module for get slice map'


def display(ARG_data, ARG_lineColor, ARG_lineOffset, ARG_lineLength):

    # create random data
    data = ARG_data

    # set different colors for each set of positions
    colors = np.array(ARG_lineColor)

    # set different line properties for each set of positions
    # note that some overlap
    lineoffsets = np.array(ARG_lineOffset)
    linelengths = ARG_lineLength

    fig, axs = plt.subplots()

    # create a vertical plot
    axs.eventplot(data, colors = colors, lineoffsets = lineoffsets, linelengths = linelengths, orientation = 'vertical')

    plt.show()


def getBlkInfo(ARG_blk, ARG_plane, ARG_blkSize, ARG_planeNum):

    goodBlk = []
    badBlk  = []
    for loopBadBlk in ARG_blk:
        if loopBadBlk:
            badBlk.append(int(loopBadBlk))

    for loopBlk in range(ARG_plane, ARG_blkSize, ARG_planeNum):
        if loopBlk not in badBlk:
            goodBlk.append(loopBlk)

    return badBlk, goodBlk


def main():

    blkAddr     = []
    dutPlane    = []
    lineLenth   = []
    lineOffset  = []
    listGoodBlk = []
    listBadBlk  = []
    lineColor   = []
    txtFiles = [name for name in os.listdir('./') if name.endswith('.txt')]
    for textLogName in txtFiles:
        waferNum = re.split(r'_', textLogName)
        with open(textLogName, 'rt') as datalogFile:
            for line in datalogFile:
                if re.match(r'HighWLDD0Screen[A-Za-z0-9_.\+\-\*\/\s]*BBKP', line):
                    splitColon  = re.split(r'\s*[:]\s*', line)
                    splitColon0 = splitColon[0]
                    splitColon1 = splitColon[1]
                    splitColon2 = splitColon[2]
                    listBlk     = re.split(r'\s*[\s]\s*', splitColon2)
                    splitSpace  = re.split(r'\s*[\s]\s*', splitColon0)
                    intDut      = int(splitSpace[1].replace('DUT', ''))
                    dutPlane.append(intDut)
                    dutPlane.append(intDut)
                    lineLenth.append(0.5)
                    lineLenth.append(0.5)
                    if splitSpace[2] == "BBKP0":
                        (listBadBlk, listGoodBlk) = getBlkInfo(listBlk, 0, 3916, 2)
                        blkAddr.append(listBadBlk)
                        blkAddr.append(listGoodBlk)
                        lineOffset.append(intDut-0.25)
                        lineOffset.append(intDut-0.25)
                        lineColor.append([1, 0, 0])
                        lineColor.append([0, 1, 0])
                    else:
                        (listBadBlk, listGoodBlk) = getBlkInfo(listBlk, 1, 3916, 2)
                        blkAddr.append(listBadBlk)
                        blkAddr.append(listGoodBlk)
                        lineOffset.append(intDut+0.25)
                        lineOffset.append(intDut+0.25)
                        lineColor.append([1, 0, 0])
                        lineColor.append([0, 1, 0])
    display(blkAddr, lineColor, lineOffset, lineLenth)


if __name__ == "__main__":
    main()
