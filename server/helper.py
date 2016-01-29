import os
import sys

def printResponse(stdout, stderr):
    stdout = stdout.decode('UTF-8')
    stderr  = stderr.decode('UTF-8')

    if stdout:
        print(stdout, end='')
    if stderr:
        print(stderr, end='')

def getTargetDir(root, extension):
    root = os.path.realpath(root)
    compiled_path = os.path.join(root, extension)
    compiled_path = os.path.realpath(compiled_path)
    if os.path.exists(compiled_path):
        relative_path = os.path.relpath(compiled_path, root)
        if not (relative_path == os.pardir or relative_path.startswith(os.pardir + os.sep)):
            return compiled_path
        else:
            print("'{}' doesn't exist".format(extension))
            sys.exit(0)
    else:
        print("'{}' doesn't exist".format(extension))
        sys.exit(0)
