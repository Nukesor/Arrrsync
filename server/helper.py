
def printResponse(stdout, stderr):
    stdout = stdout.decode('UTF-8')
    stderr  = stderr.decode('UTF-8')

    if stdout:
        print(stdout, end='')
    if stderr:
        print(stderr, end='')
