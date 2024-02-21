#!/usr/bin/env python
# by kkyick2
# import pkg
import argparse
import sys
import os
import csv
import time
from datetime import datetime
from netmiko import SSHDetect, ConnectHandler
from netmiko import NetmikoAuthenticationException
from paramiko.ssh_exception import SSHException
import logging
version = '20240220'
#################################################
# global var
#################################################
DATE = datetime.now().strftime("%Y%m%d")
LOG_FILE_LEVEL = logging.INFO  # set log file level
LOG_CONSOLE_LEVEL = logging.WARNING  # set log console level
LOG_LOWEST_LEVEL = logging.DEBUG  # set lowest log level

SCRIPT_NAME = os.path.splitext(os.path.basename(sys.argv[0]))[0]
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
#################################################
# code for logging
#################################################
# Import Logging
logger = logging.getLogger(SCRIPT_NAME)
# define the lowest-severity log message a logger will handle
logger.setLevel(LOG_LOWEST_LEVEL)
# Create Handlers(Filehandler with filename| StramHandler with stdout)
file_handler = logging.FileHandler(os.path.join(
    SCRIPT_DIR, 'log', 'pyshowcmd_' + DATE + '.log'))
stream_handler = logging.StreamHandler(sys.stdout)
# Set Additional log level in Handlers if needed
file_handler.setLevel(LOG_FILE_LEVEL)
stream_handler.setLevel(LOG_CONSOLE_LEVEL)
# Create Formatter and Associate with Handlers
tz = time.strftime('%z')
formatter = logging.Formatter(
    '%(asctime)s ' + tz + ': %(name)s: %(process)d.%(thread)d: %(funcName)-18s: %(levelname)-8s: %(message)s')
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)
# Add Handlers to logger
logger.addHandler(file_handler)
logger.addHandler(stream_handler)

#################################################
# code for pyshowcmd
#################################################
NEXTLINE = '\n'
PRJ_ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

INVENTORY_COUNT = 0
COMPLETE_COUNT = 0
FAIL_COUNT = 0
FAIL_LIST = []


def add_complete_count():
    global COMPLETE_COUNT
    COMPLETE_COUNT = COMPLETE_COUNT + 1

def add_fail_count(host):
    global FAIL_COUNT
    FAIL_COUNT = FAIL_COUNT + 1
    FAIL_LIST.append(host)


def set_total_count(count):
    global INVENTORY_COUNT
    INVENTORY_COUNT = count


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


def read_cmd_file(fn):
    """
        read filename txt return a cmd list
    """
    with open(fn, 'r') as f:
        return [line.strip() for line in f]


def read_device_file(fn):
    """
        read filename csv return a device list
    """
    print(f'### Script to read csv: {fn}')
    logger.info(f'### Script to read csv: {fn}')

    with open(fn, 'r') as csvf:
        hostnamelist = []
        devicelist = []
        reader = csv.DictReader(csvf)
        for row in reader:
            device = {
                'hostname': row['hostname'],
                'device_type': row['device_type'],
                'ip': row['ip'],
                'port': row['port'],
                'username': row['username'],
                'password': row['password'],
                'cmdfile': row['cmdfile'],
                'otag1': row['otag1'],
                'otag2': row['otag2'],
                'odir1': row['odir1'],
            }
            devicelist.append(device)
            hostnamelist.append(device['hostname'])
    print(f' Number of items in csv: {len(devicelist)}')
    logger.info(f' Number of items in csv: {len(devicelist)}')
    print(f' hostname list: {hostnamelist}')
    logger.info(f' hostname list: {hostnamelist}')
    set_total_count(len(devicelist))

    return devicelist


def print_file(msg, outf):
    """
        print string to outfile and print string to terminal
    """
    outf.write(str(msg) + str(NEXTLINE))
    return


