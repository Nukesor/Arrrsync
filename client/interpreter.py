import os
import subprocess

from commands.parser import parser, format_parse_error
from commands.bash_parser import escape
from commands.cd_parser import cd_reassemble
from commands.ls_parser import ls_reassemble
from commands.Throwing_Parser import ArgumentParserError


class Interpreter():
    def __init__(self, client, rsync, terminal):
        self.rsync = rsync
        self.client = client
        self.terminal = terminal

        stdin, stdout, stderr = client.exec_command('cd .')
        self.current_path = escape(stdout.readline().rstrip('\n'))

    def get_completion(self):
        stdin, stdout, stderr = self.client.exec_command('ls {}'.format(self.current_path))

        # Print response
        completion = []
        for line in stdout.readlines():
            completion.append(line.rstrip('\n'))
        return completion

    def interpret(self, command):
        # Parsing input, getting actual command name and arguments
        try:
            program, args = parser(command)
        except ArgumentParserError as error:
            self.terminal.add_lines(format_parse_error(error, command))
            return True

        if program == 'ls':
            compiled_paths = map(lambda path: os.path.join(self.current_path, path), args['path'])
            args['path'] = list(compiled_paths)
            # Send command to server
            stdin, stdout, stderr = self.client.exec_command(ls_reassemble(args))

            # Print response
            for line in stdout.readlines():
                self.terminal.add_line(line.rstrip('\n'))

        elif program == 'cd':
            # Compute path
            targetPath = os.path.join(self.current_path, args['path'][0])
            args['path'] = [targetPath]

            # Send command to server
            stdin, stdout, stderr = self.client.exec_command(cd_reassemble(args))

            errors = []
            for line in stderr.readlines():
                errors.append(line.rstrip('\n'))

            if not len(errors) > 1:
                # Save current position
                self.current_path = escape(stdout.readline().rstrip('\n'))
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

            compiled_paths = map(lambda path: '{}:{}'.format(self.rsync[0], os.path.join(self.current_path, path)), args['path'])
            rsync_args += list(compiled_paths)

            rsync_args.append('./')

            rsync_process = subprocess.Popen(' '.join(rsync_args), shell=True)
            rsync_process.communicate()

        elif program == 'exit':
            return False
        else:
            self.terminal.add_line('Invalid Command. Valid Commands are:')
            self.terminal.add_line('ls [path], cd [path], get [-r] [path], exit')

        return True
