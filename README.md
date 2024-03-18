# python network script

Use python connect to devices and execute commands

## How to use

step1: modify device_list.csv as inventory

```sh
username,password,hostname,ip,port,cmdfile,device_type,otag1,otag2,odir1
fwreadonly,Password,n1psefutm1301,172.31.211.1,22,cmd\cmd_fortigate_status.txt,fortinet,fgate,status,firewall
fwreadonly,Password,n1psefutm1401,172.31.211.2,22,cmd\cmd_fortigate_status.txt,fortinet,fgate,status,firewall
```

method1: Usage: python 1pyshowcmd.py <device_list.csv>

## enable venv in windows

```sh
cd C:\Users\jackyyick\projects_local\python\py-netscript>
# cretae venv
virtualenv venv
# enable venv
venv\Scripts\activate
# run python
python 1pyshowcmd.py device_empf_iosnxos_hw_n.csv -o C:\Users\jackyyick\projects_local\python
```

Export pip requirement

```sh
pip freeze > requirements.txt
```

Install pip requirement in new env

```sh
pip install -r requirements.txt
```

method2: window start.bat for multi start of 1pyshowcmd.py

## Project File structure

```sh
py-netscript
|--- cmd
     |--- xxx.txt # cmd in txt to execute
|--- outputcmd
     |--- 20231229_0111 # Layer1: output datetime batch folder
     |------ sw1_conf.txt
     |------ sw1_status.txt
     |--- 20240103_0222  # Layer1: output datetime batch folder
     |------ firewall    # Layer2: output userdefine folder
     |--------- fw1_conf.txt
|--- output
|--- 1pyshowcmd.py  # python script
|--- device_xxx.csv # modify this csv as inventory
```

## Bcompare Setting

https://www.scootersoftware.com/v4help/sample_scripts.html

https://www.scootersoftware.com/v4help/sessiontextimportance.html

The text items in the Unimportant text

| description    | regex                               |
| :------------- | :---------------------------------- |
| fortigate conf | ^#conf_file_ver=.\*                 |
| fortigate conf | ^#private-encryption-key=.\*        |
| fortigate conf | ._set password\sENC._               |
| fortigate conf | ^\s+set\ssecondary-secret\sENC\s.\* |

## Regex

### Regex for matching config file

https://regex101.com/r/i1BYBO/1

(#####[\s\S]_?)\n([\s\S]_?)(?=\s*#####[\s\S]*?|$)

```sh
Total cdp entries displayed : 3
###### EXECUTE CMD: show lldp neighbors
% LLDP is not enabled
###### EXECUTE CMD: show environment power
SW  PID                 Serial#     Status           Sys Pwr  PoE Pwr  Watts
--  ------------------  ----------  ---------------  -------  -------  -----
1A  PWR-C1-350WAC-P     DCC2522B1V0  OK              Good     n/a      350
1B  PWR-C1-350WAC-P     DCC2522B1UZ  OK              Good     n/a      350

###### EXECUTE CMD: show environment fan
Switch   FAN     Speed   State   Airflow direction
---------------------------------------------------
  1       1     14240     OK     Front to Back
  1       2     14240     OK     Front to Back
  1       3     14240     OK     Front to Back
FAN PS-1 is OK
FAN PS-2 is OK

###### EXECUTE CMD: show clock
04:01:07.912 HKT Tue Feb 13 2024
```

## Reference

netmiko https://github.com/ktbyers/netmiko

netmiko device_type #150 https://github.com/ktbyers/netmiko/blob/develop/netmiko/ssh_dispatcher.py

netmiko doc https://ktbyers.github.io/netmiko/docs/netmiko/index.html#netmiko.BaseConnection

paramiko https://github.com/paramiko/paramiko

paramiko client https://github.com/paramiko/paramiko/blob/main/paramiko/client.py

## History

| Version  | Date      | Description             |
| :------- | :-------- | :---------------------- |
| 20230713 | 2023-0713 | draft                   |
| 20240112 | 2024-0112 | update for batch backup |
| 20240207 | 2024-0207 | input using argparse    |

## To Do

```bash
login as: fwreadonly
Keyboard-interactive authentication prompts from server:
|
| This information system is the private property of eMPF Platform Company Limi
> ted. It is for authorized use only.
| Unauthorized or improper use of this system may result in civil and criminal
> penalties and administrative and disciplinary action as appropriate.
|
| Users have no explicit or implicit expectation of privacy.
| Any or all uses of this information system including files on this system may
>  be intercepted, monitored, recorded , copied , audited , inspected, and disc
> losed for eMPF Platform Company Limited authorized purposes.
|
| By using this system, the user consents to above conditions and terms listed
> in Acceptable Use Policy (AUP) of eMPF Private Cloud.
| LOG OFF IMMEDIATELY if you do not agree to any or all terms and conditions as
>  stated in this banner or AUP.
| Accept (y/N)?

```
