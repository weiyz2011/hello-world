##=======================================================================
## Copyright 2018 SanDisk Corporation.
## All Rights Reserved. Unpublished -
## all rights reserved under the copyright laws of the United States.
## USE OF A COPYRIGHT NOTICE IS PRECAUTIONARY ONLY AND DOES NOT IMPLY
## PUBLICATION OR DISCLOSURE.
##
## THIS SOFTWARE CONTAINS CONFIDENTIAL INFORMATION AND TRADE SECRETS OF
## SANDISK CORPORATION. USE, DISCLOSURE, OR REPRODUCTION IS PROHIBITED
## WITHOUT THE PRIOR EXPRESS WRITTEN PERMISSION OF SANDISK CORPORATION.
## AUTHOR: CHAMPION ZHOU 2019.05.03
## 2019.05.07 Initial release
## 2019.05.09 Add Wafer ID print
##=======================================================================
import re
import os
import os.path
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

#########################################################################
Version=1.1
raw_path=os.getcwd()
file_new=''
old_waferid = []
new_waferid = []

def autoMergeCSV(csvfloder):
        getprogramversion = 2
        raw_path=os.getcwd()+"\\"+csvfloder
        files_path=[]
        row=[]
        titles2 = ''
        cellcia = 0
        for root, dirs, files in os.walk(raw_path):
                for file in files:
                        file_path=os.path.join(root, file)
                        if file_path[-5:].lower()=='p.csv':
                                files_path.append(file_path)

        file_new=raw_path+"/"+csvfloder+"_all.csv"
        
        f_new=open(file_new,"w")
        isFirstFile=True

        for file_old in files_path:

                f_old=open(file_old)
                rownum = 0
                cellcia = 0
                if re.search("-\d\d\w\w_",file_old):
                        if re.search("SBI1",file_old):
                                cellcia = 1
                if not isFirstFile: #skip two lines if not first file
                        f_old.readline()
                        f_old.readline()
                else:
                        titles1 = f_old.readline()
                        f_new.write(titles1)
                        titles2 = f_old.readline()
                        titles2 = titles2.replace("[pcs]", '')
                        titles2 = titles2.replace("[ua]", '')

                        if cellcia == 0:
                                row = titles2.split(',')
                                row.pop(22)
                                row.pop(22)
                                row.pop(22)
                                titles2 = ''
                                for r in row:
                                        if r != "\n":
                                                titles2=titles2+r+','
                                titles2=titles2+'\n'
                        f_new.write(titles2)

                isFirstFile=False
                while True:
                        row = ''
                        titles2 = f_old.readline()
                        rownum += 1
                        if not titles2:
                                break
                        if titles2== '\n':
                                continue
                        if cellcia == 0:
                                row = titles2.split(',')
                                #print (rownum)
                                row.pop(22)
                                row.pop(22)
                                row.pop(22)
                                titles2 = ''
                                for r in row:
                                        if r != "\n":
                                                titles2=titles2+r+','
                                titles2=titles2+'\n'
                        f_new.write(titles2)
                        
                        row = titles2.split(',')        #program version

                        if getprogramversion == 2:
                                if re.search("new",csvfloder):
                                        print (row[1])
                                        new_waferid.append('Rev'+row[1][-3:-1]+':')
                                if re.search("old",csvfloder):
                                        print (row[1])
                                        old_waferid.append('Rev'+row[1][-3:-1]+':')
                                getprogramversion = 1

                searchObj = re.search( r'KGD_CharData_(.*)_\d', file_old, re.M|re.I)
                if searchObj:
                        if re.search("new",csvfloder):
                                new_waferid.append(searchObj.group(1))
                        if re.search("old",csvfloder):
                                old_waferid.append(searchObj.group(1))
                else:
                        print ("Nothing found!!")

                f_old.close()
        f_new.close()

autoMergeCSV('new')
autoMergeCSV('old')


