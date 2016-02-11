from commands.cd_parser import cd_reassemble
from commands.ls_parser import ls_reassemble
from commands.get_parser import get_reassemble


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
