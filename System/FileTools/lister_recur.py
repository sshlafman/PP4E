"list file tree recursively"

import sys, os

def lister(thisdir):
    print('curdir: [' + thisdir + ']')
    dir_list = os.listdir(thisdir)
    for fname in dir_list:
        if os.path.isdir(fname):
            lister(fname)
        else:
            path = os.path.join(thisdir,fname)
            print(path)

if __name__ == '__main__':
    lister(sys,argv[1])
