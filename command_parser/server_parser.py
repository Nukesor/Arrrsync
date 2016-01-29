import argparse

server_parser = argparse.ArgumentParser(description='Parser for ls')

server_parser.add_argument('command', type=str, help='Can be ignored.')
server_parser.add_argument('-ro', action='store_true', help='Read only for everything.')
server_parser.add_argument('-wo', action='store_true', help='Write only for everything.')
server_parser.add_argument('path', type=str, help='The directory to which the access should be restricted.')
