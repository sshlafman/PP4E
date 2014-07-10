#!/usr/bin/python
"""
###################################################################################
split a file into a set of parts; join.py puts them back together;
this is a customizable version of the standard Unix plsit command-line
utility; because it is written in Python, it also works on Windows and
can be easily modified; because it exports a function, its logic can 
also be imported and reused in other applications; 
###################################################################################
"""

import os
kilobytes = 1024
megabytes = kilobytes * 1000
chunksize = int(1.4 * megabytes)                  # default: roughly a floppy

def split(fromfile, todir, chunksize=chunksize):
    if not os.path.exists(todir):                 # caller handles errors
        os.mkdir(todir)                           # make dir, read/write parts
    else:  
        for fname in os.listdir(todir):           # delete any existing files
            os.remove(os.path.join(todir, fname))
    partnum = 0
    inputf = open(fromfile, 'rb')                  # binary: no decode, endline
    while True:                                   # eof=empty string from read
        chunk = input.read(chunksize)             # get next part <= chunksize
        if not chunk: break
        partnum += 1
        filename = os.path.join(todir, ('part%04d' % partnum))
        fileobj = open(filename, 'wb')
        fileobj.write(chunk)
        fileobj.close()                            # or simply open().write()
    inputf.close()
    assert partnum <= 9999                         # join sort fails if 5 digits
    return partnum

if __name__ == '__main__':
    if len
