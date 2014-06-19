"""
file-like objects that save standard output text in a string and provide
standard input text from a string; redirect runs a passed-in function
with its output and input streams reset to these file-like class objects;
"""

import sys

class Output:
    def __init__(self):
        self.text = ''
    def write(self, string):
        self.text += string
    def writelines(self, lines):               # add each line in a list
        for line in lines: self.write(line)

class Input:
    def __init__(self, input = ''):
        self.text = input
    def read(self, size=None):
        if size == None:
            res, self.text = self.text, ''
        else:
            res, self.text = self.text[:size], self.text[size:]
        return res
    def readline(self):
        eoln = self.text.find('\n')   # find offset of next eoln
        if eoln == -1:                # slice off through eoln
            res, self.text = self.text, ''
        else:
            res, self.text = self.text[:eoln+1], self.text[eoln+1:]
        return res

def redirect(function, pargs, kargs, input):    # redirect stdin/out
    savestreams = sys.stdin, sys.stdout
    sys.stdin  = Input(input)
    sys.stdout = Output()
    try:
        result = function(*pargs, **kargs)      # run function with args
        output = sys.stdout.text
    finally:
        sys.stdin, sys.stdout = savestreams     # restore if exc or not
    return (result, output)
        
