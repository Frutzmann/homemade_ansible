import paramiko
import logging
from .base_module import BaseModule
import jinja2
from homemade_ansible import Status


class Template(BaseModule):
    def __init__(self, src: str, dest: str, vars: dict):
        params = {'src': src, 'dest': dest, 'vars': vars}
        super().__init__(params)
        self.src = src
        self.dest = dest
        self.vars = vars

    def process(self, ssh_client: paramiko.SSHClient, task_counter: int):
        try:
            with open(self.src, 'r') as file:
                template = jinja2.Template(file.read())
            rendered_template = template.render(**self.vars)

            _, stdout, _ = ssh_client.exec_command(f'cat {self.dest}')
            current_content = stdout.read().decode()

            if current_content.split() == rendered_template.split():
                status = Status.OK
            else:
                _, stdout, _ = ssh_client.exec_command(
                    f'echo "{rendered_template}" | sudo tee {self.dest} > /dev/null')
                stdout.channel.recv_exit_status()
                status = Status.CHANGED

            logging.info(
                f"[{task_counter}] host={ssh_client.get_transport().sock.getpeername()[0]} op=template src={self.src} dest={self.dest} vars={self.vars}")
            return status

        except Exception as e:
            logging.error(
                f'[{task_counter}] host={ssh_client.get_transport().sock.getpeername()[0]} Error while rendering template: {e}')
            return Status.KO
