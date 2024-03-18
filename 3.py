import os
import re
infile = 'C:\\Users\\jackyyick\\output\\empf_np\\20240213_0400\\npne_hw\\n1pnecdmz1101_172.31.210.15_cisco_hw.txt'

with open(infile, 'r') as inF:
    data = inF.read()
    print(data)

    p_foundcontent = re.findall(r'(#####[\s\S]*?)\n([\s\S]*?)(?=\s*#####[\s\S]*?|$)', data)
    print('########################################')
    print(p_foundcontent[13])