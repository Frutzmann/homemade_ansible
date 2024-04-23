import paramiko
import logging
from .base_module import BaseModule
from homemade_ansible import Status, Choice


class Service(BaseModule):

    def __init__(self, name: str, state: Choice):
        params = {'name': name, 'state': state}
        super().__init__(params)
        self.name = name
        self.state = state

    def process(self, client: paramiko.SSHClient, task_counter: int):
        previous_status = self.__execute_service(client, self.name, 'status')
        current_status = None
        try:
            if self.state == Choice.STARTED.value:
                current_status = self.__execute_service(
                    client, self.name, 'start')
            elif self.state == Choice.STOPPED.value:
                current_status = self.__execute_service(
                    client, self.name, 'stop')
            elif self.state == Choice.RESTARTED.value:
                current_status = self.__execute_service(
                    client, self.name, 'restart')
            elif self.state == Choice.ENABLED.value:
                current_status = self.__execute_service(
                    client, self.name, 'enable')
            elif self.state == Choice.DISABLED.value:
                current_status = self.__execute_service(
                    client, self.name, 'disable')

            logging.info(
                f"[{task_counter}] host={client.get_transport().sock.getpeername()[0]} op=service name={self.name} state={self.state}")
            if previous_status == current_status:
                return Status.OK

            return Status.CHANGED

        except Exception as e:
            logging.error(
                f'[{task_counter}] host={client.get_transport().sock.getpeername()[0]} Error while trying to modify {self.name} status: {e}')
            return Status.KO

    def __execute_service(self, client: paramiko.SSHClient, name: str, action: str):
        _, stdout, _ = client.exec_command(f'sudo systemctl {action} {name}')
        return stdout.channel.recv_exit_status()
