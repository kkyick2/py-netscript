#!/usr/bin/env python
# by kkyick2
# import pkg
import os
import csv
from datetime import datetime
from netmiko import ConnectHandler
from paramiko.ssh_exception import SSHException

NEXTLINE = '\n'
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_CMD_DIR = 'cmdoutput'
OUT_XLS_DIR = 'output'


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


def read_cmd_file(filename):
    """
        read txt return a list
    """
    with open(filename, 'r') as f:
        return [line.strip() for line in f]


def read_device_file(filename):
    """
        read csv return a list
    """
    with open(filename, 'r') as csvFile:
        devicelist = []
        reader = csv.DictReader(csvFile)
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
    return devicelist


def print_file(msg, outFile):
    """
        print string to outfile and print string to terminal
    """
    # print(msg)
    outFile.write(str(msg) + str(NEXTLINE))


def connect_device(device, outFile):
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
        }
    """
    device2 = {
        'device_type': device['device_type'],
        'ip': device['ip'],
        'port': device['port'],
        'username': device['username'],
        'password': device['password'],
    }
    # connect to device using netmiko_connect
    try:
        connect = ConnectHandler(**device2)
        prompt = connect.find_prompt()
        print('#########################', outFile)
        print('### Connect: {}:{}|{}|{}'.format(device['ip'], device['port'], prompt, device['cmdfile']), outFile)
        # print_file('Connect: {}:{}|{}|{}'.format(device['ip'], device['port'], prompt, device['cmdfile']), outFile)
        # prepare command list for sending to device
        cmdlist = read_cmd_file(device['cmdfile'])
        for cmd in cmdlist:
            output = connect.send_command(cmd)
            print_file(cmd, outFile)
            print_file(output, outFile)
        print('### Exit   : {}, exit'.format(device['ip']), outFile)
        print('#########################', outFile)
    except (EOFError, SSHException) as e:
        print(e)
    except Exception as e:
        print(e)


def main(devicefile):
    """
        1/ open device csv -> device list
        2/ open cmdoutput text -> connect device
    """
    devicelist = read_device_file(devicefile)
    DATETIME = datetime.now().strftime("%Y%m%d_%H%M")
    # start connect to device
    for device in devicelist:
        OUT_TYPE_DIR = os.path.join(ROOT_DIR, OUT_CMD_DIR, device['device_type'])
        mkdir(OUT_TYPE_DIR)
        OUT_FILENAME = device['hostname'] + '_' + device['ip'] + '_' + DATETIME + '.txt'
        OUT_FILEPATH = (os.path.join(OUT_TYPE_DIR, OUT_FILENAME))
        with open(OUT_FILEPATH, 'w') as outFile:
            connect_device(device, outFile)


if __name__ == "__main__":
    devicefile = 'device_empf_x.csv'
    main(devicefile)