import paramiko
import logging
from .base_connection import BaseConnection


class ConnectPrivateSSH(BaseConnection):
    def __init__(self, key_path: str):
        params = {'ssh_key_file': key_path}
        super().__init__(params)
        self.key_path = key_path

    def connect(self, ip, port):
        try:
            client = paramiko.SSHClient()
            policy = paramiko.AutoAddPolicy()
            client.set_missing_host_key_policy(policy)
            client.connect(ip, port, username='user',
                           key_filename=self.key_path, look_for_keys=False)
            return client
        except Exception as e:
            logging.error(f'{ip} Error while connecting: {e}')
