from command_parser.cd_parser import cd_parser
from command_parser.ls_parser import ls_parser


def parser(args):
    split = args.split(' ')
    program = split[0]
    unparsed_args = split[1:]
    if program == 'ls':
        args = ls_parser.parse_args(unparsed_args)
    elif program == 'cd':
        args = cd_parser.parse_args(unparsed_args)
    else:
        args = []
    return (program, args)
