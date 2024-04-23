import paramiko
import logging
from .base_module import BaseModule
from homemade_ansible import Status


class Sysctl(BaseModule):
    def __init__(self, attribute: str, value: any, permanent: bool = False):
        params = {'attribute': attribute, 'value': value}
        super().__init__(params)
        self.attribute = attribute
        self.value = value
        self.permanent = permanent

    def process(self, ssh_client: paramiko.SSHClient, task_counter: int):
        try:
            current_value = self.__get_current_value(
                ssh_client, self.attribute)
            if current_value == self.value:
                status = Status.OK
            else:
                _, stdout, stderr = ssh_client.exec_command(
                    f'sudo sysctl {self.attribute}={self.value}')

                if self.permanent:
                    _, stdout, stderr = ssh_client.exec_command(
                        f'echo {self.attribute}={self.value} >> /etc/sysctl.conf')
                exit_status = stdout.channel.recv_exit_status()
                if exit_status != 0:
                    raise Exception(stderr.read().decode('utf-8'))

                status = Status.CHANGED

            logging.info(
                f"[{task_counter}] host={ssh_client.get_transport().sock.getpeername()[0]} op=sysctl attribute={self.attribute} value={self.value} permanent={self.permanent}")
            return status

        except Exception as e:
            logging.error(
                f'[{task_counter}] host={ssh_client.get_transport().sock.getpeername()[0]} Error while updating sysctl attribute {self.attribute}: {e}')
            return Status.KO

    def __get_current_value(self, ssh_client: paramiko.SSHClient, attribute: str):
        _, stdout, _ = ssh_client.exec_command(f'sudo sysctl -n {attribute}')
        value = stdout.read().decode().strip()
        return int(value)
