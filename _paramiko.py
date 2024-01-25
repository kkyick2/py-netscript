import paramiko

# SSH connection parameters
hostname = "172.31.211.5"
username = "fwreadonly"
password = "P@sshktw0rd202206"

# Create SSH client
client = paramiko.SSHClient()
client.load_system_host_keys()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Connect to the device
client.connect(hostname, username=username, password=password)

# Handling keyboard-interactive authentication prompts
transport = client.get_transport()
session = transport.open_session()
session.invoke_subsystem('ssh')
transport.auth_interactive(username)

# Execute command
command = "get system status"
stdin, stdout, stderr = client.exec_command(command)

# Print command output
output = stdout.read().decode()
print(output)

# Close the SSH connection
client.close()
