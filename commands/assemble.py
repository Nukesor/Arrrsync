def assemble(program, args):
    if program == 'ls':
        command = ls_assemble(args)
    elif program == 'cd':
        command = cd_assemble(args)
    elif program == 'get':
        command = get_assemble(args)
    elif program == 'push':
        command = push_assemble(args)
    elif program == 'rsync':
        command = command = 'rsync'
    else:
        command = program

    return command


def get_assemble(args):
    # Compile options for get
    get_args = ['get']
    if 'path' in args:
        get_args += args['path']
    if 'target' in args and args['target'] != '.':
        get_args.append('--target')
        get_args.append(args['target'])

    command = ' '.join(get_args)
    return command


def push_assemble(args):
    # Compile options for get
    get_args = ['push']
    if 'path' in args:
        get_args += args['path']
    if 'target' in args and args['target'] != '.':
        get_args.append('--target')
        get_args.append(args['target'])

    command = ' '.join(get_args)
    return command


def ls_assemble(args):
    # Compile options for ls
    ls_args = ['ls']
    if args['a']:
        ls_args.append('-a')
    if args['l']:
        ls_args.append('-l')
    if args['h']:
        ls_args.append('-h')
    if 'path' in args:
        ls_args += args['path']

    command = ' '.join(ls_args)
    return command


def cd_assemble(args):
    cd_args = ['cd']
    cd_args.append(args['path'][0])
    command = ' '.join(cd_args)
    return command
