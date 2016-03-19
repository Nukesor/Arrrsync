#!/bin/env python3
import os
import sys
import subprocess

from server.helper import print_response, get_target_dir
from server.log import log

from commands.parser import parser
from commands.bash_formatter import unescape
from commands.server_parser import server_parser


def main():
    arrrsync_args = vars(server_parser.parse_args(sys.argv))
    command = os.environ.get('SSH_ORIGINAL_COMMAND')
    program, args = parser(command)
    if program is None:
        print('Invalid Command. Supported Programs: \nls \ncd \nisdir \nrsync')
    if program == 'ls':
        ls_args = ['ls']
        # Args for ls
        if args['a']:
            ls_args.append('-a')
        if args['l']:
            ls_args.append('-l')
        if args['h']:
            ls_args.append('-h')
        if args['path']:
            for item in args['path']:
                targetDir = get_target_dir(arrrsync_args['path'], unescape(item))
                ls_args.append(targetDir)

        # Creating new subprocess for ls, read the output and print it
        process = subprocess.Popen(ls_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        print_response(stdout, stderr)

    elif program == 'cd':
        # Args for cd
        if args['path']:
            target = args['path'][0]
            targetDir = get_target_dir(arrrsync_args['path'], unescape(target))
            if os.path.isdir(targetDir):
                print(targetDir)
            else:
                print("'{}' is not a directory".format(args['path']), file=sys.stderr)

    elif program == 'isdir':
        # Args for cd
        if args['path']:
            target = args['path'][0]
            targetDir = get_target_dir(arrrsync_args['path'], unescape(target))
            if os.path.isdir(targetDir):
                print('True')
            else:
                print('False')
        print("False")

    elif program == 'rsync':
        # Compile rsync arguments
        rsync_args = ['rsync']
        if args['server']:
            rsync_args.append('--server')

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
        rsync_args.append('--info=progress2')

        # Sender flag is set. This means the server will send some data
        if args['sender']:
            if arrrsync_args['r'] is not True:
                print("Reading is not for your key allowed. Aborting")
                sys.exit(0)

            rsync_args.append('--sender')
            for path in args['path']:
                if not path == '.':
                    path = get_target_dir(arrrsync_args['path'], unescape(path))
                rsync_args.append(path)
        # Sender flag isn't set. This means the server will receive some data
        else:
            if arrrsync_args['w'] is not True:
                print("Writing is not for your key allowed. Aborting")
                sys.exit(0)
            path = args['path'][-1]
            if not path == '.':
                path = get_target_dir(arrrsync_args['path'], unescape(path))
            rsync_args.append(path)


        rsync_process = subprocess.Popen(rsync_args, shell=False)
        rsync_process.communicate()

    sys.exit(0)
