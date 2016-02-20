import os
import sys
import getpass
import paramiko
from paramiko.ssh_exception import PasswordRequiredException, BadAuthenticationType


def connectSSH(args):
    # Get keys and set autoadd policy
    client = paramiko.client.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.get_host_keys()

    # Read config file for later use
    ssh_config = paramiko.SSHConfig()
    user_config_file = os.path.expanduser('~/.ssh/config')
    if os.path.exists(user_config_file):
        with open(user_config_file) as f:
            ssh_config.parse(f)

    # Create default config
    default_config = {}
    default_config['user'] = getpass.getuser()
    default_config['port'] = 22
    default_config['identityfile'] = [os.path.expanduser('~/.ssh/id_rsa')]

    # Get commandline config
    pruned_args = {k: v for k, v in args.items() if v is not None}

    # Check if there is an entry for the specified hostname
    # Get ssh config from ~/.ssh/config
    config_file = ssh_config.lookup(args['hostname'])

    if config_file is not None:
        config = default_config
        config.update(config_file)
        config.update(pruned_args)
        if 'hostname' in config_file:
            config['hostname'] = config_file['hostname']
    else:
        config = default_config.update(pruned_args)

    config['port'] = int(config['port'])

    not_connected = True
    first_try = True
    while not_connected:
        try:
            if 'password' in config:
                client.connect(
                    config['hostname'],
                    port=config['port'],
                    username=config['user'],
                    key_filename=config['identityfile'],
                    password=config['password']
                )
            else:
                client.connect(
                    config['hostname'],
                    port=config['port'],
                    username=config['user'],
                    key_filename=config['identityfile']
                )
            not_connected = False

        except PasswordRequiredException:
            if first_try:
                print("No ssh-agent running or can't find a key in your ssh-agent.")
                print('Using keyfile: ' + config['identityfile'][0])
                print('If you want to connect using password authentication, enter your password here as well.')
                first_try = False
            try:
                config['password'] = getpass.getpass('Password: ')
            except (KeyboardInterrupt, EOFError):
                print('\nKeyboardInterrupt detected. Exiting')
                sys.exit(1)

        except BadAuthenticationType as error:
            print("Wrong password or wrong authentication type. Allowed types are : {}".format(str(error.allowed_types)))
            del config['password']

    rsync_hostname = config['user']
    rsync_hostname += '@'
    rsync_hostname += config['hostname'] if 'hostname' in config else args['host']

    return client, (rsync_hostname, config['port'])
