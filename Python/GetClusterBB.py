#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

__author__  = 'Yuanze Wei'
__version__ = '1.0'
__doc__     = 'Module for get cluster BB'

import re
import sys
import os
from pyecharts import Scatter, Page


def clusterBlk(ARG_blk):

    countClusterBlk = 0
    countMax = 0
    for loopBlk in ARG_blk:
        if loopBlk:
            intBLK = int(loopBlk)
            if countClusterBlk == 0:
                preBlk = intBLK
                countClusterBlk = 1
            else:
                postBlk = intBLK
                if (postBlk == preBlk + 2):
                    preBlk = postBlk
                    countClusterBlk += 1
                else:
                    if countMax < countClusterBlk:
                        countMax = countClusterBlk
                    preBlk = postBlk
                    countClusterBlk = 1
    return countMax


def paddingBlk(ARG_blk):

    postPaddingBlk = []
    countClusterBlk = 0
    for loopBlk in ARG_blk:
        if loopBlk:
            intBLK = int(loopBlk)
            postPaddingBlk.append(intBLK)
            if countClusterBlk == 0:
                preBlk = intBLK
                startBlk = preBlk
                countClusterBlk = 1
            else:
                postBlk = intBLK
                if (postBlk == preBlk + 2):
                    preBlk = postBlk
                    endBlk = postBlk
                    countClusterBlk += 1
                else:
                    if countClusterBlk >= 3:
                        postPaddingBlk.append(startBlk if (startBlk - 2 <    0) else startBlk - 2)
                        postPaddingBlk.append(endBlk   if (endBlk   + 2 > 1980) else endBlk   + 2)
                    endBlk = postBlk
                    startBlk = postBlk
                    preBlk = postBlk
                    countClusterBlk = 1
    postPaddingBlk = list(set(postPaddingBlk))
    postPaddingBlk.sort()
    return postPaddingBlk


def main():

    dutPl0 = []
    dutpl1 = []
    maxCntPl0 = []
    maxCntPl1 = []
    page = Page("Cluster Padding Figure")
    txtFiles = [name for name in os.listdir('./') if name.endswith('.txt')]
    for textLogName in txtFiles:
        waferNum = re.split(r'_', textLogName)
        with open(textLogName, 'rt') as clusterFile:
            for line in clusterFile:
                if re.match(r'IncomingBBKCount[A-Za-z0-9_.\+\-\*\/\s]*BBKP', line):
                    splitColon  = re.split(r'\s*[:]\s*', line)
                    splitColon1 = splitColon[0]
                    splitColon2 = splitColon[1]
                    splitColon3 = splitColon[2]
                    listBlk     = re.split(r'\s*[\s]\s*', splitColon3)
                    padBlk = paddingBlk(listBlk)
                    maxCnt = clusterBlk(padBlk)
                    splitSpace = re.split(r'\s*[\s]\s*', splitColon1)
                    intDut = int(splitSpace[1].replace('DUT', ''))
                    if splitSpace[2] == "BBKP0":
                        dutPl0.append(intDut)
                        maxCntPl0.append(maxCnt)
                    else:
                        dutpl1.append(intDut)
                        maxCntPl1.append(maxCnt)
        scatter = Scatter(waferNum[2])
        scatter.add("PL0", dutPl0, maxCntPl0, xaxis_name = "DUT", yaxis_name = "Max Padding BB", is_more_utils = True)
        scatter.add("PL1", dutpl1, maxCntPl1, xaxis_name = "DUT", yaxis_name = "Max Padding BB", is_more_utils = True)
        page.add(scatter)
    page.render()


if __name__ == "__main__":
    main()