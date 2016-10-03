import argparse

client_parser = argparse.ArgumentParser(
    description="The arrrsync client. Arrrsync will try to get all config data "
    "from your ssh config file. \n If this doesn't work you need to pass them as arguments."
)

client_parser.add_argument('hostname', type=str, help='The address or alias of the host.')
client_parser.add_argument('-u', '--user', type=str, help='The user you want to connect to.')
client_parser.add_argument('--password', type=str, help='The password for your identityfile, '
                           'if no ssh-agent is running. Can be supplied interactively later')
client_parser.add_argument('-p', '--port', type=int, help='Port')
client_parser.add_argument('-k', '--identityfile', type=str,
                           help='The keyfile you use for connection')
