import glob, os, re, argparse
import pandas as pd
from ciscoconfparse import CiscoConfParse
version = '20240318'

def mkdir(path):
    """
        Create a directory
        @param path : full path folder to be create
        @rtype: na
    """
    # create output batch folder
    try:
        os.makedirs(path)
    except OSError as e:
        if not os.path.isdir(path):
            raise
    return


def parseCiscoIOS_Interface(parse, hostname):
    '''
        @parse: ciscoconfparse Object
        @rtl: return a list of Interface dict
            [{'hostname': 'ES-B15W-1', 'interface': 'interface Loopback0', 'shutdown': '-', 'description': '-'}, 
             {'hostname': 'ES-B15W-1', 'interface': 'interface Loopback0', 'shutdown': '-', 'description': '-'}, ...]
    '''
    # all_intfs: list of intf objects example:
    # [ <IOSCfgLine # 258 'interface GigabitEthernet1/1'>, 
    #   <IOSCfgLine # 261 'interface GigabitEthernet1/2'>, ...] 
    rtl = []
    all_intfs = parse.find_objects(r"^interface ")
    for intf_obj in all_intfs: 

        l_nosw_noip = []
        l_trunk_vlan_list = []
        l_stp = []
        l_iphelper = []
        l_standby = []
        l_ippim = []
        l_ipigmp = []
        l_noipxxx = []
        l_ippolicy = []
        l_servicepolicy = []
        l_oth_cmd = []
        row = {
            'hostname' : '-',
            'interface' : '-',
            'shutdown' : '-',
            'description' : '-',
            'nosw_noip': '-',
            'port_mode' : '-',
            'trunk vlan': '-',
            'access vlan': '-',
            'channel-group': '-',
            'spanning-tree': '-',
            'ipaddr': '-',
            'vrf': '-',
            'helper-address' : '-',
            'access-group': '-',
            'standby': '-',
            'ippim': '-',
            'ipigmp': '-',
            'ippolicy': '-',
            'servicepolicy': '-',
            'no ip xxx': '-',
            'other': '-',
        }
        # hostname
        row['hostname'] = hostname

        # interface
        intf2 = re.split('interface ', intf_obj.text)[1]
        row['interface'] = intf2
        #print("--interface: {}".format(intf2))
        #################################################
        # print("----intf_child: {}".format(intf_obj.children))
        for intf_child in intf_obj.children:
            line = intf_child.text.lstrip().rstrip().strip()
            '''
                description Blg15W-G/F-IP-Phone
            '''
            # shutdown
            if line.startswith('shutdown'):
                row['shutdown'] = line

            # description
            elif line.startswith('description'):
                line2 = re.split('description ', line)
                row['description'] = line2[1]

            #################################################
            # [switchport/no switchport/no ip address]
            elif re.compile('no switchport$|switchport$|no ip address$').match(line):
                l_nosw_noip.append(line)
                
            # switchport mode [access\trunk]
            elif line.startswith('switchport mode'):
                line2 = re.split('switchport mode ',line)
                row['port_mode'] = line2[1]

            # channel-group
            elif line.startswith('channel-group'):
                row['channel-group'] = line

            # switchport access vlan
            elif line.startswith('switchport access vlan'):
                line2 = re.split('switchport access vlan ',line)
                row['access vlan'] = line2[1]

            # switchport trunk allowed vlan
            elif line.startswith('switchport trunk allowed vlan'):
                line2 = re.split('switchport trunk allowed vlan ', line)
                #row['trunk vlan'] = line2[1]
                #print(line2[1]
                l_trunk_vlan_list.append(line2[1])

            # spanning-tree xxx
            # multiple match, put in list
            elif line.startswith('spanning-tree'):
                line2 = re.findall(r'spanning-tree\s+(.+)', line)
                l_stp.append(line2[0])

            #################################################
            # ip address
            elif line.startswith('ip address'):
                line2 = re.split('ip address ', line)
                row['ipaddr'] = line2[1]

            # vrf
            elif line.startswith('vrf forwarding') | line.startswith('ip vrf forwarding') | line.startswith('vrf member') :
                line2 = re.split('vrf forwarding ', line)
                row['vrf'] = line2[1]

            # ip helper-address
            # multiple match, put in list
            elif line.startswith('ip helper-address'):
                line2 = re.findall(r'ip\s+helper-address\s+(\S+)$', line)
                l_iphelper.append(line2[0])
                
            # ip access-group
            elif line.startswith('ip access-group'):
                line2 = re.split('ip access-group ', line)
                row['access-group'] = line2[1]

            # standby 1 ip 10.95.138.1, standby 1 prioity 50, ...etc
            # multiple match, put in list
            elif line.startswith('standby'):
                line2 = re.findall(r'standby\s+(.+)', line)
                l_standby.append(line2[0])

            # ip pim
            # multiple match, put in list
            elif line.startswith('ip pim'):
                line2 = re.findall(r'ip pim\s+(.+)', line)
                l_ippim.append(line2[0])

            # ip igmp
            # multiple match, put in list
            elif line.startswith('ip igmp'):
                line2 = re.findall(r'ip igmp\s+(.+)', line)
                l_ipigmp.append(line2[0])

            # ip policy
            # multiple match, put in list
            elif line.startswith('ip policy'):
                line2 = re.findall(r'ip policy\s+(.+)', line)
                l_ippolicy.append(line2[0])

            # service policy
            # multiple match, put in list
            elif line.startswith('service-policy'):
                line2 = re.findall(r'service-policy\s+(.+)', line)
                l_servicepolicy.append(line2[0])

            # [no ip redirects/no ip unreachables/no ip proxy-arp]
            # multiple match, put in list
            elif re.compile('no ip redirects$|no ip unreachables$|no ip proxy-arp$').match(line):
                l_noipxxx.append(line)

            #################################################
            # other child in intf
            else:
                l_oth_cmd.append(line)

        # Append row to list d
        if l_nosw_noip:
            row['nosw_noip'] = l_nosw_noip
        if l_trunk_vlan_list:
            row['trunk vlan'] = l_trunk_vlan_list
        if l_stp:
            row['spanning-tree'] = l_stp
        if l_iphelper:
            row['helper-address'] = l_iphelper
        if l_standby:
            row['standby'] = l_standby
        if l_ippim:
            row['ippim'] = l_ippim
        if l_ipigmp:
            row['ipigmp'] = l_ipigmp
        if l_ippolicy:
            row['ippolicy'] = l_ippolicy
        if l_servicepolicy:
            row['servicepolicy'] = l_servicepolicy
        if l_noipxxx:
            row['no ip xxx'] = l_noipxxx
        if l_oth_cmd:
            row['other'] = l_oth_cmd
        rtl.append(row)

    return rtl


