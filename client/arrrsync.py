#!/bin/env python3
import sys

from client.commands.ls_parser import ls_parser
from client.commands.cd_parser import cd_parser


def clientConsole():
    running = True
    while running:
        command = input('>>:')
        split = command.split(' ')
        program = split[0]
        args = split[1:]
        if program == 'ls':
            print(ls_parser.parse_args(args))
        elif program == 'cd':
            print(cd_parser.parse_args(args))
        elif program == 'exit':
            running = False

    sys.exit(0)


def main():
    try:
        clientConsole()
    except KeyboardInterrupt:
        print('Keyboard interrupt. Shutting down')
        sys.exit(1)
