@echo off
call "C:\Users\%USERNAME%\projects_local\python\py_netscript\venv\Scripts\activate.bat"
start python 1pyshowcmd.py device_empf_iosnxos_p_hw.csv -o C:\Users\%USERNAME%\output\empf_pr
start python 1pyshowcmd.py device_empf_iosnxos_p_conf.csv -o C:\Users\%USERNAME%\output\empf_pr
start python 1pyshowcmd.py device_empf_iosnxos_p_all.csv -o C:\Users\%USERNAME%\output\empf_pr
start python 1pyshowcmd.py device_empf_fortinet_p_hw.csv -o C:\Users\%USERNAME%\output\empf_pr
start python 1pyshowcmd.py device_empf_fortinet_p_conf.csv -o C:\Users\%USERNAME%\output\empf_pr
start python 1pyshowcmd.py device_empf_fortinet_p_all.csv -o C:\Users\%USERNAME%\output\empf_pr
