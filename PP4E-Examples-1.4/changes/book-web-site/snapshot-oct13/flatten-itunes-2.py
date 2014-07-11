"""
version 2, Nov11: normalize all itunes tree files
into a uniform 4 subdirs per device or location, to
support diffs when itunes trees have diverged badly;
this also keeps/copies every file in the itunes tree:
any duplicates are renamed with a numeric extension;
also updated to run on either Python 2.X and 3.X;
run the book's dirdiff.py to compare result trees;
more: www.rmi.net/~lutz/pp4e-updates.html#flatten;

original docs: flatten Itunes subfolder tree contents 
to store on a usb drive, for copying onto my Jeep's 
harddrive where subdirs don't work well;  endwith() 
now allows tuple of strings to try, so we don't need 
to say any(filelower.endswith(x) for x in seq);
"""
from __future__ import print_function  # to run on python 2.X

import os, pprint, sys
if sys.version_info[0] == 2: input = raw_input  # more 2.X compat

# get to/from dirs
workRoot   = os.getcwd()  # or r'F:\Music\resolve-itunes-nov11'
deviceName = input('Device? [e.g., VaioP]')
deviceDir  = os.path.join(workRoot,  deviceName)
itunesRoot = input('Itunes? [e.g., %s]' % r'C:\Users\mark\Stuff\Itunes')

# set file groupings 
categories = [
    dict(name='Playable',   exts=('.mp3', '.m4a')),
    dict(name='Protected',  exts=('.m4p',)),
    dict(name='Irrelevant', exts=('.jpg', '.ini', '.xml')),
    dict(name='Other',      exts=None) ]

for cat in categories:
     cat['subdir']     = os.path.join(deviceDir, cat['name'])
     cat['members']    = []
     cat['duplicates'] = 0
     cat['dupnames']   = []

# make copy-tree dirs
for dirpath in [deviceDir] + [cat['subdir'] for cat in categories]:
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)

def noteAndCopy(category, dirfrom, filename):
    """
    copy one file from itunes tree to normalized tree;
    rename file with a numeric suffix is it's a duplicate,
    so don't overwrite prior file (e.g. "track-N" generic
    names for tracks in different subdirs);  note the "while":
    though unlikely, the renamed name may also be a duplicate!
    also note the simple copy: read/write in chunks if needed;
    TBD - dup numbers per filename instead of per category?
    """
    fromname = toname = filename
    if toname in category['members']:
        category['duplicates'] += 1
        basename, ext = os.path.splitext(toname)
        suffix = '--%s' % category['duplicates']
        toname = basename + suffix + ext
        while toname in category['members']:
            suffix += '_'
            toname = basename + suffix + ext
        category['dupnames'].append(toname)

    category['members'].append(toname)  # plus dir?
    copyfrom = os.path.join(dirfrom, fromname)
    copyto   = os.path.join(category['subdir'], toname)
    open(copyto, 'wb').write( open(copyfrom, 'rb').read() )

# walk the itunes tree
for (dirHere, subsHere, filesHere) in os.walk(itunesRoot):
    for file in filesHere:
        for cat in categories[:-1]:
            if file.lower().endswith(cat['exts']):
                noteAndCopy(cat, dirHere, file)                
                break
        else:
            other = categories[-1]
            noteAndCopy(other, dirHere, file)

# report results
os.environ['PYTHONIOENCODING'] = 'utf-8'             # filenames? too late here?
sys.stdout = open(deviceName + '-results.txt', 'w')  # send all prints to a file 
for category in categories:
     print('*' * 80)
     for key in ('name', 'exts', 'subdir', 'duplicates', 'members', 'dupnames'):
         print(key, '=>', end=' ')
         if key in ('members', 'dupnames'): print()
         pprint.pprint(category[key])

print('=' * 80)
for cat in categories:
    print('Total %s: %s' % (cat['name'].ljust(10), len(cat['members'])))
