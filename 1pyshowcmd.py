#!/usr/bin/env python
# by kkyick2
# import pkg
import os
import sys
import csv
import time
from datetime import datetime
from netmiko import SSHDetect, ConnectHandler
from paramiko.ssh_exception import SSHException

#################################################
# code for logging
#################################################
import logging
scriptname = os.path.splitext(os.path.basename(sys.argv[0]))[0]
logger = logging.getLogger(scriptname)
logger.setLevel(logging.DEBUG)

DATE = datetime.now().strftime("%Y%m%d")
script_dir = os.path.dirname(os.path.realpath(__file__))

# Create Handlers(Filehandler with filename| StramHandler with stdout)
file_handler_info = logging.FileHandler(
    os.path.join(script_dir, 'pyshowcmd_info_'+DATE+'.log'))
file_handler_debug = logging.FileHandler(
    os.path.join(script_dir, 'pyshowcmd_debug_'+DATE+'.log'))
stream_handler = logging.StreamHandler(sys.stdout)

# Set Additional log level in Handlers if needed
file_handler_info.setLevel(logging.INFO)
file_handler_debug.setLevel(logging.DEBUG)
# Warning or above will log to console
stream_handler.setLevel(logging.WARNING)

# Create Formatter and Associate with Handlers
tz = time.strftime('%z')

formatter = logging.Formatter(
    '%(asctime)s ' + tz + ' - %(name)s - %(levelname)s - %(message)s')
file_handler_info.setFormatter(formatter)
file_handler_debug.setFormatter(formatter)
stream_handler.setFormatter(formatter)

# Add Handlers to logger
logger.addHandler(file_handler_info)
logger.addHandler(file_handler_debug)
logger.addHandler(stream_handler)

#################################################
# code for pyshowcmd
#################################################
NEXTLINE = '\n'
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
O_CMD_DIR = 'cmdoutput'
O_XLS_DIR = 'output'


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
    print(f'###### Read csv: {fn}')
    logger.info(f'###### Read csv: {fn}')

    with open(fn, 'r') as csvf:
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
            }
            devicelist.append(device)
    print(f' Number of host in csv: {len(devicelist)}')
    logger.info(f' Number of host in csv: {len(devicelist)}')
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
        f'###### Connect to {device["ip"]}:{device["port"]} execute: {device["cmdfile"]}')
    logger.info(
        f'###### Connect to {device["ip"]}:{device["port"]} execute: {device["cmdfile"]}')

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
    except (EOFError, SSHException) as e:
        print(e)
        logger.warning(e)
    except Exception as e:
        print(e)
        logger.warning(e)

    return


def main(devicefile):
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
        O_TYPE_DIR = os.path.join(O_BATCH_DIR, device['device_type'])
        mkdir(O_TYPE_DIR)

        # output filename
        O_FILENAME = device['hostname'] + '_' + \
            device['ip'] + '_' + DATETIME + '.txt'
        O_FILEPATH = (os.path.join(O_TYPE_DIR, O_FILENAME))

        # start connect to device
        connect_device(device, O_FILEPATH)

    return


if __name__ == "__main__":

    # loggin test #
    logger.debug("This is Debug message")
    logger.info("This is Info message")
    logger.warning("This is Warning message")
    logger.error("This is Error message")
    logger.critical("This is Critical message")

    print(f'###')
    logger.info(f'###')
    print(f'###')
    logger.info(f'###')
    print(f"{'#'*15} INITIALIZING THE SCRIPT {'#'*15}")
    logger.info(f"{'#'*15} INITIALIZING THE SCRIPT {'#'*15}")
    devicefile = 'device_lhk2.csv'
    main(devicefile)

    print(f'############    END SCRIPT    ############ ')
    logger.info(f'############    END SCRIPT    ############ ')
