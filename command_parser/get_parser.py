import argparse

get_parser = argparse.ArgumentParser(description='Parser for ls')

get_parser.add_argument('-r', '--recursive', action='store_true', help='Detailed list view for ls.')
get_parser.add_argument('files', nargs='*', default=['.'], type=str, help='Specify a directory or file you want to inspect.')
