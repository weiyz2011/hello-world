import os, re

dict_dbp = dict()
raw_datalog = 'WLC_LOG_MF64I003D0_01P_Z0AAA000AA_20181217164324_1_S2.txt'
out_name = 'leak_schmoo.txt'

# print('read middle file...')
# with open('output.dat', 'r') as FR:
#     for line in FR:
#         line_list = line.strip().split(' ')
#         if len(line_list) == 4:
#             dbp = line_list[0] + '_' + line_list[1] + '_' + line_list[2]
#             print(dbp)
#             dict_dbp[dbp] = list()
#             dict_dbp[dbp].append(line_list[3])

print('read raw datalog...')
pat_schmoo = re.compile(r'>>\d+ \d+ WLWLLeakDCMeasure Schnoo\d+ (DUT\d+)  (B\d+) (P\d+) Loop: (\d+)')
pat_leak = re.compile(r'>>\d+ \d+ WLWLLeakDCMeasure DUT(\d+)  B(\d+)  (\d+)\s+([-\d\.]+)')
pat_schmoo_d = re.compile(r'>>\d+ \d+ WLWLLeakDCMeasure Schnoo(\d+) DUT(\d+)  B(\d+) P(\d+) Loop: (\d+)')


with open(raw_datalog, 'r') as FR:
    for line in FR:
        m_leak = pat_leak.search(line)
        m_schmoo_d = pat_schmoo_d.search(line)
        m_schmoo = pat_schmoo.search(line)
        if m_leak:
            dut = int(m_leak.group(1))
            blk = int(m_leak.group(2))
            page = int(m_leak.group(3))
            leak = m_leak.group(4)
            dbp = (dut,blk,page)
            dict_dbp[dbp] = list()
            dict_dbp[dbp].append(leak)
        if m_schmoo_d:
            schmoo = int(m_schmoo_d.group(1))
            dut = int(m_schmoo_d.group(2))
            blk = int(m_schmoo_d.group(3))
            page = int(m_schmoo_d.group(4))
            loop = m_schmoo_d.group(5)
            dbp = (dut,blk,page)
            if dbp in dict_dbp.keys():
                dict_dbp[dbp].append(str(schmoo) + ':' + loop)
            else:
                print('Not find schmoo:', dbp)

print('writing...')
with open(out_name, 'w') as FW:
    FW.write('dut_blk_page\tleak\tloops\n')
    for item in dict_dbp.keys():
        leak = dict_dbp[item][0]
        loops = str(dict_dbp[item][1:])
        FW.write(str(item) + '\t' + leak + '\t' + loops + '\n')



