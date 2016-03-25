from commands.ThrowingParser import ThrowingParser

# cd Parser
cd_parser = ThrowingParser(description='Parser for ls', add_help=False)
cd_parser.add_argument('path', nargs='*', default=['.'], type=str, help='A directory you want to cd into.')

# get Parser
get_parser = ThrowingParser(description='Parser for get', add_help=False)
get_parser.add_argument('path', nargs='*', default=['.'], type=str, help='The files you want to get.')
get_parser.add_argument('-t', '--target', default='.', type=str, help='The file/directory your files will be downloaded to.')

# push Parser
push_parser = ThrowingParser(description='Parser for push', add_help=False)
push_parser.add_argument('path', nargs='*', type=str, help='The files you want to push.')
push_parser.add_argument('-t', '--target', default='.', type=str, help='The file/directory you want to push to.')

# ls Parser
ls_parser = ThrowingParser(description='Parser for ls', add_help=False)
ls_parser.add_argument('-l', action='store_true', help='Detailed list view for ls.')
ls_parser.add_argument('-a', action='store_true', help='Show all files. Including hidden files.')
ls_parser.add_argument('-h', action='store_true', help='Human readable output.')
ls_parser.add_argument('path', nargs='*', default=['.'], type=str, help='Specify a directory or file you want to inspect.')

# isdir Parser
isdir_parser = ThrowingParser(description='Parser for ls', add_help=False)
isdir_parser.add_argument('path', nargs='*', default=['.'], type=str, help='A directory you want to cd into.')