def output_dataframe(df, outf):
    '''
        @df : pandas dataframe
        @outf: a list include [filename,sheetname]
    '''
    print("### Step2: Export dataframe:")
    # print(" Prepare export to file: ")
    # option1: Excel
    # df.to_excel(outf[0], sheet_name=outf[1], index=False)
    # option2: CSV
    df.to_csv(outf[0], index=False)

    print(" Export dataframe to file: {}".format(outf[0]))
    return


def parse_configfile_to_dict(inf):
    '''
        @inf : input config txt file
        @rt: return a list of dict
            [{'hostname': 'ES-B15W-1', 'interface': 'interface Loopback0', 'shutdown': '-', 'description': '-'}, 
             {'hostname': 'ES-B15W-1', 'interface': 'interface Loopback0', 'shutdown': '-', 'description': '-'}, ...]
    '''
    print(f'### Step1: Start Parsing input file: {inf}')
    parse = CiscoConfParse(inf)
    #################################################
    # Hostname line
    line = parse.find_objects(r'^hostname\b|^\s+sysname')[0].text
    type = 'tbc'

    # Cisco: hostname<space>SW1
    if line.startswith('hostname'):
        hostname = re.findall(r'^hostname\s+(\S+)', line)[0]
        type = 'ios'

    # H3C: <space>sysname<space>SW1
    elif line.startswith(' sysname'):
        hostname = re.findall(r'^\s+sysname\s+(\S+)', line)[0]
        type = 'h3c'

    print(f'Prepare to parse: hostname: {hostname} | type: {type}')
    #################################################
    # parseCiscoIOS_Interface
    rt_int = []
    if type == 'ios':
        rt_int = parseCiscoIOS_Interface(parse, hostname)
    elif type == 'h3c':
        rt_int = parseCiscoIOS_Interface(parse, hostname)

    return rt_int


def parse_a_configfile(in_root_path, out_root_path):

    infilename = os.path.basename(in_root_path)
    outf = os.path.join(out_root_path, infilename + '_out.csv')

    #################################################
    # Step1
    dict = parse_configfile_to_dict(in_root_path)
    #################################################
    # Step2
    df1 = pd.DataFrame(dict)
    output_dataframe(df1, [outf, 'sheet1'])

    return df1


def merage_dataframe(outpath):
    extension = "*.csv"
    output = os.path.join(outpath, 'meraged.csv')
    interesting_files = glob.glob(os.path.join(outpath, extension)) 
    df = pd.concat((pd.read_csv(f, header = 0) for f in interesting_files), ignore_index=True)
    df.to_csv(output)


def main(inpath, outpath, merage):

    extension = "*.txt"

    print(f'###')
    print(f'###')
    print(f'############################################################## ')
    print(f'##################       START SCRIPT       ################## ')

    # input path
    infile_list = glob.glob(os.path.join(inpath, extension))
    print(f'### There are: {len(infile_list)} file in input path')
    print(f' Input file list: {infile_list}')
    # output path
    print(f' Output path: {outpath}')
    mkdir(outpath)
    # merage option
    print(f' merage option: {merage}')

    for in_cfg in infile_list:
        df = parse_a_configfile(in_cfg, outpath)

    if merage == 'yes':
        merage_dataframe(outpath)


if __name__ == "__main__":

    #usage: python 2pyconfparse.py <inputpath> -o <output path> -m <merage?yesORno>

    #example: python 2pyconfparse.py C:/Users/jackyyick/output/empf_np/20240227_0400/npne_conf -m yes

    O_PARSE_DIR = 'outputconfparse'

    parser = argparse.ArgumentParser()
    parser.add_argument("inpath", help="dir that contain configuration files in txt")
    parser.add_argument("-o", "--outpath", help="output path of the csv result",
                        default=os.path.join(os.path.dirname(os.path.abspath(__file__)), O_PARSE_DIR))
    parser.add_argument("-m", "--merage", help="merage the result csv: yes OR no",
                        default='no')
    args = parser.parse_args()
    inpath = args.inpath
    outpath = args.outpath
    merage = args.merage

    main(inpath, outpath, merage)