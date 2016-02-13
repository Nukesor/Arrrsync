import os


def log(log):
    path = os.path.expanduser('~/logfile')
    log_file = open(path, 'a')
    log_file.write(log)
    log_file.write('\n')
    log_file.close()
