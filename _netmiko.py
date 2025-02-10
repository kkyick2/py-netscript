from netmiko import ConnectHandler

cisco1 = { 
    "device_type": "cisco_nxos",
    "host": "172.31.210.71",
    "username": "swreadonly",
    "password": "d8Nz7KW756sbmEXv!",
}

# Show command that we execute.
command = "show interface"

connect = ConnectHandler(**cisco1)
prompt = connect.find_prompt()
output = connect.send_command(command)

# Automatically cleans-up the output so that only the show output is returned
print()
print(prompt)
print(output)
print()