def connect_device(device, outpath):
    """
        connect device using netmiko
        @param device: device dict in this formet, need pop the cmdfile key for using netmiko
         PTHLF1251 = {
            'device_type': 'cisco_nxos',
            'ip': '10.100.171.103',
            'port': '22',
            'username': 'col',
            'password': 'col123col',
            'cmdfile': 'cmd_test_1251.txt', <--need pop this item
        @param outPath: output file full path
        }
    """
    device2 = {
        'device_type': device['device_type'],
        'ip': device['ip'],
        'port': device['port'],
        'username': device['username'],
        'password': device['password'],
    }
    devicetype = device['device_type']
    print(
        f'### Script connect to {device["ip"]}:{device["port"]} execute: {device["cmdfile"]}')
    logger.info(
        f'### Script connect to {device["ip"]}:{device["port"]} execute: {device["cmdfile"]}')

    # read cmd file
    cmdlist = read_cmd_file(device['cmdfile'])
    print(f' Prepare to execute {len(cmdlist)} cmd : {cmdlist}')
    logger.info(f' Prepare to execute {len(cmdlist)} cmd : {cmdlist}')

    # connect to device using netmiko_connect
    try:
        # Case1: auto detect device type
        if (devicetype) == 'autodetect':
            print(f' Device Type: {devicetype}')
            logger.info(f' Device Type: {devicetype}')
            guesser = SSHDetect(**device2)
            best_match = guesser.autodetect()
            print(best_match)  # Name of the best device_type to use further
            # Dictionary of the whole matching result
            print(guesser.potential_matches)

        # Case2: input device type
        else:
            connect = ConnectHandler(**device2)
            prompt = connect.find_prompt()
            print(f' Device Type: {devicetype} | Prompt: {prompt}')
            logger.info(f' Device Type: {devicetype} | Prompt: {prompt}')

            # open output file
            with open(outpath, 'w', encoding='utf-8') as outf:
                # send each cmd to device
                print_file('###### WILL EXECUTE:', outf)
                for cmd in cmdlist:
                    if cmd:
                        print_file(cmd, outf)
                # send each cmd to device
                for cmd in cmdlist:
                    if cmd:
                        output = connect.send_command(cmd)
                        print_file('###### EXECUTE CMD: ' + cmd, outf)
                        print_file(output, outf)

        print(f' Complete and disconnect')
        logger.info(f' Complete and disconnect')
        add_complete_count()

    except (EOFError, SSHException, NetmikoAuthenticationException) as e:
        add_fail_count(device["ip"] + ':' + device["cmdfile"])
        print(f' Exception: {e}')
        logger.warning(e)
        pass
    except Exception as e:
        add_fail_count(device["ip"] + ':' + device["cmdfile"])
        print(f' Exception: {e}')
        logger.warning(e)
        pass
    '''
    ###########################################################################################
    # below part for tshoot login issue
    ###########################################################################################
    connect = ConnectHandler(**device2)
    print("login jor!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1!!!!!!!!!!!!!!!!!!!!")

    prompt = connect.find_prompt()
    print(f' Device Type: {devicetype} | Prompt: {prompt}')
    logger.info(f' Device Type: {devicetype} | Prompt: {prompt}')

    # open output file
    with open(outpath, 'w', encoding='utf-8') as outf:
        # send each cmd to device
        for cmd in cmdlist:
            output = connect.send_command(cmd)
            print_file('###### EXECUTE CMD: ' + cmd, outf)
            print_file(output, outf)

    print(f' Complete and disconnect')
    logger.info(f' Complete and disconnect')
    add_complete_count()
    ###########################################################################################
    '''
    return


