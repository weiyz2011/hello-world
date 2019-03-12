#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os
import re
import sys

__author__  = 'Yuanze Wei'
__version__ = '0.3'
__doc__     = 'Module for uncompress slice map'


def main():

    path = os.path.abspath('./logs/')
    listFiles = [name for name in os.listdir('./logs/') if name.endswith('.dat4.dat')]
    for fileLocR in listFiles:
        fileLocW = fileLocR.replace('.dat4.dat', '.dat4.txt')
        with open(os.path.join(path, fileLocR), 'rb') as f:
            fileRead = f.read()                                 # Move read point to file end
            filesize = f.tell()                                 # File point location
            f.seek(0, 0)                                        # Set file read point to begining
            readPoint = 0
            readOffset = 1
            isBlkColumn = 0
            with open(os.path.join(path, fileLocW), 'w+') as w:
                w.write("// X   Y B BBK CRD DUT Num : PL0_ColAdr : PL1_ColAdr : BlkAdr\n")
                w.write("#")
                while readPoint < filesize:
                    if readOffset == 1:
                        dataRead = f.read(readOffset)
                        if ord(dataRead) == 0xFF:
                            readOffset = 11
                            isBlkColumn = 0
                            w.write("\n")
                            continue
                        else:
                            if ord(dataRead) == 0x2C:           # ','
                                isBlkColumn = 1
                                badBlkColumnCnt = 0
                            if isBlkColumn == 1:
                                if ord(dataRead) == 0x42:       # 'B', Bad block address
                                    badBlkColumnCnt += 1
                                if ord(dataRead) == 0x43:       # 'C', bad column address PL0 and PL1
                                    badBlkColumnCnt += 2
                            w.write("%c" % ord(dataRead))
                    elif readOffset == 11:
                        dataRead = f.read(readOffset)
                        readOffset = 2
                        w.write("  %02d  %02d%02x%02x%02x%02x%02x%02x%02x%02x%02x : " % (dataRead[0], dataRead[1], dataRead[2], \
                                                                                         dataRead[4], dataRead[3], dataRead[6], \
                                                                                         dataRead[5], dataRead[8], dataRead[7], \
                                                                                         dataRead[10], dataRead[9]))
                        if badBlkColumnCnt == 1:
                            w.write(": : ")
                    elif readOffset == 2:
                        badBlkColumnLoop = badBlkColumnCnt
                        while badBlkColumnLoop > 0:
                            dataRead = f.read(readOffset)
                            if int(dataRead[0]) == 0xFF and int(dataRead[1]) == 0xFF:
                                if badBlkColumnLoop == 1:
                                    if badBlkColumnCnt == 2:
                                        w.write(" : :\n")
                                    if badBlkColumnCnt == 3 or badBlkColumnCnt == 1:
                                        w.write(" :\n")
                                    readPoint = f.tell()
                                    dataRead = f.read(readOffset)
                                    if int(dataRead[0]) == 0xFF and int(dataRead[1]) == 0xFF:
                                        readOffset = 1
                                        if readPoint + 2 < filesize:
                                            w.write("#")
                                    else:
                                        readOffset = 11
                                        f.seek(readPoint, 0)    # Set file read point back to before 2 bytes
                                else:
                                    w.write(" : ")
                                badBlkColumnLoop -= 1
                            else:
                                w.write("%02x" % int(dataRead[1]))
                                w.write("%02x" % int(dataRead[0]))
                    else:
                        print('Error read offset!')
                    readPoint = f.tell()
        print("%d bytes uncompress done!" % filesize)


if __name__ == "__main__":
    main()
