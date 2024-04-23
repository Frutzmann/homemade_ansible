import click
import yaml

import logging
from collections import Counter

from .logger import Logger
from .connections import ConnectDefaultSSH, ConnectPrivateSSH, ConnectUserPass
from .connections.base_connection import BaseConnection
from .modules import Copy, APT, Command, Service, Sysctl, Template
from .modules.base_module import BaseModule
from homemade_ansible import Status, Choice


@click.command()
@click.option('-f', '--playbook-file', 'playbook', type=click.Path(exists=True, readable=True), required=True, help='The playbook file/todo list file\'s path (in YAML).')
@click.option('-i', '--inventory-file', 'inventory', type=click.Path(exists=True, readable=True), required=True, help='The inventory file\'s path (in YAML).')
@click.option('--debug', is_flag=True, help="Enable debug mode, displays the stack trace")
def main(playbook, inventory, debug):

    connections = []
    hosts = {}

    with open(inventory) as i:
        inv = yaml.safe_load(i)
        for key, value in inv['hosts'].items():
            address = value['ssh_address']
            port = value['ssh_port']
            if 'ssh_user' in value and 'ssh_password' in value:
                user = value['ssh_user']
                password = value['ssh_password']
                connection = ConnectUserPass(user, password)
            elif 'ssh_key_file' in value:
                key_file = value['ssh_key_file']
                connection = ConnectPrivateSSH(key_file)
            else:
                connection = ConnectDefaultSSH()
            hosts[address] = []
            connections.append(connection.connect(address, port))

    Logger(is_debug=debug)

    with open(playbook) as f:
        play = yaml.safe_load(f)
        logging.info(
            f"processing {len(play)} tasks on hosts: {', '.join(hosts.keys())}")
        task_counter = 1
        for tasks in play:
            module = tasks['module']
            params = tasks['params']
            processdict = {}

            for connection in connections:
                if module == 'apt':
                    apt = APT(params['name'], Choice(params['state']))
                    status = apt.process(connection, task_counter)

                elif module == 'copy':
                    copy = Copy(params['src'],
                                params['dest'], params['backup'])
                    status = copy.process(connection, task_counter)

                elif module == 'command':
                    command = Command(params['command'])
                    status = command.process(connection, task_counter)

                elif module == 'sysctl':
                    sysctl = Sysctl(params['attribute'],
                                    params['value'], params['permanent'])
                    status = sysctl.process(connection, task_counter)

                elif module == 'service':
                    service = Service(params['name'], params['state'])
                    status = service.process(connection, task_counter)

                elif module == 'template':
                    template = Template(
                        params['src'], params['dest'], params['vars'])
                    status = template.process(connection, task_counter)

                co = connection.get_transport().sock.getpeername()[0]
                processdict[co] = status
                hosts[co].append(status.value)

            for ip_key in processdict:
                logging.info(
                    f"[{task_counter}] host={ip_key} op={module} status={processdict[ip_key].name}")

            task_counter += 1

    log_results(hosts)


def log_results(hosts):
    for ip_key in hosts:
        counter = Counter(hosts[ip_key])
        ok = counter[Status.OK.value]
        changed = counter[Status.CHANGED.value]
        ko = counter[Status.KO.value]

        logging.info(f"host={ip_key} ok={ok} changed={changed} ko={ko}")


if __name__ == "__main__":
    main()
