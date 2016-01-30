#!/bin/env python3
import os
import sys
import subprocess

from command_parser.parser import parser
from command_parser.server_parser import server_parser
from server.helper import printResponse, getTargetDir
from server.log import log


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
        # Args for cd
        if args['path']:
            targetDir = getTargetDir(arrrsync_args['path'], args['path'])
            if os.path.isdir(targetDir):
                print(targetDir)
            else:
                print("'{}' is not a directory".format(args['path']), file=sys.stderr)

    elif program == 'rsync':
        # Compile rsync arguments
        rsync_args = ['rsync']
        if args['server']:
            rsync_args.append('--server')
        if args['sender']:
            rsync_args.append('--sender')

        if args['recursive']:
            rsync_args.append('--recursive')
        if args['partial']:
            rsync_args.append('--partial')
        if args['perms']:
            rsync_args.append('--perms')
        if args['times']:
            rsync_args.append('--times')

        if args['one_file_system']:
            rsync_args.append('--one-file-system')
        if args['cvs_exclude']:
            rsync_args.append('--cvs-exclude')
        if args['ignore_times']:
            rsync_args.append('--ignore-times')

        # Don't allow users to copy symlinked directories.
        rsync_args.append('--links')
        rsync_args.append('--rsh=.')

        for path in args['files']:
            if not path == '.':
                path = getTargetDir(arrrsync_args['path'], path)
            rsync_args.append(path)

        rsync_process = subprocess.Popen(rsync_args, shell=False)
        rsync_process.communicate()

    sys.exit(0)
