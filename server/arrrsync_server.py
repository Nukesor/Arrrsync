#!/bin/env python3
import os
import sys
import subprocess

from command_parser.parser import parser
from command_parser.server_parser import server_parser
from server.helper import printResponse

def main():
    args = vars(server_parser.parse_args(sys.argv))
    command = os.environ.get('SSH_ORIGINAL_COMMAND')
    program, args = parser(command)
    if program == 'ls':
        ls_args = ['ls']
        # Args for ls
        if args['a']:
            ls_args.append('-a')
        if args['l']:
            ls_args.append('-l')
        if args['path']:
            ls_args.append(args['path'])

        # Creating new subprocess for ls, read the output and print it
        process = subprocess.Popen(ls_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        printResponse(stdout, stderr)

    elif program == 'cd':
        process = subprocess.Popen(["cd"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, errout = process.communicate()
        print(stdout, errout)
    elif program == 'rsync':
        print('rsync stuff')

    sys.exit(0)
