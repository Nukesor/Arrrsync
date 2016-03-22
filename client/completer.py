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

    def check_if_dir(self, path):
        """ Checks if the remote path is a directory """
        stdin, stdout, stderr = self.client.exec_command('isdir {}'.format(path))
        response = escape(stdout.readline().rstrip('\n'))
        if response == 'True':
            return True
        return False

    def remote_completion_list(self, relative_path):
        """ Get the matching completion for a relative path on the remote machine """

        # Normalize path
        if relative_path.startswith('~') or relative_path.startswith('/'):
            path = os.path.expanduser(relative_path)
            os.path.join(self.remote_directory_root, relative_path)
        else:
            path = relative_path
        path = os.path.normpath(path)

        if not self.check_if_dir(path):
            path = os.path.dirname(path)
            dirname = os.path.dirname(relative_path)
            # If the User uses '/' on filenames, we need to get the real directory
            # This is needed to handle wrong input
            while not self.check_if_dir(dirname) and dirname != './' and dirname != '/':
                dirname = os.path.dirname(dirname)
            basename = os.path.basename(relative_path)
        else:
            dirname = relative_path
            basename = ''

        stdin, stdout, stderr = self.client.exec_command('ls {}'.format(escape(path)))

        completion = []
        for line in stdout.readlines():
            if line.startswith(basename):
                completion.append(os.path.join(dirname, line.rstrip()))

        self.completion_list = completion

    def local_completion_list(self, relative_path):
        """ Get the matching completion for a relative path on the local machine """

        # Normalize path
        if relative_path.startswith('~'):
            path = os.path.expanduser(relative_path)
        elif relative_path.startswith('.') or relative_path == '':
            path = os.path.join(os.getcwd(), relative_path)
        else:
            path = path
        path = os.path.normpath(path)
        path = os.path.realpath(path)

        if not os.path.isdir(path):
            dirname = os.path.dirname(relative_path)
            # If the User uses '/' on files, we need to get the real directory
            # This is needed to handle wrong input
            while not os.path.isdir(dirname) and dirname != '':
                dirname = os.path.dirname(dirname)
            basename = os.path.basename(relative_path)
        else:
            dirname = relative_path
            basename = ''

        # Check for wrong dirname
        if dirname == '':
            dirname = './'
        # Check for bad userinput and wrong pathnames
        while not os.path.isdir(path):
            path = os.path.dirname(path)

        # Get list of files in dir
        itemlist = os.listdir(path)
        completion = []
        for item in itemlist:
            if item.startswith(basename):
                completion.append(os.path.join(dirname, item.rstrip()))

        self.completion_list = completion

    def complete(self, buffer):
        """ Actual function called by the terminal. Creates a list of possible completions and returns the first element """

        # Save buffer for later completions
        self.completion_buffer = buffer

        program, args = parser(buffer)
        if 'path' in args:
            self.completion_index = 0

            # Local completion
            if 'target' in args and args['target'] != '.':
                self.local_completion_list(args['target'])

            # Remote completion
            else:
                self.remote_completion_list(unescape(args['path'])[-1])

            return self.next()
        else:
            self.completion_list = []
            return self.completion_buffer

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
