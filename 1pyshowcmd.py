#!/usr/bin/env python
# by kkyick2
# import pkg
import sys
import os
import csv
import time
from datetime import datetime
from netmiko import SSHDetect, ConnectHandler
from netmiko import NetmikoAuthenticationException
from paramiko.ssh_exception import SSHException
import logging
version = '20241001'
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
    SCRIPT_DIR, 'pyshowcmd_' + DATE + '.log'))
stream_handler = logging.StreamHandler(sys.stdout)
# Set Additional log level in Handlers if needed
file_handler.setLevel(LOG_FILE_LEVEL)
stream_handler.setLevel(LOG_CONSOLE_LEVEL)
# Create Formatter and Associate with Handlers
tz = time.strftime('%z')
formatter = logging.Formatter(
    '%(asctime)s ' + tz + ' - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)
# Add Handlers to logger
logger.addHandler(file_handler)
logger.addHandler(stream_handler)

#################################################
# code for pyshowcmd
#################################################
NEXTLINE = '\n'
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
O_CMD_DIR = 'outputcmd'
O_XLS_DIR = 'output'

INVENTORY_COUNT = 0
COMPLETE_COUNT = 0


def add_complete_count():
    global COMPLETE_COUNT
    COMPLETE_COUNT = COMPLETE_COUNT + 1


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
        devicelist = []
        reader = csv.DictReader(csvf)
        for row in reader:
            print(row)
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
            }
            devicelist.append(device)
    print(f' Number of items in csv: {len(devicelist)}')
    logger.info(f' Number of itens in csv: {len(devicelist)}')
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
                for cmd in cmdlist:
                    output = connect.send_command(cmd)
                    print_file('###### EXECUTE CMD: ' + cmd, outf)
                    print_file(output, outf)

        print(f' Complete and disconnect')
        logger.info(f' Complete and disconnect')
        add_complete_count()

    except (EOFError, SSHException, NetmikoAuthenticationException) as e:
        print(f' Exception: {e}')
        logger.warning(e)
        pass
    except Exception as e:
        print(f' Exception: {e}')
        logger.warning(e)
        pass

    return


def process_input(devicefile):
    """
        1/ open device csv -> device list
        2/ open cmdoutput text -> connect device
    """
    # create device object
    devicelist = read_device_file(devicefile)

    # loop each row of csv
    DATETIME = datetime.now().strftime("%Y%m%d_%H%M")
    for device in devicelist:
        # create batch folder
        O_BATCH_DIR = os.path.join(ROOT_DIR, O_CMD_DIR, DATETIME)
        mkdir(O_BATCH_DIR)

        # create device type folder
        # O_TYPE_DIR = os.path.join(O_BATCH_DIR, device['device_type'])
        # mkdir(O_TYPE_DIR)

        # output filename
        O_FILENAME = device['hostname'] + '_' + \
            device['ip'] + '_' + device['otag1'] + \
            '_' + device['otag2'] + '.txt'
        O_FILEPATH = (os.path.join(O_BATCH_DIR, O_FILENAME))

        # start connect to device
        connect_device(device, O_FILEPATH)

    return


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Fail to execute, Usage: python 1pyshowcmd.py <device_list.csv>")
        logger.info(
            f'Fail to execute, Usage: python 1pyshowcmd.py <device_list.csv>')
        sys.exit(1)
    devicefile = sys.argv[1]
    # devicefile = 'device_lhk2.csv'

    print(f'###')
    print(f'###')
    logger.info(f'###')
    logger.info(f'###')
    print(f'############################################################## ')
    print(f'##################       START SCRIPT       ################## ')
    print(f'### Input device inventory: {devicefile}')
    logger.info(
        f'############################################################## ')
    logger.info(
        f'##################       START SCRIPT       ################## ')
    logger.info(f'### Input device inventory: {devicefile}')

    process_input(devicefile)

    print(
        f' ### Summary: Complete/Total: {COMPLETE_COUNT} / {INVENTORY_COUNT} in file {devicefile}')
    logger.info(
        f' ### Summary: Complete/Total: {COMPLETE_COUNT} / {INVENTORY_COUNT} in file {devicefile}')

    print(f'###############       END SCRIPT       ############### ')
    print(f'###################################################### ')
    logger.info(f'###############       END SCRIPT       ############### ')
    logger.info(f'###################################################### ')
