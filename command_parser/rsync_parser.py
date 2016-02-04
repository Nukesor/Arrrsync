import argparse

rsync_parser = argparse.ArgumentParser(description='Parser for arrrsync rsync.')

rsync_parser.add_argument('-p', '--perms', action='store_true', help='')
rsync_parser.add_argument('-r', '--recursive', action='store_true', help='')
rsync_parser.add_argument('-t', '--times', action='store_true', help='')
rsync_parser.add_argument('-i', '--ignore-times', action='store_true', help='')
rsync_parser.add_argument('-s', '--protect-args', action='store_true', help='')
rsync_parser.add_argument('-f', '--filter', action='store_true', help='')
rsync_parser.add_argument('-x', '--one-file-system', action='store_true', help='')

rsync_parser.add_argument('-L', '--copy-links', action='store_true', help='')
rsync_parser.add_argument('-C', '--cvs-exclude', action='store_true', help='')

rsync_parser.add_argument('--partial', action='store_true', help='')
rsync_parser.add_argument('--server', action='store_true', help='')
rsync_parser.add_argument('--sender', action='store_true', help='')

rsync_parser.add_argument('files', nargs='*', type=str, help='The different directories we want to copy arround')
