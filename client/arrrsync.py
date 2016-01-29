#!/bin/env python3
import sys

from command_parser.parser import parser


def clientConsole():
    running = True
    while running:
        command = input('>>:')
        program, args = parser(command)
        if program == 'ls':
            print(program, args)
        elif program == 'cd':
            print(program, args)
        elif program == 'exit':
            running = False

    sys.exit(0)


def main():
    try:
        clientConsole()
    except KeyboardInterrupt:
        print('Keyboard interrupt. Shutting down')
        sys.exit(1)
