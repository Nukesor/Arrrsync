def assemble(program, args):
    if program == 'ls':
        command = ls_reassemble(args)
    elif program == 'cd':
        command = cd_reassemble(args)
    elif program == 'get':
        command = get_reassemble(args)
    elif program == 'rsync':
        command = command = 'rsync'
    else:
        command = program

    return command


def get_reassemble(args):
    # Compile options for get
    get_args = ['get']
    if args['recursive']:
        get_args.append('-r')
    if 'path' in args:
        get_args += args['path']

    command = ' '.join(get_args)
    return command


def ls_reassemble(args):
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


def cd_reassemble(args):
    cd_args = ['cd']
    cd_args.append(args['path'][0])
    command = ' '.join(cd_args)
    return command
