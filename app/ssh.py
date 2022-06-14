import io
import paramiko

# app libraries
from web.static.models import Server


def execute_command(server: Server, command: str):
    p = paramiko.SSHClient()
    p.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    if server.auth_method == "password":
        p.connect(server.host, server.port, server.username, server.password)
    else:
        private_key_file = io.StringIO()
        private_key_file.write(server.ssh_key)
        private_key_file.seek(0)
        private_key = paramiko.RSAKey.from_private_key(private_key_file)
        p.connect(server.host, server.port, server.username, pkey = private_key)
    stdin, stdout, stderr = p.exec_command(command)
    opt = stdout.readlines()
    opt = "".join(opt)
    return opt, stderr
