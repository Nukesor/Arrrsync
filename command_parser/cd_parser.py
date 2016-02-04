import argparse

cd_parser = argparse.ArgumentParser(description='Parser for ls')

cd_parser.add_argument('path', nargs='*', default=['.'], type=str, help='A directory you want to cd into.')


def cd_reassemble(args):
    cd_args = ['cd']
    cd_args.append(args['path'][0])
    command = ' '.join(cd_args)
    return command
