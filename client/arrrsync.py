#!/bin/env python3
import sys

from command_parser.parser import parser
from command_parser.client_parser import client_parser
from client.ssh import connectSSH


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

    client = connectSSH(args)

    try:
        clientConsole(client)
    except KeyboardInterrupt:
        print('Keyboard interrupt. Shutting down')
        client.close()
        sys.exit(1)
