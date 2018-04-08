import sys

def error(message, end = False):
    sys.stderr.write(str(message) + '\n')
    
    if end:
        exit(1)
