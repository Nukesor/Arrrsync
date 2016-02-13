from commands.Throwing_Parser import ThrowingParser

get_parser = ThrowingParser(description='Parser for get', add_help=False)

get_parser.add_argument('-r', '--recursive', action='store_true', help='Recursive get')
get_parser.add_argument('path', nargs='*', default=['.'], type=str, help='The files you want to get.')


def get_reassemble(args):
    # Compile options for get
    get_args = ['get']
    if args['recursive']:
        get_args.append('-r')
    if 'path' in args:
        get_args += args['path']

    command = ' '.join(get_args)
    return command
