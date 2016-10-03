import os
import subprocess

from client.helper import rsync_error_check

from commands.bash_formatter import escape
from commands.parser import parser, format_parse_error
from commands.assemble import cd_assemble, ls_assemble
from commands.ThrowingParser import ArgumentParseException


class Interpreter():
    def __init__(self, client, rsync, terminal):
        self.rsync = rsync
        self.client = client
        self.terminal = terminal

        stdin, stdout, stderr = client.exec_command('cd .')
        self.current_path = escape(stdout.readline().rstrip('\n'))

    def interpret(self, command):
        command = command.lstrip()
        # Parsing input, getting actual command name and arguments
        try:
            program, args = parser(command)
        except ArgumentParseException as error:
            self.terminal.add_lines(format_parse_error(error, command))
            return True

        if program == 'ls':
            compiled_paths = map(lambda path: os.path.join(self.current_path, path), args['path'])
            args['path'] = list(compiled_paths)
            # Send command to server
            stdin, stdout, stderr = self.client.exec_command(ls_assemble(args))

            # Print response
            for line in stdout.readlines():
                self.terminal.add_line(line.rstrip('\n'))

        elif program == 'cd':
            # Compute path
            targetPath = os.path.join(self.current_path, args['path'][0])
            args['path'] = [targetPath]

            # Send command to server
            stdin, stdout, stderr = self.client.exec_command(cd_assemble(args))

            errors = []
            for line in stderr.readlines():
                errors.append(line.rstrip('\n'))

            if not len(errors) > 1:
                # Save current position
                self.current_path = escape(stdout.readline().rstrip('\n'))
            else:
                # Print response
                self.terminal.add_lines(errors)

        elif program == 'push':
            rsync_args = ['rsync']
            rsync_args.append('--recursive')
            rsync_args.append('--partial')
            rsync_args.append('--perms')
            rsync_args.append('--times')
            rsync_args.append('--links')
            rsync_args.append('--info=progress2')

            rsync_args += args['path']

            target_path = '{}:{}'.format(
                self.rsync[0],
                os.path.join(self.current_path, args['target'])
            )
            rsync_args.append(target_path)

            rsync_process = subprocess.Popen(
                rsync_args,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT
            )
            # Add a line in the terminal self.lines. We need this for update_last_lines to work
            self.terminal.add_line('')
            # Continously pass output to terminal, abort rsync process if ctrl-c occurs
            try:
                no_error = True
                while rsync_process.poll() is None and no_error:
                    line = rsync_process.stdout.readline()
                    line = line.rstrip()
                    line = line.decode('utf-8')

                    if line != '':
                        self.terminal.update_last_lines([line])
                    no_error = rsync_error_check(line)
                stdout, stderr = rsync_process.communicate()
            except KeyboardInterrupt:
                self.terminal.add_line('Terminating rsync process, please wait')
                rsync_process.terminate()
                rsync_process.communicate()
                self.terminal.update_last_lines(['Rsync process terminated'])

        elif program == 'get':
            rsync_args = ['rsync']
            # rsync_args.append("-e 'ssh -p {}'".format(self.rsync[1]))
            rsync_args.append('--recursive')
            rsync_args.append('--partial')
            rsync_args.append('--perms')
            rsync_args.append('--times')
            rsync_args.append('--links')
            rsync_args.append('--info=progress2')

            compiled_paths = map(lambda path: '{}:{}'.format(
                self.rsync[0], os.path.join(self.current_path, path)), args['path'])
            rsync_args += list(compiled_paths)

            rsync_args.append(os.path.expanduser(args['target']))

            rsync_process = subprocess.Popen(
                rsync_args,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT
            )
            # Add a line in the terminal self.lines. We need this for update_last_lines to work
            self.terminal.add_line('')
            # Continously pass output to terminal, abort rsync process if ctrl-c occurs
            try:
                no_error = True
                while rsync_process.poll() is None and no_error:
                    line = rsync_process.stdout.readline()
                    line = line.rstrip()
                    line = line.decode('utf-8')

                    if line != '':
                        self.terminal.update_last_lines([line])
                    no_error = rsync_error_check(line)
                stdout, stderr = rsync_process.communicate()
            except KeyboardInterrupt:
                self.terminal.add_line('Terminating rsync process, please wait')
                rsync_process.terminate()
                rsync_process.communicate()
                self.terminal.update_last_lines(['Rsync process terminated'])

        elif program == 'exit':
            return False
        else:
            self.terminal.add_line('Invalid command. Valid commands are:')
            self.terminal.add_line('ls [path], cd [path], get [-r] [path], exit')

        return True
