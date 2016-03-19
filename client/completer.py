import os

from commands.parser import parser
from commands.bash_formatter import escape, unescape
from commands.assemble import assemble



class Completer():
    def __init__(self, client, terminal):
        self.client = client
        self.terminal = terminal

        self.completionList = []
        self.completionIndex = 0
        self.completionBuffer = None
        self.toBeCompleted = ''
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
            self.completionIndex = 0
            # Save buffer for later completions
            self.completionBuffer = buffer

            # Local completion
            if 'target' in args and args['target'] != '.':
                self.toBeCompleted = args['target']
                self.completionList = self.get_local_completion_list(args['target'])
            # Remote completion
            else:
                self.toBeCompleted = unescape(args['path'])[-1]
                self.completionList = self.get_remote_completion_list(self.toBeCompleted)

            # Filtering completion options to match given string
            self.completionList = list(filter(lambda string: string.startswith(self.toBeCompleted), self.completionList))

        return self.next()

    def next(self):
        """ Returns the next completion suggestion """
        if len(self.completionList) > 0:
            program, args = parser(self.completionBuffer)
            if 'target' in args and args['target'] != '.':
                args['target'] = escape(self.completionPath + self.completionList[self.completionIndex])
            else:
                args['path'][-1] = escape(self.completionList[self.completionIndex])
            buffer = assemble(program, args)
        else:
            buffer = self.completionBuffer

        # Increment completion index
        self.completionIndex += 1
        if self.completionIndex >= len(self.completionList):
            self.completionIndex = 0

        return buffer
