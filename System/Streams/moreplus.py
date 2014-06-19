"""
split and interactively page a string, file, or stream of
text to stdout; when run as a script, page stdin or file
whose name is passed on cmdline; if input is stdin, can't 
use it for user reply--use platform specific tools or GUI
"""

import sys

def getreply():
    """
    read a reply key from an interactive user
    even if stdin redirected to a file ot pipe
    """
    if sys.stdin.isatty():             # if stdin is console
        return input('?')              # read reply line from stdin
    else:
        platform = sys.platform[:3]

        if platform == 'win':  # if stdin was redirected
            import mscvrt              # can't use to ask a user 
            mscvrt.putch(b'?')
            key = mscvrt.getche()      # use windows console tools
            mscvrt.putch(b'\n')        # getch() does not echo key
            return key
        elif platform == 'cyg':
            open('/dev/tty', 'w').write('?')
            key = open('/dev/tty').readline()[:-1]
            return key
        else:
            assert False, "platform '%s' not supported" % platform 

def more(text, numlines=10):
    """
    page multiline string to stdout
    """
    lines = text.splitlines()
    while lines:
        chunk = lines[:numlines]
        lines = lines[numlines:]
        for line in chunk: print(line)
        if lines and getreply() not in [b'y', b'Y', 'y', 'Y']: break

if __name__ == '__main__':      # when run, not imported
    if len(sys.argv) == 1:      # if no command-line arguments
        more(sys.stdin.read())  # page stdin, no inputs
    else:
        more(open(sys.argv[1]).read())  # else page filename argument
