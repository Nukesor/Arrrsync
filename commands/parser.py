from commands.terminal_parser import cd_parser, ls_parser, get_parser
from commands.rsync_parser import rsync_parser
from commands.bash_formatter import argsplit


def parser(unsplit_args):
    split = argsplit(unsplit_args)
    program = split[0]
    unparsed_args = split[1:]
    if program == 'ls':
        args = vars(ls_parser.parse_args(unparsed_args))
    elif program == 'cd':
        args = vars(cd_parser.parse_args(unparsed_args))
    elif program == 'get':
        args = vars(get_parser.parse_args(unparsed_args))
    elif program == 'rsync':
        for var in unparsed_args:
            # Workaround to remove e. from functions
            if var[:1] == '-' and var[1:2] != '-':
                if 'e.' in var:
                    fixed_argument = var.replace('e.', '')
                    unparsed_args[unparsed_args.index(var)] = fixed_argument

        args = vars(rsync_parser.parse_args(unparsed_args))
    else:
        args = {}

    return program, args


def format_parse_error(error, unsplit_args):
    output = []
    program = argsplit(unsplit_args)[0]

    # Format and pass error output
    message = error.args[0]
    message = message.split('\n')
    output += message
    output.append('\n')

    # Format and pass usage output
    usage = error.args[1]
    usage = usage.replace('arrrsync', program)
    usage = usage.split('\n')
    output += usage

    filtered_output = filter(lambda x: len(x) != 0, output)

    return list(filtered_output)
