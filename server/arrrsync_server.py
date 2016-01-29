#!/bin/env python3
import os
import sys

from command_parser.parser import parser

def main():
    command = os.environ.get('SSH_ORIGINAL_COMMAND')
    program, args = parser(command)
    print(program)
    print(str(args))
    sys.exit(0)
