#!/bin/env python3
import os
import sys

import paramiko

from command_parser.parser import parser
from command_parser.client_parser import client_parser


def clientConsole(client):
    running = True
    while running:
        command = input('>>: ')
        program, args = parser(command)
        if program == 'ls':
            ls_args = ['ls']
            # Args for ls
            if args['a']:
                ls_args.append('-a')
            if args['l']:
                ls_args.append('-l')
            ls_args.append(args['path'])
            stdin, stdout, stderr = client.exec_command(' '.join(ls_args))

            for line in stdout.readlines():
                print(line, end='')

        elif program == 'cd':
            print(program, args)
        elif program == 'exit':
            running = False

    client.close()
    sys.exit(0)


def main():
    args = vars(client_parser.parse_args())

    # Get keys and set autoadd policy
    client = paramiko.client.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.get_host_keys()

    # Read config file for later use
    ssh_config = paramiko.SSHConfig()
    user_config_file = os.path.expanduser("~/.ssh/config")
    if os.path.exists(user_config_file):
        with open(user_config_file) as f:
            ssh_config.parse(f)

    # Check if there is an entry for the specified hostname
    config = ssh_config.lookup(args['host'])
    if config is not None:
        client.connect(config['hostname'], port=int(config['port']))
    else:
        client.connect(args['host'], port=args['port'], username=args['user'])

    try:
        clientConsole(client)
    except KeyboardInterrupt:
        print('Keyboard interrupt. Shutting down')
        client.close()
        sys.exit(1)
