import os

from commands.parser import parser
from commands.bash_formatter import escape, unescape
from commands.assemble import assemble


class Completer():
    def __init__(self, client, terminal):
        self.client = client
        self.terminal = terminal

        self.completion_list = []
        self.completion_index = 0
        self.completion_buffer = None
        self.completionPath = ''

        stdin, stdout, stderr = client.exec_command('cd .')
        self.remote_directory_root = escape(stdout.readline().rstrip('\n'))

    def get_remote_completion_list(self, relative_path):
        """ Get the completion for a relative path on the remote machine """

        # Normalize path
        if relative_path.startswith('~') or relative_path.startswith('/'):
            path = os.path.expanduser(relative_path)
            os.path.join(self.remote_directory_root, relative_path)

        elif relative_path.startswith('.'):
            path = os.path.join(self.terminal.interpreter.current_path, relative_path)
        else:
            path = relative_path
        path = os.path.normpath(path)

        # The path is a file, but we need a directory for completion
        if not path.endswith('/'):
            path = os.path.dirname(path)

        stdin, stdout, stderr = self.client.exec_command('ls {}'.format(escape(path)))

        # format for later use
        completion = []
        for line in stdout.readlines():
            if path.endswith('/'):
                full_path = path + line.rstrip('\n')
            else:
                full_path = line.rstrip('\n')
            completion.append(full_path)
        return completion

    def get_local_completion_list(self, relative_path):
        """ Get the completion for a relative path on the local machine """

        # Normalize path
        if relative_path.startswith('~'):
            path = os.path.expanduser(relative_path)
        elif relative_path.startswith('.'):
            path = os.path.join(os.getcwd(), relative_path)
        path = os.path.normpath(path)
        path = os.path.realpath(path)

        # Get directory name, if path is not a directory
        if not os.path.isdir(path):
            path = os.path.dirname(path)

        # Get list of files in dir
        itemlist = os.listdir(path)
        completion = []
        for item in itemlist:
            completion.append(relative_path + item)
        return completion

    def complete(self, buffer):
        """ Actual function called by the terminal. Creates a list of possible completions and returns the first element """
        program, args = parser(buffer)
        if 'path' in args:
            self.completion_index = 0
            # Save buffer for later completions
            self.completion_buffer = buffer

            # Local completion
            if 'target' in args and args['target'] != '.':
                to_be_completed = args['target']
                self.completion_list = self.get_local_completion_list(to_be_completed)
            # Remote completion
            else:
                to_be_completed = unescape(args['path'])[-1]
                self.completion_list = self.get_remote_completion_list(to_be_completed)

            # Filtering completion options to match given string
            self.completion_list = list(filter(lambda string: string.startswith(to_be_completed), self.completion_list))

        return self.next()

    def next(self):
        """ Returns the next completion suggestion """
        if len(self.completion_list) > 0:
            program, args = parser(self.completion_buffer)
            if 'target' in args and args['target'] != '.':
                args['target'] = escape(self.completionPath + self.completion_list[self.completion_index])
            else:
                args['path'][-1] = escape(self.completion_list[self.completion_index])
            buffer = assemble(program, args)
        else:
            buffer = self.completion_buffer

        # Increment completion index
        self.completion_index += 1
        if self.completion_index >= len(self.completion_list):
            self.completion_index = 0

        return buffer
