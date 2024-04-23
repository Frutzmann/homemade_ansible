import paramiko
import logging
import os
import time
from scp import SCPClient
from .base_module import BaseModule
from homemade_ansible import Status


class Copy(BaseModule):
    def __init__(self, src: str, dest: str, back: bool = False):
        params = {'src': src, 'dest': dest, 'back': back}
        super().__init__(params)
        self.src = src
        self.dest = dest
        self.back = back

    def process(self, ssh_client: paramiko.SSHClient, task_counter: int):
        changed = 0
        try:
            with ssh_client.open_sftp() as sftp:
                for root, dirs, files in os.walk(self.src):
                    remote_root = os.path.join(
                        self.dest, os.path.relpath(root, self.src))

                    if len(dirs) > 0:
                        for dir in dirs:
                            remote_dir = os.path.join(remote_root, dir)
                            try:
                                sftp.stat(remote_dir)
                            except IOError:
                                sftp.mkdir(remote_dir)
                                changed += 1

                    if len(files) > 0:
                        for file in files:
                            source = os.path.join(root, file)
                            destination = os.path.join(remote_root, file)
                            try:
                                sftp.stat(destination)
                                if self.back:
                                    sftp.rename(
                                        destination, f'{destination}.bak_{int(time.time())}')
                                    sftp.put(source, destination)
                                    changed += 1
                            except IOError:
                                sftp.put(source, destination)
                                changed += 1

            logging.info(
                f"[{task_counter}] host={ssh_client.get_transport().sock.getpeername()[0]} op=copy src={self.src} dest={self.dest} back={self.back}")
            return Status.CHANGED if changed > 0 else Status.OK

        except Exception as e:
            logging.error(
                f'[{task_counter}] host={ssh_client.get_transport().sock.getpeername()[0]} Error while copying file: {e}')
            return Status.KO
