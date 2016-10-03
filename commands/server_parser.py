import argparse

server_parser = argparse.ArgumentParser(description='Parser for arrrsync server.')

server_parser.add_argument('command', type=str, help='Can be ignored.')
server_parser.add_argument('-r', action='store_true', help='Read allowed.')
server_parser.add_argument('-w', action='store_true', help='Write allowed.')
server_parser.add_argument('path', type=str,
                           help='The directory to which the access should be restricted.')
