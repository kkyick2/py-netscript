import os
import re
infile = 'C:\\Users\\jackyyick\\output\\empf_pr\\20240410_1645\prne_all\\ocpnecwan0101_172.31.210.26_cisco_all.txt'

with open(infile, 'r') as inF:
    data = inF.read()
    ## print(data)

    p_foundcontent = re.findall(r'(##### EXECUTE CMD: [\s\S]*?)\n([\s\S]*?)(?=\s*#####[\s\S]*?|$)', data)
 
    for index,item in enumerate(p_foundcontent):
        print(f'{index} | {p_foundcontent[index][0]}')