import argparse
import getpass

client_parser = argparse.ArgumentParser(
    description='The arrrsync client. Arrrsync will try to get all config data from your ssh config file. \n If this doesn\'t work you need to pass them as arguments.'
)

client_parser.add_argument('host', type=str, help='The address of the host.')
client_parser.add_argument('--user', type=str, default=getpass.getuser(), help='The user you want to connect to.')
client_parser.add_argument('--port', type=int, default=22, help='Port')
