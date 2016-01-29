import argparse

ls_parser = argparse.ArgumentParser(description='Parser for ls')

ls_parser.add_argument('-l', action='store_true', help='Detailed list view for ls.')
ls_parser.add_argument('-a', action='store_true', help='Show all files. Including hidden files.')
ls_parser.add_argument('path', nargs='?', default='.', type=str, help='Specify a directory or file you want to inspect.')
