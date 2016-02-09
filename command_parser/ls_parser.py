import argparse

ls_parser = argparse.ArgumentParser(description='Parser for ls', add_help=False)

ls_parser.add_argument('-l', action='store_true', help='Detailed list view for ls.')
ls_parser.add_argument('-a', action='store_true', help='Show all files. Including hidden files.')
ls_parser.add_argument('-h', action='store_true', help='Human readable output.')
ls_parser.add_argument('path', nargs='*', default=['.'], type=str, help='Specify a directory or file you want to inspect.')


def ls_reassemble(args):
    # Compile options for ls
    ls_args = ['ls']
    if args['a']:
        ls_args.append('-a')
    if args['l']:
        ls_args.append('-l')
    if args['h']:
        ls_args.append('-h')

    # Get absolute path from current position to target
    ls_args.append(args['path'][0])
    command = ' '.join(ls_args)
    return command
