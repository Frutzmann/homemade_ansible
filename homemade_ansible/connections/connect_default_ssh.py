import paramiko
import logging
from getpass import getuser
from .base_connection import BaseConnection


class ConnectDefaultSSH(BaseConnection):
    def __init__(self):
        super().__init__(None)

    def connect(self, ip, port):
        try:
            current_user = getuser()
            client = paramiko.SSHClient()
            # Utilisé uniquement pour des fins de testing, une solution plus secure
            # serait de vérifier les 'known hosts'
            policy = paramiko.AutoAddPolicy()
            client.set_missing_host_key_policy(policy)
            client.connect(ip, port, username=current_user)
            return client
        except Exception as e:
            logging.error(f'{ip} Error while connecting: {e}')
