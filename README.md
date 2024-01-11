# python network script

Use python connect to devices and execute commands

## How to use

step1: modify device_list.csv as inventory

```sh
username,password,hostname,ip,port,cmdfile,device_type,otag1,otag2
fwreadonly,Password,n1psefutm1301,172.31.211.1,22,cmd\cmd_fortigate_status.txt,fortinet,fgate,status
fwreadonly,Password,n1psefutm1401,172.31.211.2,22,cmd\cmd_fortigate_status.txt,fortinet,fgate,status
```

method1: Usage: python 1pyshowcmd.py <device_list.csv>

```sh
cd C:\Users\jackyyick\projects_local\python\py-netscript>
venv\Scripts\activate
python 1pyshowcmd.py evice_list.csv>
```

method2: window start.bat for multi start of 1pyshowcmd.py

## Project File structure

```sh
py-netscript
|--- cmd
     |--- xxx.txt # cmd in txt to execute
|--- outputcmd
     |--- 20240101_0111 # output cmd batch folder
|--- output
     |--- DNS Security Report-2023-02-14-1704_1915.zip
     |--- IPS Report-2023-02-14-1704_1915.zip
     |--- Web Usage Summary Report-2023-02-14-1704_1915.zip
|--- 1pyshowcmd.py
|--- device_xxx.csv # modify this csv as inventory
```

## Reference

netmiko https://github.com/ktbyers/netmiko

## History

| Version  | Date      | Description             |
| :------- | :-------- | :---------------------- |
| 20230713 | 2023-0713 | draft                   |
| 20240112 | 2024-0112 | update for batch backup |
