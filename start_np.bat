@echo off
call "C:\Users\OCC\projects_local\python\py-netscript\venv\Scripts\activate.bat"
start python 1pyshowcmd.py device_empf_iosnxos_n_hw.csv -o C:\Users\OCC\output\empf_np
start python 1pyshowcmd.py device_empf_iosnxos_n_conf.csv -o C:\Users\OCC\output\empf_np
start python 1pyshowcmd.py device_empf_iosnxos_n_all.csv -o C:\Users\OCC\output\empf_np
start python 1pyshowcmd.py device_empf_fortinet_n_hw.csv -o C:\Users\OCC\output\empf_np
start python 1pyshowcmd.py device_empf_fortinet_n_conf.csv -o C:\Users\OCC\output\empf_np
start python 1pyshowcmd.py device_empf_fortinet_n_all.csv -o C:\Users\OCC\output\empf_np