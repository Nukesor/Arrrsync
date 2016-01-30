#!/bin/env python3
import os
import sys
import subprocess

from command_parser.parser import parser
from command_parser.server_parser import server_parser
from server.helper import printResponse, getTargetDir


def main():
    arrrsync_args = vars(server_parser.parse_args(sys.argv))
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
            targetDir = getTargetDir(arrrsync_args['path'], args['path'])
            ls_args.append(targetDir)

        # Creating new subprocess for ls, read the output and print it
        process = subprocess.Popen(ls_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        printResponse(stdout, stderr)

    elif program == 'cd':
        cd_args = ['cd']
        # Args for cd
        if args['path']:
            targetDir = getTargetDir(arrrsync_args['path'], args['path'])
            cd_args.append(targetDir)

        print(targetDir)

    elif program == 'rsync':
        print('rsync stuff')

    sys.exit(0)