def process_input(devicefile, timestamp, outpath):
    """
        1/ open device csv -> device list
        2/ open cmdoutput text -> connect device
    """
    OUT_ROOT_PATH = outpath

    # create device object
    devicelist = read_device_file(devicefile)

    # create layer0: output folder
    mkdir(OUT_ROOT_PATH)

    # loop each row of csv
    for device in devicelist:
        # output filename
        O_FILENAME = device['hostname'] + '_' + \
            device['ip'] + '_' + device['otag1'] + \
            '_' + device['otag2'] + '.txt'

        # create layer1: datetime batch folder
        O_BATCH_PATH = os.path.join(OUT_ROOT_PATH, timestamp)
        mkdir(O_BATCH_PATH)

        # if outdir1 is empty, then no need create layer2 folder
        if not device['odir1']:
            O_FILE_PATH = (os.path.join(O_BATCH_PATH, O_FILENAME))
        # else create layer2 user define name folder
        else:
            O_TYPE_DIR = os.path.join(O_BATCH_PATH, device['odir1'])
            mkdir(O_TYPE_DIR)
            O_FILE_PATH = (os.path.join(O_TYPE_DIR, O_FILENAME))

        # start connect to device
        connect_device(device, O_FILE_PATH)

    return


def main(devicefile, outpath):

    # prepare output batch timestamp
    DATETIME = datetime.now().strftime("%Y%m%d_%H%M")

    print(f'###')
    print(f'###')
    logger.info(f'###')
    logger.info(f'###')
    print(f'############################################################## ')
    print(f'##################       START SCRIPT       ################## ')
    print(f'### Input device inventory: {devicefile}')
    print(f'### Output path: {outpath}')
    logger.info(
        f'############################################################## ')
    logger.info(
        f'##################       START SCRIPT       ################## ')
    logger.info(f'### Input device inventory: {devicefile}')
    logger.info(f'### Output path: {outpath}')

    process_input(devicefile, DATETIME, outpath)

    print(f'### Summary {devicefile}, Complete/Total: {COMPLETE_COUNT} / {INVENTORY_COUNT}')
    print(f'            {devicefile},     Fail/Total: {FAIL_COUNT} / {INVENTORY_COUNT}')
    print(f'            {devicefile},     Fail List : {FAIL_LIST}')

    logger.info(f'### Summary {devicefile}, Complete/Total: {COMPLETE_COUNT} / {INVENTORY_COUNT}')
    logger.info(f'            {devicefile},     Fail/Total: {FAIL_COUNT} / {INVENTORY_COUNT}')
    logger.info(f'            {devicefile},     Fail List : {FAIL_LIST}')

    with open(os.path.join(outpath,DATETIME,'result_log.txt'), 'a', encoding='utf-8') as outf:
        print_file(f'### Summary {devicefile}, Complete/Total: {COMPLETE_COUNT} / {INVENTORY_COUNT}', outf)
        print_file(f'            {devicefile},     Fail/Total: {FAIL_COUNT} / {INVENTORY_COUNT}', outf)
        print_file(f'            {devicefile},     Fail List : {FAIL_LIST}', outf)

    print(f'###############       END SCRIPT       ############### ')
    print(f'###################################################### ')
    logger.info(f'###############       END SCRIPT       ############### ')
    logger.info(f'###################################################### ')


if __name__ == "__main__":

    O_CMD_DIR = 'outputcmd'

    # example1: python 1pyshowcmd.py device_lhk2.csv
    #   output folder default: C:\Users\jackyyick\projects_local\python\py-netscript\outputcmd>

    # example2: python 1pyshowcmd.py device_empf_iosnxos_hw_n.csv -o C:\Users\jackyyick\projects_local\python\<xxx>
    #   output folder : C:\Users\jackyyick\projects_local\python\<xxx>
    parser = argparse.ArgumentParser()
    parser.add_argument("devicefile", help="device_list in csv formet")
    parser.add_argument("-o", "--outpath", help="output path of the show cmd result",
                        default=os.path.join(os.path.dirname(os.path.abspath(__file__)), O_CMD_DIR))
    args = parser.parse_args()
    devicefile = args.devicefile
    outpath = os.path.join(args.outpath)

    main(devicefile, outpath)