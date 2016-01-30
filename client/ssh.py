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
        if 'user' in config and args['user']:
            user = config['user']
        else:
            user = args['user']
        client.connect(config['hostname'], port=int(config['port']), username=user)
    else:
        client.connect(args['host'], port=args['port'], username=args['user'])

    rsync_hostname = user if user else args['user']
    rsync_hostname += '@'
    rsync_hostname += config['hostname'] if 'hostname' in config else args['host']
    port = config['port'] if 'port' in config else args['port']

    return client, (rsync_hostname, port)