old_version = []
fail_bin_dut = []
bin_sum_old = []
bin_sum_old_percent = []
bin_sum_new = []
bin_sum_new_percent = []
map_ids_old = []
map_ids_new = []
map_ids = []
old_version = []
new_version = []

for num in range(0,1000):
        map_ids_old.append('')
        map_ids_new.append('')
        bin_sum_old.append(0)
        bin_sum_old_percent.append(0.00)
        bin_sum_new.append(0)
        bin_sum_new_percent.append(0.00)

file_new=os.getcwd()+"\\old"+"/old_all.csv"

row_index = 0
with open(file_new,"r") as f:
    for line in f:
        row = line.split(',')
        row_index += 1
        if row_index >2:
                fail_bin_dut.append(row[17])
                map_ids_old[int(row[17])] = row[16]
                bin_sum_old[int(row[17])] += 1

for num in range(0,500):
        if bin_sum_old[num] != 0:
                bin_sum_old_percent[num] = bin_sum_old[num]/(row_index-2)

file_new=os.getcwd()+"\\new"+"/new_all.csv"

row_index = 0
with open(file_new,"r") as f:
    for line in f:
        row = line.split(',')
        row_index += 1
        if row_index >2:
                fail_bin_dut.append(row[17])
                map_ids_new[int(row[17])] = row[16]
                bin_sum_new[int(row[17])] += 1

for num in range(0,500):
        if bin_sum_new[num] != 0:
                bin_sum_new_percent[num] = bin_sum_new[num]/(row_index-2)

index_fail_count = 0
for num in range(0,169):
        if bin_sum_new[num] != 0 or bin_sum_old[num] != 0:
                old_version.append(0.00)
                new_version.append(0.00)
                old_version[index_fail_count] = round(bin_sum_old_percent[num]*100,2)
                new_version[index_fail_count] = round(bin_sum_new_percent[num]*100,2)
                if bin_sum_new[num] != 0:
                        map_ids.append(map_ids_new[num])
                elif bin_sum_old[num] != 0:
                        map_ids.append(map_ids_old[num])
                index_fail_count += 1

ind = np.arange(len(old_version))  # the x locations for the groups
width = 0.35  # the width of the bars
mpl.rcParams["figure.figsize"]=(10.0,5.0)
mpl.rcParams["figure.subplot.left"]=0.1
mpl.rcParams["figure.subplot.right"]=0.9
mpl.rcParams["figure.subplot.bottom"]=0.3
mpl.rcParams["figure.subplot.top"]=0.88
mpl.rcParams["figure.subplot.wspace"]=0.7
mpl.rcParams["figure.subplot.hspace"]=0.7
fig, ax = plt.subplots()
old_label='old'+str(row_index)

titles3 = ''
titles4 = ''
for r in old_waferid:
        if r != "\n":
                titles3=titles3+r+"\n"
for r in new_waferid:
        if r != "\n":
                titles4=titles4+r+"\n"

rects1 = ax.bar(ind - width/2, old_version, width,
                color='SkyBlue', label=titles3)
rects2 = ax.bar(ind + width/2, new_version, width,
                color='IndianRed', label=titles4)

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Yield Loss %')
ax.set_title('BIN COMPARE')
ax.set_xticks(ind)
ax.set_xticklabels(map_ids)
plt.xticks(rotation=60)
mpl.rcParams["font.size"]=6.0
ax.legend()

def autolabel(rects, xpos='center'):
    xpos = xpos.lower()  # normalize the case of the parameter
    ha = {'center': 'center', 'right': 'right', 'left': 'left'}
    offset = {'center': 0.5, 'right': 0.57, 'left': 0.43}  # x_txt = x + w*off

    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()*offset[xpos], 1.0*height,
                '{}'.format(height), ha=ha[xpos], va='bottom')

autolabel(rects1, "center")
autolabel(rects2, "center")

plt.savefig('./bin2bin.png',dpi=300)

plt.show()
