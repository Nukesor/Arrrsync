from commands.ThrowingParser import ThrowingParser

# cd Parser
cd_parser = ThrowingParser(description='Parser for ls', add_help=False)
cd_parser.add_argument('path', nargs='*', default=['.'], type=str, help='A directory you want to cd into.')


# get Parser
get_parser = ThrowingParser(description='Parser for get', add_help=False)
get_parser.add_argument('-r', '--recursive', action='store_true', help='Recursive get')
get_parser.add_argument('path', nargs='*', default=['.'], type=str, help='The files you want to get.')


# ls Parser
ls_parser = ThrowingParser(description='Parser for ls', add_help=False)
ls_parser.add_argument('-l', action='store_true', help='Detailed list view for ls.')
ls_parser.add_argument('-a', action='store_true', help='Show all files. Including hidden files.')
ls_parser.add_argument('-h', action='store_true', help='Human readable output.')
ls_parser.add_argument('path', nargs='*', default=['.'], type=str, help='Specify a directory or file you want to inspect.')
