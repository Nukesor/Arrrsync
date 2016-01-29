import argparse

ls_parser = argparse.ArgumentParser(description='Parser for ls')

ls_parser.add_argument('-l', action='store_true', help='Detailed list view for ls.')
ls_parser.add_argument('-a', action='store_true', help='Show all files. Includes hidden files.')
