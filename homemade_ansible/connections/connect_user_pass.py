import paramiko
import logging
from .base_connection import BaseConnection


class ConnectUserPass(BaseConnection):
    def __init__(self, username: str, password: str):
        params = {'ssh_user': username, 'ssh_password': password}
        super().__init__(params)
        self.username = username
        self.password = password

    def connect(self, ip, port):
        try:
            client = paramiko.SSHClient()
            policy = paramiko.AutoAddPolicy()
            client.set_missing_host_key_policy(policy)
            client.connect(ip, port, username=self.username,
                           password=self.password)
            return client
        except Exception as e:
            logging.error(f'{ip} Error while connecting: {e}')
