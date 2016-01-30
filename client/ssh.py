import os
import paramiko


def connectSSH(args):
    # Get keys and set autoadd policy
    client = paramiko.client.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.get_host_keys()

    # Read config file for later use
    ssh_config = paramiko.SSHConfig()
    user_config_file = os.path.expanduser("~/.ssh/config")
    if os.path.exists(user_config_file):
        with open(user_config_file) as f:
            ssh_config.parse(f)

    # Check if there is an entry for the specified hostname
    config = ssh_config.lookup(args['host'])
    if config is not None:
        client.connect(config['hostname'], port=int(config['port']))
    else:
        client.connect(args['host'], port=args['port'], username=args['user'])

    return client
