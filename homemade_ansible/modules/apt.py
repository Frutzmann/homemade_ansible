import paramiko
import logging
from .base_module import BaseModule
from homemade_ansible import Choice, Status


class APT(BaseModule):
    def __init__(self, name: str, state: Choice):
        params = {'name': name, 'state': state}
        super().__init__(params)
        self.name = name
        self.state = state

    def process(self, ssh_client: paramiko.SSHClient, task_counter: int):
        status = None
        _, stdout, _ = ssh_client.exec_command(
            f'sudo apt list --installed | grep {self.name}')
        is_installed = 'installed' in stdout.read().decode()
        try:
            if self.state == Choice.PRESENT:
                if is_installed:
                    status = Status.OK
                else:
                    self.__apt_run_command(f'sudo apt update -y', ssh_client)
                    status = self.__apt_run_command(
                        f'sudo apt install -y {self.name}', ssh_client)
            elif self.state == Choice.ABSENT:
                if not is_installed:
                    status = Status.OK
                else:
                    status = self.__apt_run_command(
                        f'sudo apt remove -y {self.name}', ssh_client)

            logging.info(
                f"[{task_counter}] host={ssh_client.get_transport().sock.getpeername()[0]} op=apt name={self.name} state={self.state.name}")
            return status

        except Exception as e:
            logging.error(
                f'[{task_counter}] host={ssh_client.get_transport().sock.getpeername()[0]} Error while installing or removing package {self.name}: {e}')
            return Status.KO

    def __apt_run_command(self, command: str, ssh_client: paramiko.SSHClient):
        _, stdout, _ = ssh_client.exec_command(command)
        exit_status = stdout.channel.recv_exit_status()

        if exit_status != 0:
            raise Exception
        else:
            return Status.CHANGED
