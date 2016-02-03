import argparse

cd_parser = argparse.ArgumentParser(description='Parser for ls')

cd_parser.add_argument('path', nargs="?", default='.', type=str, help='A directory you want to cd into.')
