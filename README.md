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
venv\Scripts\activate
python 1pyshowcmd.py device_empf_iosnxos_hw_n.csv -o C:\Users\jackyyick\projects_local\python
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

## pip requirement

Export pip requirement

```sh
pip freeze > requirements.txt
```

Install pip requirement in new env

```sh
pip install -r requirements.txt
```

## Bcompare Setting

https://www.scootersoftware.com/v4help/sample_scripts.html

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
