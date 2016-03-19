

def rsync_error_check(line):
    if 'Permission denied' in line:
        return False
    return True
