#!/bin/env python3
import sys

from client.ssh import connectSSH
from client.terminal import Terminal
from commands.client_parser import client_parser


def main():
    # SSH Initialization
    args = vars(client_parser.parse_args())
    client, rsync = connectSSH(args)

    terminal = Terminal(client, rsync)
    running = True

    while running:
        try:
            running = terminal.update()
        except:
            terminal.restore_terminal()
            raise

    terminal.restore_terminal()
    sys.exit(0)
