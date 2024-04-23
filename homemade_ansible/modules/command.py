import paramiko
import logging
from .base_module import BaseModule
from homemade_ansible import Status


class Command(BaseModule):
    def __init__(self, command: str, shell: str = '/bin/bash'):
        params = {'command': command, 'shell': shell}
        super().__init__(params)
        self.command = command
        self.shell = shell

    def process(self, ssh_client: paramiko.SSHClient, task_counter: int):
        try:
            _, stdout, _ = ssh_client.exec_command(self.command)
            exit_status = stdout.channel.recv_exit_status()

            if exit_status != 0:
                status = Status.CHANGED
            else:
                status = Status.OK

            logging.info(
                f"[{task_counter}] host={ssh_client.get_transport().sock.getpeername()[0]} op=command command={self.command}")
            return status

        except Exception as e:
            logging.error(
                f'[{task_counter}] host={ssh_client.get_transport().sock.getpeername()[0]} Error while executing command {self.command}: {e}')
            return Status.KO
