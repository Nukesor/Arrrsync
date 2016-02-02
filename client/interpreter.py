import os
import subprocess

from command_parser.parser import parser
from command_parser.bash_parser import escape


class Interpreter():
    def __init__(self, client, rsync, terminal):
        self.rsync = rsync
        self.client = client
        self.terminal = terminal

        stdin, stdout, stderr = client.exec_command('cd .')
        self.current_path = stdout.readline().rstrip('\n')

    def interpret(self, command):
        # Parsing input, getting actual command name and arguments
        program, args = parser(command)
        if program == 'ls':
            # Compile options for ls
            ls_args = ['ls']
            if args['a']:
                ls_args.append('-a')
            if args['l']:
                ls_args.append('-l')

            # Get absolute path from current position to target
            targetPath = os.path.join(self.current_path, args['path'])
            ls_args.append(escape(targetPath))

            # Send command to server
            stdin, stdout, stderr = self.client.exec_command(' '.join(ls_args))

            # Print response
            for line in stdout.readlines():
                self.terminal.add_line(line.rstrip('\n'))

        elif program == 'cd':
            cd_args = ['cd']
            # Get absolute path from current position to target
            targetPath = os.path.join(self.current_path, args['path'])

            cd_args.append(escape(targetPath))
            stdin, stdout, stderr = self.client.exec_command(' '.join(cd_args))

            errors = []
            for line in stderr.readlines():
                errors.append(line.rstrip('\n'))

            if not len(errors) > 1:
                # Save current position
                self.current_path = stdout.readline().rstrip('\n')
            else:
                # Print response
                self.terminal.add_lines(errors)

        elif program == 'get':
            rsync_args = ['rsync']
            rsync_args.append("-e 'ssh -p {}'".format(self.rsync[1]))
            if args['recursive']:
                rsync_args.append('--recursive')
            rsync_args.append('--partial')
            rsync_args.append('--perms')
            rsync_args.append('--times')

            for path in args['files']:
                compiled_path = '{}:{}'.format(self.rsync[0], os.path.join(self.current_path, path))
                rsync_args.append(escape(compiled_path))

            rsync_args.append('./')

            rsync_process = subprocess.Popen(' '.join(rsync_args), shell=True)
            rsync_process.communicate()

        elif program == 'exit':
            return False

        return True
